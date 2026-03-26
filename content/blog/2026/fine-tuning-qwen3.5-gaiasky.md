+++
author = "Toni Sagristà Sellés"
title = "Fine-tuning Qwen3.5 for Gaia Sky"
description = "How I fine-tuned Qwen3.5 4/9B models to become Gaia Sky experts"
date = 2029-03-24
categories = ["AI"]
tags = ["LLM", "AI", "LM Studio", "fine-tuning", "AI inference", "unsloth"]
featuredpath = "date"
type = "post"
+++ 

Some time ago I set up a [local pipeline](/blog/2025/local-llm-rag) to use different [LLM](@ "Large Language Model")s to [respond to Gaia Sky questions](/blog/2025/gaiasky-ai-assisstant) using [RAG](@ "Retrieval Augmented Generation"). In that post, I built a dynamic scrapper that parsed the Gaia Sky website and documentation and ingested the content it into a vector database. Then, I built a minimal chatbot interface that received the user prompt, queried the database for semantically similar data, and built up the context for each LLM call. The results were promising, and I found that they strongly depended on the model.

Fast forward a few months and the Qwen 3.5 models were released by Alibaba. The general consensus is that they are quite good for their size, and I've been testing them for local inference with a similar impression. I thought that it would be interesting to repeat the exercise of creating a Gaia Sky AI assistant, but using a radically different approach: Instead of RAG, I would **fine-tune the model** itself. In this post, I describe this fine-tuning project, from the creation and engineering of the training dataset to the fine-tuning and production of the final GGUF models.

<!--more-->

## Links

