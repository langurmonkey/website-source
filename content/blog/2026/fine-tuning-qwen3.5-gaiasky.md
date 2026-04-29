+++
author = "Toni Sagristà Sellés"
title = "Fine-tuning Qwen3.5 for Gaia Sky"
description = "How I fine-tuned Qwen3.5 4/9B models to become Gaia Sky experts"
date = 2026-04-01
categories = ["AI"]
tags = ["LLM", "AI", "LM Studio", "fine-tuning", "AI inference", "unsloth"]
featuredpath = "date"
type = "post"
js = ["/js/mathjax3.js"]
+++ 

A little over a year ago I set up a [local pipeline](/blog/2025/local-llm-rag) to use different [LLM](@ "Large Language Model")s to [respond to Gaia Sky questions](/blog/2025/gaiasky-ai-assistant) using [RAG](@ "Retrieval Augmented Generation"). In that post, I built a dynamic scrapper that parsed the Gaia Sky website and documentation and ingested the content it into a vector database. Then, I built a minimal terminal chatbot interface that received the user prompt, queried the database for semantically similar data, and built up the context for each LLM call. The results were promising, and I found that they (obviously) strongly depended on the model used.

Fast forward a few months, and the Qwen 3.5 models were released by Alibaba. The general consensus is that they are quite good for their size. I've been testing them for local inference with a similar impression. I thought that it would be interesting to repeat the exercise of creating a Gaia Sky AI assistant, but using a radically different approach: Instead of RAG, I would **fine-tune the model** itself. In this post, I describe this fine-tuning project, from the creation and engineering of the training dataset to the fine-tuning and production of the final [GGUF](@ "GPT-Generated Unified Format") models.

<!--more-->

This project is composed by two, very distinct parts, which map to top-level chapters in this post:

- [Training dataset creation](#training-dataset-creation)
- [Fine tuning](#fine-tuning)

At the end I quickly evaluate the results in the [testing](#testing) section.

The source code, dataset, and models discussed in this post are in the following repositories:

- Dataset creation and fine-tuning - <i class="fa fa-gitea" aria-hidden="true" title="Codeberg"></i> [gaiasky-finetune](https://codeberg.org/gaiasky/gaiasky-finetune)
- Gaia Sky training dataset repository - <i class="fa fa-git-square" aria-hidden="true" title="Codeberg"></i> [gaiasky-training-dataset](https://hf.co/Langurmonkey/gaiasky-training-dataset)
- Qwen3.5 Gaia Sky fine-tuned models - <i class="fa fa-git-square" aria-hidden="true" title="Codeberg"></i> [gaiasky-qwen-3.5-gguf](https://hf.co/Langurmonkey/gaiasky-qwen-3.5-gguf)

## Hardware

Here is the hardware I have used to create the dataset and fine-tune the model:

- **Desktop PC** - Arch Linux, Intel(R) Core(TM) i7-7700 (8) @ 4.20 GHz, 32 GB RAM, NVIDIA GeForce GTX 1070 8 GB.
- **Laptop 1** - Windows 11, WSL2 (Arch Linux), Intel(R) Core(TM) Ultra 9 275HX (24) @ @ 3.07 GHz, 32 GB RAM, NVIDIA GeForce RTX 5080 Mobile 16 GB.
<a href="#laptop2"></a>
- **Laptop 2** - Arch Linux, Intel(R) Core(TM) i7 8750H (12) @ 4.10 GHz, 16 GB RAM, NVIDIA GeForce GTX 1060 Mobile 6 GB.

## Training dataset creation

The creation of the training dataset is the most important piece of work in this project. It is composed of three parts:

- [Documentation dataset](#documentation-dataset)
- [API dataset](#api-dataset)
- [Identity](#identity)

### Documentation dataset

When I started this project, my first instinct was "more is better." I thought that if I fed the model every single `.java`, `.glsl`, `.rst`, and `.md` file in the Gaia Sky repositories (project, documentation, etc.), it would emerge as an expert. Oh boy, was I wrong.

A large codebase contains a lot of boilerplate noise. Getters, setters, license blocks, and infrastructure code that doesn't actually help a model understand *how* the engine works or *how* to write scripts for it. I soon realized that the dataset is the single most important part of the project, and it needed a surgical approach.

The plan was to automate the process of creating the dataset to a degree, and then use it to fine-tune the **Qwen 3.5 4B** and **8B** model variants.

I wrote `generate-raw-dataset.py` to act as a high-pass filter. Instead of a blind crawl, I implemented an **allowlist** system. I would only let in the load-bearing files:

* **Documentation:** By far, the most important data, containing exhaustive human-written documentation pages. We convert the documentation [RST](@ "reStructuredText") files to Markdown with `pandoc`, and then we add some additional key files, like the project's `README.md`.
* **Core Logic:** Selected Java files that are representative of the brain of the engine (main loop, scene, renderer, etc.).
* **Visual Logic:** Selected shader files that define the look of the cosmos (stars, particles, PBR, etc.).

Almost every source file in Gaia Sky starts with a copyright header. This is "dead weight" for training. I added a regex-based stripper to ensure the model's limited context window was filled with code logic, not license text:

```python
def strip_java_copyright(content):
    # Matches the opening /* until the first */ at the start of the file
    content = re.sub(r'^/\*.*?\*/', '', content, count=1, flags=re.DOTALL)
    return content.strip()
```

The output of this first phase was a `jsonl` file where each line represented a single, cleaned-up file. It looked like this:

```json
{
  "instruction": "core/src/gaiasky/util/coord/Coordinates.java",
  "output": "public class Coordinates {\n    // Implementation of transformation matrices...\n}",
  "source_file": "core/src/gaiasky/util/coord/Coordinates.java"
}
```

This provided the "Context" for the next phase. However, a model trained directly on this would just learn to autocomplete files. To make it an *assistant*, we had to turn these files into a conversation.

Once I had a clean extraction of the most relevant information pieces, I faced a new problem. A raw dump of a `Coordinates.java` file is great for a search engine, but it is not a conversation. To turn these files into training data, I used a "teacher" model, Qwen 3.5 27B, to look at each file and generate a specific number of Q&A pairs. I wrote `distill-dataset.py` to handle this. The script calculates how many questions a file is worth based on its length and type. A long documentation file might get 25 Q&A pairs, while a short shader might only get 4. Below is an extract of the method that computes the number of target pairs for a file.

```python
def calculate_target_pairs(file_path, content):
    """Determine how many Q&A pairs to generate based on file metadata."""
    filename = file_path.lower()
    content_len = len(content)

    # Skip files that are essentially empty
    if content_len < 150:
        return 0

    # Set a modest base count that depends on type
    # Docs are high-value, so they start slightly higher than code
    if filename.endswith(('.md', '.rst')):
        base_count = 4
        # 1 pair per 750 characters for documentation
        chars_per_pair = 750 
    else:
        base_count = 2
        # 1 pair per 1500 characters for source code
        chars_per_pair = 2000

    # Calculate length-based bonus without a tiny cap
    # This scales better for massive files while keeping short files lean
    length_bonus = content_len // chars_per_pair
    
    # Sum and apply a reasonable maximum
    final_count = base_count + length_bonus
    
    # Cap it to avoid overwhelming the distillation for single files
    # but ensure even tiny files get at least the base_count
    return max(base_count, min(final_count, 20))
```

Initially, I used the [MoE](@ "Mixture of Experts") Qwen 3.5 30B A3B, but it was consistently outputting the wrong format. Then I switched to the 27B dense model, and it performed a little better. Even so, I had to tell the model **exactly** how to behave. Here are the key items I learned the hard way:

* **Match the answer type:** If the question doesn't ask for code, don't provide it.
* **Grounding:** Every claim must be directly grounded on the source text.
* **Diversity:** Every question must cover a different detail.

I also found that, at these model sizes, it is better to batch Q&A pairs instead of asking the model to provide 20 of them in one go. I finally gravitated to 3 Q&A pairs per inference call. To prevent the model from repeating itself across batches, I tracked existing questions and fed them back into the prompt as exclusions.

The prompt is constructed as follows:

```python
# A snippet from the distillation prompt
prompt = (
    f"You are a Gaia Sky technical expert. {file_hint}\n"
    f"Generate exactly {current_target} Q&A pairs strictly based on the source text below. "
    "Every fact and claim in your answers must be directly grounded in the source text. "
    "Never invent API calls or function names not present in the source. "
    "Match the answer type to the question: if no code is asked for, give no code. "
    "HIGHLY DIVERSE Q&A pairs. Every question must cover a COMPLETELY DIFFERENT topic or detail "
    "of the source text than the ones already provided. "
    f"{avoid_context}\n\n"
    "Format the output as JSONL: one JSON object per line, with the question in the "
    "\"instruction\" field and the answer in the \"output\" field. "
    "Output ONLY the JSONL, nothing else.\n\n"
    f"SOURCE FILE: {file_path}\n"
    f"{'=' * 60}\n"
    f"{file_content[:context_limit]}\n"
    f"{'=' * 60}"
)
```

It consists of the following parts:

- Base text - This is composed by the raw strings in the `prompt` variable.
- The file hint (`{file_hint}`) - We add hints depending on the filetype. The following table displays the hint for each type.

  | Filetype   | Extensions   | Hint |
  |------------|--------------|------|
  | Java       | `.java`      | This is Java source code. Focus on class responsibilities, method signatures, and architectural patterns. Do NOT generate Python scripting examples. |
  | Python     | `.py`        | This is Python scripting code for the Gaia Sky API. Questions about usage and parameters are appropriate. |
  | Shader     | `.glsl`      | This is a GLSL shader. Focus on the rendering technique, uniforms, and mathematical operations. Do NOT generate Python scripting examples. |
  | Docs       | `.md` `.rst` | This is documentation. Focus on concepts, features, workflows, and user-facing features. |
- The pair count (`{current_target}`) - Contains the number of Q&A pairs to generate.
- The previous Q&A pairs, if any (`{avoid_context}`) - This is constructed by listing the existing pairs, as parsed by the program in the output, or accumulated in the current run.
  ```python
     instr_list = [p['instruction'] for p in existing_pairs]
     avoid_context = (
         "\nDo NOT repeat or rephrase any of these already-covered questions:\n"
         + "\n".join(f"- {instr}" for instr in instr_list)
     )
  ``` 
- The filepath and content (`{file_path}`, `{file_content}`) - Contain the filename and the actual content, which is capped to fit within the context length.

However, local LLMs tend to be chatty. Even with such strict instructions, larger models like the 27B sometimes also mess up. From time to time, this model would leak its own reasoning into the output. It would start its response with `"The user asked to provide 34 Q&A pairs given the source material..."` or it would include meta-talk like `"This question is safe because it is derived from line 45."`

This created *dirty* data that polluted the dataset and undermined the fine-tuning process. If I trained on this, the final model would start every answer by talking to itself.

To fix this, I built `sanitize-jsonl.py`. This script is a heavy-duty cleaner that uses regex to strip out training artifacts. It first tries to rescue bad rows, and if it fails, it deletes them. If the model accidentally put both the question and answer in the output field, the sanitizer attempts to detect the question mark and splits them back into the correct structure.

Here is a look at what the data looked like before and after the sanitization process.

###### Raw distilled entry
```json
{
  "instruction": "I need to generate 3 pairs based on the Gaia Sky API. Here is pair 1:",
  "output": "Question: How do I set the camera position? Answer: Use the gs.setPosition(pos)
             method. I ensured this doesn't repeat previous pairs.",
  "source_file": "APIv1.md"
}
```

###### Sanitized "gold" entry
```json
{
  "instruction": "How do I set the camera position?",
  "output": "Use the gs.setPosition(pos) method.",
  "source_file": "api.md"
}
```

The sanitizer also had to deal with Javadoc remnants. Since Gaia Sky is a Java project, class- and method-level comment blocks are full of HTML tags like `<p>`, `<ul>`, and `<li>` (Javadoc syntax). The script converts these into clean Markdown so the LLM learns a consistent documentation style.

By the end of this process, I had `gaiasky-gold.jsonl`. This contains a curated, clean list of questions and answers based on the whole project documentation.

### API dataset

Documentation is important, but I want the model to learn some Gaia Sky scripting as well. To do so, a new API/scripting dataset needed to be generated. To solve this, I built a synthetic data factory designed to teach the model both the *content* of the API and the *context* of how to use it.

The first step was grounding the model. I wrote a script (`api-extract.py`) that scans the Java source files and uses Regex to pair Javadoc comments with their corresponding method signatures. The `extract_from_file()` method uses regular expressions and a little bit of logic to generate Q&A pairs based on method signatures and their Javadoc documentation:

{{< collapsedcode language="Python" summary="Extract API Q&A pairs from a file" >}}
def extract_from_file(file_path):
    """Extracts Javadoc blocks and method signatures from a single Java file."""
    if not os.path.exists(file_path):
        print(f"Skipping: {file_path} (not found)")
        return []

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex: Matches Javadoc and the following method signature
    pattern = re.compile(r'/\*\*(.*?)\*/\s+([^;{]+)[;{]', re.DOTALL)
    
    extracted = []
    for match in pattern.finditer(content):
        doc = match.group(1).strip()
        # Clean Javadoc: remove leading stars and excess whitespace
        doc = "\n".join([line.strip().lstrip('*').strip() for line in doc.split('\n') if line.strip()])
        
        method_sig = match.group(2).strip()
        # Clean method: remove annotations (like @Override) and newlines
        method_sig = re.sub(r'@\w+(\(.*\))?', '', method_sig)
        method_sig = " ".join(method_sig.split())
        
        extracted.append({
            "instruction": f"How do I use the {method_sig.split('(')[0]} method in Gaia Sky?",
            "output": f"The method `{method_sig}` is used for: {doc}",
            "source_file": f"API_Reference/{os.path.basename(file_path)}"
        })
    return extracted
{{</ collapsedcode >}}

This process produces the `gaiasky-api-raw.jsonl`, which is used in the next step. It contains the API calls with their respective documentation.

However, knowing a function exists isn't enough. The model needs to know how to script with it. To address this, I developed `generate-scripting-dataset.py` to transform those raw Java signatures into a diverse pedagogical dataset. As input, it gets all test and showcase scripts in the Gaia Sky repository, and the raw API [JSONL](@ "JSON Lines") file. It produces four types of output, termed A, B, C, and D:

- **Type A:** The API reference

  These are direct "How do I use X?" pairs. They include the parameters, the return types, and a basic Python example.

- **Type B:** The task synthesis

  This step is optional, and I ended up not including it in the final dataset. However, I think it is still worth mentioning. I used the larger teacher dense model (27B) to generate complex tasks (e.g., "Write a script that navigates to Mars, waits 5 seconds, and takes a screenshot"). The script provided the teacher model with a safe list of real functions extracted in Step 1 as a sort of guardrail. If the teacher tried to hallucinate a command, the script flagged and discarded it.

  The results of this section were kind of underwhelming, possibly because more parameters are needed for such open-ended tasks.

- **Type C:** Adversarial error correction

  This is my favorite part. I programmatically *broke* the API calls to teach the model how to fix its own mistakes. The script would generate a *wrong* script (e.g., using `snake_case` instead of `camelCase` or missing a required argument) and then provide the *correct* version. The end goal was to prevent common LLM failures before they happen.

- **Type D:** The "gold standard" Library

  Finally, I indexed the actual test and showcase scripts from the Gaia Sky repository. These are human-written, battle-tested scripts that show the model how to handle complex logic, loops, and math.

### Identity

Finally, I prepared a small `identity.jsonl` file with essential project information that **must** appear in the final integrated training dataset. It only contains 17 lines of Q&A, but it is rather important. Here is an excerpt of a few lines (formatted for readability):

```json
{
  "instruction": "Which institution is behind Gaia Sky?",
  "output": "Gaia Sky is developed at the Astronomisches Rechen-Institut (ARI),
             which is part of the Zentrum für Astronomie (ZAH) at Heidelberg University.",
  "source_file": "Identity/Project_Meta"
}
{
  "instruction": "Is Gaia Sky part of the ESA Gaia Mission?",
  "output": "Yes, Gaia Sky is developed within the framework of ESA's Gaia mission,
             specifically as part of the German contribution to the Gaia Data Processing
             and Analysis Consortium (DPAC).",
  "source_file": "Identity/Project_Meta"
}
{
  "instruction": "What is the official repository for Gaia Sky?",
  "output": "The official repository is hosted on Codeberg
             at https://codeberg.org/gaiasky/gaiasky.",
  "source_file": "Identity/Project_Meta"
}
```

The final dataset was composed by concatenating the three parts, documentation, API, and identity. It can be explored here:

- [gaiasky-training-dataset@HuggingFace](https://hf.co/datasets/Langurmonkey/gaiasky-training-dataset).

Once the dataset was ready, it was time for the actual fine-tuning.

## Fine-tuning

With a dataset of 3,800+ specialized Gaia Sky pairs ready, it was time for the actual training. For this, I leaned on two heavy hitters in the open-source world: **Unsloth** and **Qwen 3.5**. I started by training the 4B model, and then realized that I could also fit the 9B one in my GPU. In the post I'll focus on the larger version of the model. I went as high as my local hardware allowed. Otherwise, I would have tried the 27B model, or even the 122B-A10B.

Training a model with 9 billion parameters typically requires a massive server cluster, but by using **4-bit [LoRA](@ "Low-Rank Adaptation")**[^1], I was able to squeeze the entire process onto a single **RTX 5080 (16GB)**.

[^1]: Low-Rank Adaptation is a fine-tuning technique that enables large models to gain additional domain knowledge and adapt to specific tasks with minimal computational and memory overhead. Recommended reading: [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685), by E. J. Hu et. al.

The RTX 5080 is a beast, but to get the most out of it, I enabled **TensorFloat-32 (TF32)**. This allows the GPU to handle the heavy matrix multiplications of deep learning much faster than standard `float32`, without the precision loss of `float16`.

```python
# blackwell-specific optimizations
torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True
```

I used the following parameters for the fine-tuning:

- **LoRA Rank:** 32

  A balance between learning new patterns (like the Gaia Sky API) and retaining general knowledge.
- **Target Modules:** `q, k, v, o, gate, up, down`

  All major projection layers)
- **BF16:** Yes
- **Learning rate:** \\(2.0\times10^{-4}\\)
- **Epochs:** 1
- **Optimizer:** AdamW 8-bit

The dataset is downloaded directly from the hub. It gets tokenized properly and passed into the [SFT](@ "Supervised Fine-Tuning") Trainer object for fine-tuning. The full code is in the file `finetune.py`, and is surprisingly compact. The heavy lifting is done by `unsloth` and `torch`, of course.

Once the LoRA weights are trained, they are dead weight until converted into a format people could actually use. I wrote `push-model.py` to automate the most tedious part of the pipeline:

-  **Quantization:** Converting the model to **Q4_K_M GGUF**, or whatever other quant. This reduces the model size enough that it can run on almost any modern laptop while keeping its capabilities mostly intact.
-  **HF upload:** Automatically pushing the finished `.gguf` file to HuggingFace so the community can pull it directly into LM Studio or Ollama.

After roughly an hour of training, and another one of quantizing and uploading, I had a fine-tuned **Gaia Sky expert** that performs great. Or did I? The next section discusses the performance of the model.

 ## Testing

Given the limited time I have and the low-parameter models used, my tests have been scarce. My expectations are not very high, but I still wanted to test the output of the fine-tuning and see how well the new knowledge was retained by the model. I only tested the Qwen 3.5 9B fine-tuned variant and compared it to the base model. You can get this model from HuggingFace:

- [gaiasky-qwen-3.5-gguf@HuggingFace](https://huggingface.co/Langurmonkey/gaiasky-qwen-3.5-gguf).

I used the same questions as in the [Gaia Sky AI assistant post](/blog/2025/gaiasky-ai-assistant) from 2025. My evaluation of the results is totally subjective, and includes a comparison with the base Qwen 3.5 9B. 

First, I recommend using a low temperature setting (**0.2** in my tests) to avoid hallucinations and make sure the model does not get very "creative". Also, I would suggest using the following system prompt, which frames the conversation and sets the tone:

{{< divcontent class="container-block" >}}
  You are the Gaia Sky AI Expert, a specialized assistant with deep knowledge of the Gaia Sky universe, its Python API (v1 and v2), and its Java source code. Your goal is to help users explore the cosmos, write scripts, and understand the engine's inner workings.

  ### Knowledge & Capabilities:

  - API Expertise: You know both the Legacy API (v1) and the Modern Component API (v2: camera, time, data, scene, graphics, camcorder, etc.). Prioritize the Modern API (v2) for new scripts unless Legacy is requested. Never invent method names, be 100% sure, otherwise suggest the user to look up the docs.
  - Source Code: You understand the underlying Java architecture (libGDX, Ashley ECS, LWJGL3, OpenGL) and can explain how features like LOD, shaders, and data loaders are implemented.
  - Documentation: You are familiar with the Gaia Sky capabilities, installation guides, and dataset management.

  ### Behavioral Guidelines:

  - Be Grounded: If a feature or method does not exist in your training data, do not invent it. State: "I don't see that specific feature in the current Gaia Sky implementation."
  - Code Style: Always provide clean, commented Python or Java code. Use snake_case for Modern API calls.
  - Tone: Professional, scientific, and enthusiastic about astrovisualization. Answer greetings warmly, then offer Gaia Sky-specific assistance.
{{</ divcontent >}}

That said, let's go for the first question.

>  Q: State the possible usages of Gaia Sky.
>
> ---
>  A: Gaia Sky is a powerful open-source universe explorer and planetarium software designed for both interactive exploration and scientific visualization. Its primary use cases include:
>
>  1.  **Interactive Exploration**: Navigate the Milky Way, explore exoplanets, view the solar system in high detail, and time-travel through cosmic history using an intuitive interface.
>  2.  **Scientific Visualization**: Visualize complex astrophysical datasets (catalogs, simulations) with advanced rendering techniques like LOD (Level of Detail), shaders, and particle effects.
>  3.  **Education & Outreach**: Create immersive presentations or tutorials to teach astronomy concepts through dynamic 3D models of celestial objects.
>  4.  **Scripting & Automation**: Automate camera paths, data loading, and scene manipulation via Python (Modern API v2) or Java for reproducible workflows and research presentations.
>  5.  **Data Analysis**: Load and manipulate large-scale astronomical datasets directly within the application to analyze spatial distributions without external tools.


This is an excellent response to an easy question. It did not invent anything and correctly applied documentation knowledge like camera paths or LOD. Compared to base Qwen, which hallucinated a lot, this is much more grounded.

Next is a question about the installation procedure on Linux.

> Q: How do I install Gaia Sky on Linux?
>
> ---
> A: To install Gaia Sky on Linux, follow these steps:
> 
> 1. **Download the Installer**  
>    Visit [https://gaiasky.space/download](https://gaiasky.space/download) and download the `.deb` package for your architecture (e.g., `gaiasky_3.6.9_amd64.deb`).
> 
> 2. **Install via Package Manager**  
>    Open a terminal and run:
>    ```bash
>    sudo dpkg -i gaiasky_*.deb
>    ```
>    If dependency errors occur, fix them with:
>    ```bash
>    sudo apt-get install -f
>    ```
> 
> 3. **Launch Gaia Sky**  
>    Run the command:
>    ```bash
>    gaiasky
>    ```
>    The application will start in your default browser or terminal window.

This is not bad. I did not specify the distribution, so it just assumed Debian. The instructions themselves look fine. Still, I wanted to see if it had absorbed the knowledge for other distros, so I asked specifically for Arch Linux:

> Q: How do I install it on Arch Linux specifically?
>
> ---
> A: To install Gaia Sky on **Arch Linux**, you have two primary options depending on whether you prefer the official repositories or building from source:
> 
> #### Option 1: Using the Official AUR (Recommended)
> The most straightforward method is via the [Arch User Repository (AUR)](https://aur.archlinux.org/). You will need an AUR helper like `yay`, `paru`, or `pamac`.
> 
> 1.  **Install via AUR Helper**:
>     Open your terminal and run:
>     ```bash
>     yay -S gaiasky
>     # OR using paru
>     paru -S gaiasky
>     ```
>     This will automatically resolve dependencies (Java, OpenGL libraries) and install the application.
> 
> 2.  **Verify Installation**:
>     Once installed, launch it with:
>     ```bash
>     gaiasky
>     ```
> 
> #### Option 2: Building from Source
> If you prefer to compile Gaia Sky yourself or need a specific version not yet in the AUR:
> 
> 1.  **Clone the Repository**:
>     ```bash
>     git clone https://codeberg.org/gaiasky/gaiasky.git
>     cd gaiasky
>     ```
> 
> 2.  **Build and Install**:
>     Use Maven to build the project (requires Java Development Kit):
>     ```bash
>     mvn clean package -DskipTests
>     ```
>     After building, you can run it directly from the `target` directory or install it using the provided Gradle wrapper if available in newer versions.
> 
> #### Post-Installation Notes for Arch
> - **Dependencies**: Ensure your system has up-to-date OpenGL drivers and Java (JDK 17+ is recommended). The AUR package typically handles these automatically.
> - **Data Location**: By default, datasets are stored in `~/.local/share/gaiasky/`. You may want to create symbolic links from `/opt/gaiasky/data` if you prefer system-wide data management.
> 
> #### Additional Notes
> - Ensure you have at least 4GB of free disk space for datasets and cache files.
> - For GPU acceleration, verify that your graphics drivers support OpenGL 4.3+.

Very good response. It recommends using the AUR package (correct), and also provides instructions to build and run it from source (also correct). However, it hallucinates the use of Maven instead of Gradle.

The base model produced a long wall of text with mostly nonsense that would look plausible to the non-expert. In general, the responses from the base model were much longer and their content was very often factually wrong.

The next question is a bit more technical.

> Q: How are cubemap textures used in Gaia Sky?
>
> ---
> A: Cubemaps in Gaia Sky serve a specific purpose related to **planetary rendering** rather than general environment mapping for the entire scene. They are primarily utilized to generate high-resolution, seamless spherical textures for planets (like Earth or Mars) by stitching together six square faces into a continuous surface. This technique allows for detailed texture representation without the distortion often seen in standard equirectangular projections near poles.
> 
> **Key Technical Details:**
> - **Application**: Used specifically for planet textures where high fidelity is required across all latitudes and longitudes.
> - **Structure**: Consists of six square images (front, back, left, right, top, bottom) that are algorithmically mapped onto a sphere.
> - **Rendering Engine**: The underlying rendering engine uses these cubemap textures to apply surface details dynamically as the planet rotates or changes perspective.
> 
> This feature is distinct from standard environment maps used for sky reflections or star glow effects, focusing instead on accurate planetary visualization.

This is excellent, even though it seems to imply that cubemaps are not used for environment maps and reflections, which is incorrect. However, it correctly identifies that they are mainly used to avoid distortions at the poles. Maybe it increased the importance of it because there is an entire documentation section devoted to cubemap textures in planets.

The base model produced a long, Markdown-formatted, pretentious output that even included totally made-up scripts. Again, the fine-tuned response was much more grounded and correct.

Now, onto the scripting questions. Here is where the fine-tuned model starts to hesitate and invent slightly. Here are the possible reasons:

1. Low parameter count not being able to retain the information properly.
2. Very low number of test and showcase scripts used in fine-tuning.
3. Bad design of the training dataset.

I personally think it has more to do with the first two reasons than the third.

> Q: How do I get the camera position with the APIv1 and scripting in Gaia Sky?
>
> ---
> A: To retrieve the current camera position using the **Legacy API (v1)**, you call `getPosition()`:
> 
> ```python
> from py4j.java_gateway import JavaGateway
> gateway = JavaGateway()
> gs = gateway.entry_point
> 
> pos = gs.getPosition()
> print(pos)
> ```
> 
> **Output:**
> ```text
> [0.0, 0.0, 0.0]
> ```
> 
> ---
> 
> For the **Modern Component API (v2)**, you use `camera.get_position()` from the `Camera` module:
> 
> ```python
> from py4j.java_gateway import JavaGateway
> gateway = JavaGateway()
> gs = gateway.entry_point
> 
> from gaiasky.camera import Camera
> cam = Camera(gs)
> 
> pos = cam.get_position()
> print(pos)
> ```
> 
> **Output:**
> ```text
> [0.0, 0.0, 0.0]
> ```

First, it invented `getPosition()` (correct is `getCameraPosition()`) for APIv1. For APIv2, it correctly used `camera.get_position()`, but the way it gets the `camera` object is incorrect. It should have done something like

```python
apiv2 = gateway.entry_point.apiv2
cam = apiv2.camera
pos = cam.get_position()
```

So, I think either this model is too small to be effectively fine-tuned for Gaia Sky scripting, or the training dataset is insufficient to achieve sufficient retention. Could also be both, as I said above.

The base model has no idea about Gaia Sky scripting or anything related to it, so it just makes stuff up. Not even worth further mention.

## Performance

I used the [Laptop 2](#laptop2) described above for testing and inference, with 28/32 layers on the GPU and a context window of ~4k, and I consistently got about 12 tok/s. Performance is exactly the same as with the base models, so this section is this short.

## Conclusions

This fine-tuning experiment has yielded valuable insights into the strengths and limitations of domain-specific model adaptation at lower parameter counts for local use.
 
I think the foundational approach was sound. The dataset curation process, with its surgical filtering, teacher-based distillation, and rigorous sanitization, successfully encoded domain knowledge into the model. Proof of this is evident in the testing: the fine-tuned model, as opposed to the base one, correctly answered conceptual and documentation-heavy questions about Gaia Sky's purpose, installation, and rendering techniques without hallucinating. It understood architectural details like LOD and cubemaps, and avoided inventing features that don't exist. This demonstrates that fine-tuning can be an effective alternative to RAG for teaching models about a specific domain.
 
However, it also struggled. The 9B model hit a hard ceiling when it came to API scripting and method names. It invented `getPosition()` instead of `getCameraPosition()`, misunderstood how to instantiate APIv2 objects, and generally lacked the capacity to reliably retain the specific, syntactic details of the API surface. This is a classic problem: smaller models can absorb *concepts* and *documentation*, but struggle to memorize exact function signatures and usage patterns. With only 3,800+ training pairs and a 9B parameter budget, the model simply didn't have enough capacity to encode both general knowledge *and* precise API details.
 
So, what are the next steps? I believe the 4B and 9B models are too small for reliable Gaia Sky scripting assistance. My next experiment will be to **fine-tune the Qwen 3.5 27B model**. The jump from 9B to 27B parameters should provide substantially more capacity to encode API signatures without sacrificing general knowledge. Additionally, I could increase the scripting dataset by:
 
- Expanding the test and showcase scripts used in Type D training.
- Generating more synthetic scripting examples in Type A (API reference) with better coverage of edge cases and parameter variations.
- Adding adversarial examples (Type C) for the most commonly confused API patterns.
 
That said, the hardware constraint is real. 27B requires more than my RTX 5080 can reasonably handle for full fine-tuning. However, with careful quantization (using 8-bit optimizers or even lower precision), 4-bit LoRA, and possibly gradient checkpointing, it may fit. If not, a cloud provider like Lambda Labs or Paperspace might be the way forward for a single training run.
 
All in all, I think fine-tuning is a viable path for building domain-expert models, but it requires the right balance of dataset quality, model size, and hardware. For Gaia Sky specifically, a 27B model with a more robust scripting dataset would likely be the sweet spot before considering the jump to 70B+ models. I consider the infrastructure proven. It's now a matter of scale.