- Dataset creation and fine-tuning -- <i class="fa fa-gitea" aria-hidden="true" title="Codeberg"></i> [gaiasky-finetune](https://codeberg.org/gaiasky/gaiasky-finetune)
- Gaia Sky training dataset repository -- <i class="fa fa-git-square" aria-hidden="true" title="Codeberg"></i> [gaiasky-training-dataset](https://hf.co/Langurmonkey/gaiasky-training-dataset)
- Qwen3.5 Gaia Sky fine-tuned models -- <i class="fa fa-git-square" aria-hidden="true" title="Codeberg"></i> [gaiasky-qwen-3.5-gguf](https://hf.co/Langurmonkey/gaiasky-qwen-3.5-gguf)

## Hardware

Here is the hardware I have used to distill the dataset and fine-tune the model:

- **Desktop PC** -- Arch Linux, Intel(R) Core(TM) i7-7700 (8) @ 4.20 GHz, 32 GB RAM, NVIDIA GeForce GTX 1070 8 GB.
- **Laptop** -- Windows 11, WSL2 (Arch Linux), Intel(R) Core(TM) Ultra 9 275HX (24) @ @ 3.07 GHz, 32 GB RAM, NVIDIA GeForce RTX 5080 Laptop 16 GB.

## Quality over quantity

When I started this project, my first instinct was "more is better." I thought that if I fed the model every single `.java`, `.glsl`, `.rst`, and `.md` file in the Gaia Sky repositories (project, documentation, etc.), it would emerge as an expert. Oh boy, was I wrong. 

A large codebase contains a lot of "boilerplate noise". Getters, setters, and infrastructure code that doesn't actually help a model understand *how* the engine works or *how* to write scripts for it. I soon realized that the dataset is the single most important part of the project, and it needed a surgical approach.

### Base extraction
I wrote `generate-raw-dataset.py` to act as a high-pass filter. Instead of a blind crawl, I implemented an **allowlist** system. I would only let in the load-bearing files:
* **Core Logic:** The brain of the engine (main loop, scene, renderer, etc.).
* **Visual Logic:** The shaders that define the look of the cosmos (stars, particles, PBR, etc.).
* **Documentation:** All the existing Markdown and reStructuredText files.

One technical hurdle was that Gaia Sky’s documentation was written in `.rst` (reStructuredText), while LLMs seem to be much *happier* with Markdown. I integrated `pandoc` directly into the extraction pipeline to convert these on the fly:

```python
def convert_rst_to_md(rst_content):
    """Use pandoc to pipe the RST content and get Markdown back"""
    try:
        process = subprocess.Popen(
            ['pandoc', '-f', 'rst', '-t', 'gfm', '--wrap=none'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=rst_content)
        # ... cleaning logic ...
        return stdout.strip()
    except FileNotFoundError:
        return rst_content
```

Every source file in Gaia Sky starts with a significant copyright header. While important for licensing, this is "dead weight" for training. I added a regex-based stripper to ensure the model's limited context window was filled with code logic, not license text:

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

Once I had a clean extraction of the Gaia Sky codebase, I faced a new problem. A raw dump of a `Coordinates.java` file is great for a search engine, but it is not a conversation. To turn these files into training data, I used a "Teacher" model, Qwen 3.5 27B, to look at each file and generate a specific number of Q&A pairs. I wrote `distill-dataset.py` to handle this. The script calculates how many questions a file is worth based on its length and type. A long documentation file might get 25 pairs, while a short shader might only get 4. 

The prompt was possibly the most delicate part. I had to tell the model exactly how to behave:
* **Match the answer type:** If the question doesn't ask for code, don't provide it.
* **Grounding:** Every claim must be directly in the source text.
* **Diversity:** Every question must cover a different detail.

To prevent the model from repeating itself across batches, I tracked existing questions and fed them back into the prompt as "exclusions."

```python
# A snippet from the distillation prompt
prompt = (
    f"You are a Gaia Sky technical expert. {file_hint}\n"
    f"Generate exactly {current_target} Q&A pairs strictly based on the source text below. "
    f"{avoid_context}\n"
    "Format the output as JSONL... Output ONLY the JSONL, nothing else."
)
```

LLMs are chatty. Even with such strict instructions, these low-parameter models sometimes mess up. I quickly discovered that the teacher model would sometimes leak its own reasoning into the output. It would start its response with `"The user asked to provide 34 Q&A pairs given the source material..."` or it would include meta-talk like `"This question is safe because it is derived from line 45."`

This created "dirty" data that polluted the dataset and undermined the fine-tuning process. If I trained on this, the final model would start every answer by talking to itself.

To fix this, I built `sanitize-jsonl.py`. This script is a heavy-duty cleaner that uses regex to strip out training artifacts. It first tries to rescue bad rows, and if it fails, it deletes them. If the model accidentally put both the question and answer in the "output" field, the sanitizer attempts to detect the question mark and splits them back into the correct structure.

Here is a look at what the data looked like before and after the "Monologue Killer" got to it.

**Raw distilled entry:**
```json
{
  "instruction": "I need to generate 3 pairs based on the Gaia Sky API. Here is pair 1:",
  "output": "Question: How do I set the camera position? Answer: Use the gs.setPosition(pos) method. I ensured this doesn't repeat previous pairs.",
  "source_file": "APIv1.md"
}
```

**Sanitized "gold" entry:**
```json
{
  "instruction": "How do I set the camera position?",
  "output": "Use the gs.setPosition(pos) method.",
  "source_file": "api.md"
}
```

The sanitizer also had to deal with Javadoc remnants. Since Gaia Sky is a Java project, the source is full of HTML tags like `<p>`, `<ul>`, and `<li>` coming from Javadocs. The script converts these into clean Markdown so the LLM learns a consistent documentation style.

By the end of this process, I had `gaiasky-gold.jsonl`. This contains a curated, clean list of questions and answers based on the whole project documentation.

## Bridging the language barrier

The biggest hurdle in fine-tuning a model for a niche project like Gaia Sky is the language mismatch. Gaia Sky is a GLSL/Java project at its core, but its users and automation enthusiasts speak **Python** (via the Py4J bridge). If you simply feed a model the Java source code, it will try to write Java. If you feed it general Python, it won't know the specific method names.

To solve this, I built a synthetic data factory designed to teach the model both the *content* of the API and the *context* of how to use it.


### Raw extraction
The first step was grounding the model. I wrote a script (`api-extract.py`) that scans the Java source files and uses Regex to pair Javadoc comments with their corresponding method signatures.

```python
# Regex: Matches Javadoc (Group 1) and the following Method Signature (Group 2)
pattern = re.compile(r'/\*\*(.*?)\*/\s+([^;{]+)[;{]', re.DOTALL)
```
This produced a raw "dictionary" of every possible command in Gaia Sky, ensuring the model never had to guess if a function like `goToObject()` existed, as it saw the source code proof.

### Four pillars of training
Knowing a function exists isn't enough; the model needs to know how to script with it. I developed `generate-scripting-dataset.py` to transform those raw Java signatures into a diverse pedagogical dataset:

- Type A: the API reference (mapping)
  These are direct "How do I use X?" pairs. They include the parameters, the return types, and a basic Python example.

- Type B: the task synthesis (reasoning)
  I used a larger "Teacher" model (Qwen 27B) to generate complex tasks (e.g., "Write a script that navigates to Mars, waits 5 seconds, and takes a screenshot").

  The Guardrail: The script provided the Teacher model with a "Safe List" of real functions extracted in Step 1. If the Teacher tried to hallucinate a command, the script flagged and discarded it.

- Type C: Adversarial Error Correction (Vaccination)
  This is my favorite part. I programmatically "broke" the API calls to teach the model how to fix its own mistakes. The script would generate a "Wrong" script (e.g., using snake_case instead of camelCase or missing a required argument) and then provide the "Correct" version.

  Goal: Prevent common LLM failures before they happen.

- Type D: The "Gold Standard" Library
  Finally, I indexed the actual assets/scripts folder from the Gaia Sky repository. These are human-written, battle-tested scripts that show the model how to handle complex logic, loops, and math.

### Handling the Py4J boilerplate
One of the most annoying parts of Gaia Sky scripting for a beginner is the setup code:

```python
from py4j.java_gateway import JavaGateway
gateway = JavaGateway()
gs = gateway.entry_point
```
 
By including this boilerplate in 50% of the training data and omitting it in the other 50%, I trained the model to be context-aware. It can now write a complete, runnable .py file from scratch, or just give you the specific `gs.method()` line you need for an existing project.


## Fine-tuning

With a dataset of 2,500+ specialized Gaia Sky pairs ready, it was time for the actual training. For this, I leaned on two heavy hitters in the open-source world: **Unsloth** and **Qwen 3.5**.

Training a model with 9 billion parameters typically requires a massive server cluster, but by using **4-bit LoRA (Low-Rank Adaptation)**, I was able to squeeze the entire process onto a single **RTX 5080 (16GB)**.

### Hardware optimization: Blackwell & TF32
The RTX 5080 is a beast, but to get the most out of it, I enabled **TensorFloat-32 (TF32)**. This allows the GPU to handle the heavy matrix multiplications of deep learning much faster than standard `float32`, without the precision loss of `float16`.

```python
# blackwell-specific optimizations
torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True
```

### The training recipe (`finetune.py`)
I chose **Qwen 3.5 (9B)** as the base model because of its incredible performance-to-size ratio. Using the Unsloth library, the training was surprisingly efficient:

* **LoRA Rank (r=32):** A balance between learning new patterns (like the Gaia Sky API) and retaining general knowledge.
* **Target Modules:** I targeted all major projection layers (`q, k, v, o, gate, up, down`) to ensure the model's "scripting brain" was fully rewired.
* **Speed:** Thanks to Unsloth's kernels, the model loaded in seconds and trained significantly faster than standard HuggingFace implementations.


### GGUF export
Once the LoRA weights were trained, they were "dead weight" until converted into a format people could actually use. I wrote `push-model.py` to automate the most tedious part of the pipeline:

1.  **Quantization:** Converting the model to **Q4_K_M GGUF**. This reduces the model size enough that it can run on almost any modern laptop while keeping the intelligence intact.
2.  **The "Boilerplate" Injection:** Ensuring the tokenizer correctly handles the `<|im_start|>` and `<|im_end|>` tags for smooth chat interactions.
3.  **HF Upload:** Automatically pushing the finished `.gguf` file to HuggingFace so the community can pull it directly into LM Studio or Ollama.

### Output
After roughly an hour of training, I had a specialized **Gaia Sky Expert**. In the next part, we'll see the payoff: testing the model's "Cosmic IQ" and seeing if it can actually write a cinematic tour of the solar system.


 
## Dataset creation

I have learned that the dataset used is the single most important part by far.

Explain the history: First I included all files (all Java/GLSL/Python source code, documentation, markdown, etc.) in the distillation process. Then I decided to only include the most important source code files, but all docs and some markdown files (readme, etc.). The API/scripting dataset is generated with a custom script.

### Documentation dataset

- Creation of base dataset from source files. `generate-raw-dataset.py`: "This script crawls Gaia Sky source directories to create a structured JSONL dataset for LLM fine-tuning. It captures logic, documentation, and shaders to help the model understand the engine's inner workings."
- Distillation by Qwen 3.5 27B. A self-instruct distiller script tells the model to generate Q&A pairs from the output of `generate-raw-dataset.py`. The distiller is in `distill-dataset.py`.
- Sanitization by stripping HTML tags, ChatML/LLama-3 tokens, meta-prompts, etc. This is in `sanitize-jsonl.py`:
  ```
   Gaia Sky Dataset Sanitizer
   -------------------------
   Cleans synthetic Q&A pairs by removing training artifacts and 
   fixing structural errors in distilled JSONL data.

   Specifically:
   - Strips Javadoc HTML tags (<p>, <ul>, <li>, <strong>, etc.)
   - Strips ChatML/Llama-3 tokens (<|start_header_id|>, <|eot_id|>, etc.)
   - Splits multi-part answers into individual training samples
   - Repairs swapped instruction/output fields
   - Promotes orphaned questions to the instruction field
   - Strips meta-prompts and Q&A markers (Q:, A:, <QUESTION>)
   - Handles "Extract a Q&A pair" patterns
   - Filters out empty or low-utility entries
  ``` 

 This produces `gaiasky-gold.jsonl`.

 ### Identity

 Handcrafted dataset with important data on the project like authors, URLs, and some basic knowledge.

 This is `identity.jsonl`.

 ### API/scripting dataset

 First, we generate the raw API dataset with `api-extract.py`. This parses and extracts javadoc comments from source files, and produces `gaiasky-api-raw.jsonl`. Then, we use `generate-scripting-dataset.py` to generate a custom dataset from the API and other stuff.

 This produces `gaiasky-scripting.jsonl`.

 ### Final dataset

 We concat the previous `jsonl` products into the final dataset. With that, we create the training dataset, published in HF.

 ## Fine-tuning

 Here we comment on the fine-tuning process. The file is `finetune.py`. Uses the HF dataset and a Qwen 3.5 model (usually an unsloth-produced quant) to produce a fine-tuned version.

 Then, `push-model.py` pushes the resulting GGUFs to HF.

 ## Testing

 To be done. I have some saved conversations.

 ## Conclusions

 Here the conclusions.
