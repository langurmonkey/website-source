+++
author = "Toni Sagrista Selles"
categories = ["AI"]
tags = ["LLM", "AI", "ollama", "RAG"]
date = 2025-03-26
linktitle = ""
title = "Building a local AI assistant with user context"
description = "We use Ollama and Chroma DB to build a personalized assistant from scraped web content"
featuredpath = "date"
type = "post"
+++

In my last [post](/blog/2025/local-llm-rag), I explored the concept of Retrieval-Augmented Generation (RAG). It enabled a locally running generative AI model to access and incorporate new information, that was later accessed during inference. To achieve this, I used hardcoded documents as context, which were then embedded as vectors and sent into Chroma DB. The data were finally retrieved for context when using the chatbot.
But using a few sentences hardcoded strings is not very elegant or particularly exciting. It's alright for educational purposes, but that's it. However, if we need to build a *minimally useful system*, we need to be more sophisticated than this. In this new post, I set out to create a local Gaia Sky assistant by feeding Chroma DB with the official [Gaia Sky documentation](http://docs.gaiasky.space) and [our homepage](https://gaiasky.space), and leveraging Ollama to generate context-aware responses. So, let’s dive into the code and explain how it all works.

The source code used in this post is available [here](https://codeberg.org/langurmonkey/gaiasky-ai).

<!--more-->

## Scraping the Websites

The first thing we need to do is extract useful content from the web. This is where web scraping comes into play:

- We’re using the `requests` library to fetch the HTML content from a given URL.

- First, we get all the internal links for every URL by recursively scraping the content (with `BeautifulSoup`) and looking for all `a` tags (anchors) that don't point to internal anchors. This happens in `get_all_doc_links(base_url)`.

- Then, we extract the text from every page by extracting the tags `h1`, `h2`, `h3`, `h4`, `h5`, `p`, `li`, `td`, and `article`. This step required a little bit of trial and error. Once we have the text for each page, we concatenate everything and return it. This is implemented mostly in `extract_text_from_page(url)`.

- As we mentioned earlier, we make sure to avoid non-HTML files and internal page anchors (those pesky # URLs that only point to a specific section). This ensures that we only scrape actual web pages that contain relevant data.

With this method, we capture all the relevant documentation — every corner of the site. Since the process is recursive, we don’t miss any pages (unless they’re blocked or have weird redirect loops, but that's a discussion for another time).

Below is the relevant code.

```python
import os

# Set user agent enviornment variable
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
os.environ["USER_AGENT"] = user_agent

import requests, ollama, argparse, readline
from termcolor import colored
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from langchain_community.document_loaders import WebBaseLoader
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings

headers = {
    "User-Agent": user_agent
}

def get_all_doc_links(base_url):
    """Finds all internal links within the documentation site."""
    visited = set()
    to_visit = {base_url}

    while to_visit:
        url = to_visit.pop()
        print(f"Scraping {colored(url, 'blue')}")
        if url in visited:
            continue
        visited.add(url)

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.find_all("a", href=True):
            full_url = urljoin(base_url, link["href"])
            parsed = urlparse(full_url)

            # Ignore anchors (#...) and non-HTML files
            if parsed.fragment or not parsed.path.endswith((".html", "/")):
                continue

            if base_url in full_url and full_url not in visited:
                to_visit.add(full_url)

    return visited

def extract_text_from_page(url):
    """Extracts meaningful text from a given URL."""
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract text from multiple meaningful elements
    content_blocks = []
    for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "p",
                              "li", "td", "article"]):
        text = tag.get_text(strip=True)
        if text:
            content_blocks.append(f" {text} ")
    
    return "\n".join(content_blocks)

def scrape_urls(base_urls):
    """Scrape and extract text content from multiple URLs."""
    all_text = ""
    
    for base_url in base_urls:
        all_links = get_all_doc_links(base_url)
        print(f"Found {len(all_links)} pages to scrape...")
        print(f"Extracting text from pages...")
        for url in all_links:
            page_text = extract_text_from_page(url)
            if page_text:
                all_text += f"\n\n### {url}\n{page_text}"

    return all_text

    # Main body
    urls = ["https://gaia.ari.uni-heidelberg.de/gaiasky/docs/master/",
            "https://gaiasky.space"]

    print("Starting scraping...")
    doc_text = scrape_urls(urls)

```

## Storing Embeddings with ChromaDB
Once we've scraped the content, it’s time to turn that raw text into something that the machine can understand. This is where embeddings come into play.


- We use the `langchain` library to split the scraped text into manageable chunks. This is done using the `RecursiveCharacterTextSplitter`, which splits the content into chunks of a predefined size (to avoid overloading the model). I tuned this by trial and error, and ended up with a chunk size of 1000, and a chunk overlap of 200.

- The text is then passed through an embedding model, specifically the "sentence-transformers/all-MiniLM-L6-v2" model from [HuggingFace](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2), which transforms it into a high-dimensional vector representation. It is super compact and performs well. I have tried other embed models (see commented out lines at the top of [this code block](#code-embed)), but in my experience they did not perform better than `all-MiniLM-L6-v2`.

- Finally, we store these vectors in a vector database, Chroma DB. The vectors are indexed so that when we query the database, it can efficiently retrieve the most relevant pieces of text. For the retrieval, I'm using 5 results (`search_kwargs` in `as_retriever()` method). I tried with 2 and 3, but it seemed that most models didn't get enough context.

This is where the magic happens. By converting text into vectors, we enable the chatbot to compare and understand the semantic meaning of different pieces of text. The advantage here is that embeddings can capture the relationships between words and concepts, even if they’re not an exact match — meaning the chatbot can intelligently pull out relevant context to answer your questions.

The relevant code consists of the concatenated texts we produced in the previous step (we called it `doc_text`), and the location for our disk database:

<a name="code-embed"></a>
```python
embed_model = "sentence-transformers/all-MiniLM-L6-v2"
# embed_model = "BAAI/bge-base-en-v1.5"
# embed_model = "HIT-TMG/KaLM-embedding-multilingual-mini-v1"
# embed_model = "Linq-AI-Research/Linq-Embed-Mistral"

def store_embeddings(texts, db_path):
    """Tokenizes, embeds, and stores the texts in a ChromaDB vector store."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.create_documents([texts])
    if not documents:
        raise ValueError("No documents found to embed. Check the scraper output.")
    
    embeddings = HuggingFaceEmbeddings(model_name=embed_model)
    vector_store = Chroma.from_documents(documents, embeddings, persist_directory=db_path)
    return vector_store

print("Storing embeddings in ChromaDB...")
db_path = "chroma_db"
vector_store = store_embeddings(doc_text, db_path)
```

## Querying with Ollama

Now that we’ve got our indexed data, it’s time to query it. But instead of just returning raw search results, we want to use an LLM (Large Language Model) to generate smart, context-aware answers. Enter Ollama.

- We use `langchain`’s `create_stuff_documents_chain` and `create_retrieval_chain` to first create a chain to retrieve documents from our vector store and pass them on to the model.

- The LLM we’re using is locally hosted through Ollama. The model takes the relevant text retrieved from Chroma and uses that context to generate responses to user queries. The actual model is user-selected at the beginning of the program.

- We use a simple interface where the user can ask questions, and the chatbot pulls from the stored content to generate an answer. If it doesn’t have enough context to answer, it will graciously let you know, but more often than not, it’s ready to impress with its knowledge.

By combining Chroma with an LLM, we ensure that the chatbot not only returns raw text but generates contextually appropriate answers. The power of an LLM with RAG lies in its ability to take a set of relevant documents and provide a coherent, informative response. So, when you ask, “What’s the internal reference system of Gaia Sky?” the chatbot can retrieve the most relevant content and synthesize it into a helpful response.

### System prompt

One of the key elements in ensuring a Retrieval-Augmented Generation (RAG) system behaves as expected is the **system prompt**—a set of initial instructions that guide how the language model responds to queries. In our application, the system prompt is designed to enforce a structured and helpful interaction:

```python
system_prompt = (
    "You are a customer support agent, helping users by following directives and answering questions. "
    "Use the given context to answer the question. "
    "If you don't know the answer, say you don't know. "
    "Keep the answer concise and to the point. "
    "Context: {context}"
)
```

The prompt explicitly states that the LLM is a *customer support agent* to steer its behavior towards professional responses. It also includes a sentence about context awareness so that it actually uses information given in the context. Then, we ask it to not invent something it does not find in the context, and we demand short and concise answers.

By fine-tuning this system prompt, we set clear boundaries for how the model should behave, ensuring it delivers accurate, relevant, and trustworthy responses based on the retrieved knowledge.

### Other parameters

- **Temperature** -- The temperature controls the randomness of the model's responses, with lower values making answers more deterministic and factual, while higher values increase creativity and variability.We use a low temperature value to get more correct and less creative responses.
- **Number of results** -- The number of results parameter (`n_results` or `k`) determines how many relevant documents are retrieved from the vector database to provide context for the model's response, with higher values increasing the available information but potentially adding noise. We use a fine-tuned value of 10.

The relevant code that does the actual querying lives in the `query_with_ollama(vector_store, llm_model)` method. The code below includes the relevant parameters at the top.

```python

system_prompt = (
    "You are a customer support agent, helping users by following directives and answering questions. "
    "Use the given context to answer the question. "
    "If you don't know the answer, say you don't know. "
    "Keep the answer concise and to the point. "
    "Context: {context}"
)
# Number of results to retrieve from the vector store
n_results = 10
# Low temperature to get less creative and more correct responses
temp = 0.3

def query_with_ollama(vector_store, model_name):
    """Uses an Ollama model to retrieve and answer user queries based on stored embeddings."""
    retriever = vector_store.as_retriever(search_kwargs={"k": n_results})
    prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    qa_chain = create_stuff_documents_chain(OllamaLLM(model=model_name, temperature=temp, stream=True), prompt)
    chain = create_retrieval_chain(retriever, qa_chain)
    
    while True:
        query = input(colored("Ask a question (type 'exit' to quit): ", "yellow", attrs=["bold"]))
        if query.lower() in ["exit", "quit", "bye"]:
            break

        for chunk in chain.stream({"input": query}):
            if "answer" in chunk:
                print(chunk["answer"], end="", flush=True)
    
        print("\n")

print("Connecting to Ollama for queries...")
query_with_ollama(vector_store, llm_model)
```
This method contains the context retrieval code and the question-answer loop. The actual **LLM model** to use, stored in `llm_model`, is **user-defined** (code not shown here). After starting, the program presents the available models, and the user needs to select one of them.

## Implementation details

One of the coolest aspects of this setup is the flexibility it provides. You can scrape the website and generate embeddings only when needed by using a command-line flag (`--scrape`). If you’ve already scraped the site and generated embeddings, the system will load the existing embeddings from disk, saving you time and resources. It’s efficient, and you don’t have to redo the work every time you launch the chatbot.

Also, by using `stream=True` in the creation of `OllamaLLM`, and calling `chain.stream()` instead of `chain.query()`, we can stream the response as it is generated, token-by-token.

## Testing

In this section we test the system with [`mistral-small:22b-instruct-2409-q4_K_M`](https://ollama.com/library/mistral-small:22b-instruct-2409-q4_K_M), a small instruct LLM with capabilities comparable to larger models, and with [`llama3.1:8b-instruct-q5_K_M`](https://ollama.com/library/llama3.1:8b-instruct-q5_K_M), a much smaller but better quantized model(Q5-K-M vs Q4-K-M), also specifically trained for instruct.

{{< notice "Note" >}}
You can install these models directly with Ollama:
```
ollama pull mistral-small:22b-instruct-2409-q4_K_M llama3.1:8b-instruct-q5_K_M
```
{{</ notice >}}

Remember, if you want to try out the chatbot yourself, download it from [this repository](https://codeberg.org/langurmonkey/gaiasky-ai).

### Mistral Small 3 instruct, 22B Q4-K-M

Here we use the general [Mistral Small 3 instruct (22B, Q4-K-M)](https://ollama.com/library/mistral-small:22b-instruct-2409-q4_K_M) model. It uses Q4_K_M quantization and features 22.2B parameters. I think this is around the limit of what my computer can handle (see [conclusion](#conclusion)).

On a first pass, we run the program with the `--scrape` flag to gather the information from the websites and create the embeddings. This corresponds to the output shown below, where all the URLs are fetched and scraped.

```bash
$ gsai.py --scrape
Welcome to the Gaia Sky AI assistant! We connect to Ollama to use a local LLM.

Available models:
 [0] mistral-small:22b-instruct-2409-q4_K_M
 [1] llama3.1:8b-instruct-q5_K_M
 [2] gemma3:12b
 [3] qwen2.5:7b
 [4] deepseek-r1:14b
 [5] llama3.1:8b
 [6] mistral-small:24b

Select model (default 0): 0
Using model: mistral-small:22b-instruct-2409-q4_K_M
Embed model: sentence-transformers/all-MiniLM-L6-v2

Starting scraping...
Scraping https://gaia.ari.uni-heidelberg.de/gaiasky/docs/master/
Scraping https://gaia.ari.uni-heidelberg.de/gaiasky/docs/master/Location-log.html
Scraping https://gaia.ari.uni-heidelberg.de/gaiasky/docs/master/Virtual-textures.html
[...]
Scraping https://gaia.ari.uni-heidelberg.de/gaiasky/docs/master/Cubemaps.html
Scraping https://gaia.ari.uni-heidelberg.de/gaiasky/docs/master/Archetypes.html
Found 69 pages to scrape...
Extracting text from pages...
Scraping https://gaiasky.space
Scraping https://gaiasky.space/privacypolicy/
Scraping https://gaiasky.space/news/
[...]
Scraping https://gaiasky.space/news/2023/gaiasky_3.4.0/
Scraping https://gaiasky.space/news/2023/gaiasky_3.5.3/
Scraping https://gaiasky.space/news/page/5/
Scraping https://gaiasky.space/news/page/6/
Found 64 pages to scrape...
Extracting text from pages...
Storing embeddings in ChromaDB...
Connecting to Ollama for queries...

Ask a question (type 'exit' to quit): quit
```

Then, we can just run `gsai.py` without the flag to access the chatbot directly.

First, I asked about the main features of Gaia Sky:

> **Q: What are the main features of Gaia Sky?**
>
 > Gaia Sky is a powerful and versatile visualization tool designed to explore and analyze astronomical data, particularly from the Gaia mission. Here are some of its main features:
> 
> 1. **3D Visualization**: Gaia Sky allows users to view astronomical data in three dimensions, providing a more intuitive understanding of spatial relationships between celestial objects.
> 
> 2. **Data Integration**: It supports integration with various astronomical databases and catalogs, including but not limited to Gaia, allowing for comprehensive analysis and visualization.
> 
> 3. **Interactive Interface**: The software offers an interactive interface that enables users to zoom, rotate, and pan through the celestial sphere, making it easier to explore specific regions of interest.
> 
> 4. **Customizable Views**: Users can customize their views by selecting different color schemes, adjusting opacity levels, and filtering data based on various parameters such as magnitude, distance, or spectral type.
> 
> 5. **Scripting Capabilities**: Gaia Sky includes a scripting engine that supports JavaScript, enabling users to automate tasks, create complex visualizations, and perform custom analyses.
> 
> 6. **Virtual Reality (VR) Support**: The software offers VR support, allowing for immersive exploration of the cosmos using VR headsets. This feature is particularly useful for educational purposes and outreach activities.
> 
> 7. **Augmented Reality (AR) Support**: In addition to VR, Gaia Sky also supports AR, enabling users to overlay astronomical data onto real-world views through compatible devices.
> 
> 8. **Educational Tools**: The software includes a variety of educational tools and resources, such as pre-defined tours and tutorials, making it an excellent resource for teaching and learning about astronomy.
> 
> 9. **Cross-Platform Compatibility**: Gaia Sky is designed to run on multiple operating systems, including Windows, macOS, and Linux, ensuring broad accessibility.
> 
> 10. **Community and Support**: The developers of Gaia Sky maintain an active community and provide support through various channels, such as forums and documentation, to help users make the most of the software.
>
> These features collectively make Gaia Sky a valuable tool for astronomers, educators, and enthusiasts interested in exploring and understanding the universe.

This answer is not concise, but it is quite alright. It captures all important features of Gaia Sky and gives a short description for each. However, it includes imaginary features, like AR... Also, this model is quite slow on my computer. The whole answer must have taken about 3-4 minutes to generate.

Next, I ask how to install Gaia Sky on Linux. We have several options to install the software on Linux, including APT, DEB and AUR packages, Flatpak, AppImage, and tarballs. Let's see if the model captures these well.

> **Q: How do I install Gaia Sky on Linux?**
>
> To install Gaia Sky on a Linux system, you can follow these steps. There are multiple methods to install it, including using the package manager (if available), downloading the tarball, or building from source.
> 
> **Method 1: Using Package Manager (if available)**
>
> Some distributions may have Gaia Sky in their repositories. You can check and install it using your package manager.
> 
> For example, on Debian-based systems:
>   ```sh
>   sudo apt update
>   sudo apt install gaiasky
>   ```
> 
> On Fedora-based systems:
>   ```sh
>   sudo dnf install gaiasky
>   ```
> 
> **Method 2: Downloading the Tarball**
>
> 1. **Download the tarball:**
>    - Visit the [Gaia Sky download page](https://gaiasky.space/downloads/) and download the latest Linux version (usually a `.tar.gz` file).
> 
> 2. **Extract the tarball:**
>    ```sh
>    tar -xzvf gaiasky-<version>.tar.gz
>    ```
> 
> 3. **Navigate to the extracted directory:**
>    ```sh
>    cd gaiasky-<version>
>    ```
> 
> 4. **Run Gaia Sky:**
>    ```sh
>    ./gaiasky
>    ```
> 
> **Method 3: Building from Source**
>
> 1. **Install dependencies:**
> Ensure you have the necessary build tools and libraries installed. You can usually do this with:
>   ```sh
>   sudo apt-get update
>   sudo apt-get install git cmake g++ libglfw3-dev libglew-dev libassimp-dev libboost-all-dev
>   ```
> 
> 2. **Clone the repository:**
>   ```sh
>   git clone https://github.com/gaia-sky/gaiasky.git
>   cd gaiasky
>   ```
> 
> 3. **Build Gaia Sky:**
>   ```sh
>   mkdir build
>   cd build
>   cmake ..
>   make
>   ```
> 
> 4. **Run Gaia Sky:**
>   ```sh
>   ./gaiasky
>   ```
> 
> **Additional Configuration**
>
> - **Configuration File:** The configuration file for Gaia Sky is located at `~/.config/gaiasky/config.yaml`. You can edit this file to customize your settings.
> 
> - **Data Directory:** Ensure that the data directory (`$GS_DATA`) contains all necessary datasets. This directory is usually located in `~/.gaiasky/data`.
> 
> **Troubleshooting**
>
> - **Crashes at Start-up:** If Gaia Sky crashes at start-up, check the logs for any error messages and ensure you have all dependencies installed.
> - **Memory Issues:** If you run out of memory, try closing other applications or increasing your system's swap space.
> 
> By following these steps, you should be able to install and run Gaia Sky on your Linux system.


Wow, lots of awesome info here. It gets some things right. There are also a few errors:

- It shows how to install Gaia Sky on `apt` and `dnf` systems as if Gaia Sky was in the official repositories. It is not, you need to download the packages.
- The "building from source" section is completely bullshit. It instructs to use `cmake` and `make`, but Gaia Sky is a Java application that uses `gradle`.
- It missed Flatpak and AppImage.

To be fair, this was a rather open question, so it would be surprising that such a small model were able to capture all the info perfectly.

Finally, I asked for something much more technical and specific---I asked it to explain how cubemaps are used in Gaia Sky.
    
> **Q: How does Gaia Sky use cubemaps?**
> 
>  Cubemaps are used in Gaia Sky to provide detailed and realistic textures for various objects, particularly planets and other celestial bodies. They offer a more immersive experience by allowing the rendering of different views of an object from multiple angles. Here's how cubemaps are utilized in Gaia Sky:
> 
> 1. **Detailed Texturing**: Cubemaps consist of six individual textures that represent the up, down, right, left, front, and back views of an object. This allows for highly detailed and realistic texturing of surfaces.
> 
> 2. **Realistic Lighting and Reflections**: By using cubemaps, Gaia Sky can simulate realistic lighting and reflections on objects. This is particularly useful for rendering planets with atmospheres or other complex surfaces where light interacts in a variety of ways.
> 
> 3. **Volumetric Effects**: Cubemaps are also used to create volumetric effects, such as the aurora borealis and australis. These effects are rendered using ray-marching algorithms, which produce a volumetric object that appears more realistic.
> 
> 4. **Multiple Channels**: Gaia Sky supports multiple channels for cubemaps, including diffuse, specular, normal, emissive, metallic, roughness, and height maps. This allows for a wide range of visual effects to be applied to objects.
> 
> 5. **Ease of Generation**: Equirectangular images can be easily converted into cubemaps using provided scripts. This makes it straightforward for users to create their own custom textures for use in Gaia Sky.
> 
> 6. **Integration with Gaia Sky Properties**: To use a cubemap in Gaia Sky, you need to set the appropriate property (e.g., "diffuseCubemap") to the location of the six cubemap sides. Gaia Sky will then automatically select the correct image for each side based on the file name suffixes.
> 
> By leveraging cubemaps, Gaia Sky enhances the visual quality and realism of its simulations, providing users with a more engaging and immersive experience.

This is an ok answer. Save for the volumetric grabage (point 3), all the other points are correct.So 5/6, I guess?


I think this Mistral model is too verbose. You can see specks of larger models, like the good formatting, or the effort to produce complete and exhaustive answers. However, the accuracy is not always on point. I wonder if using a model with better quantization (Q6?) would solve this.


### Llama 3.1 instruct, 8B Q5-K-M

Now we test the [Llama 3.1 instruct (8B, Q5-K-M)](https://ollama.com/library/llama3.1:8b-instruct-q5_K_M) model, an instruct-specific model that is much smaller than Mistral Small 3 (24B). However, this time around I stepped up the quantization a bit by using Q5_K_M, which should improve accuracy over the basic Q4_0.

First, features:

> **Q: What are the main features of Gaia Sky?**
> 
> Based on the provided text, here are the main features of Gaia Sky:
> 
> 1. **Real-time Space Simulation**: Gaia Sky is a real-time space simulation software that allows users to explore the universe in 3D.
> 2. **Astrophysical Data**: It includes astrophysical data from various sources, such as the European Space Agency's (ESA) Gaia mission, which provides precise positions and distances of stars in the Milky Way galaxy.
> 3. **Interactive Interface**: The software has an interactive interface that allows users to navigate through the universe, explore different celestial objects, and customize their viewing experience.
> 4. **Real-time Rendering**: Gaia Sky uses real-time rendering techniques to provide a smooth and immersive experience, allowing users to see the universe in stunning detail.
> 5. **Customization Options**: Users can customize their view by selecting specific objects, adjusting the zoom level, and choosing from various display options.
> 6. **Scripting Capabilities**: The software has scripting capabilities that allow developers to create custom scenarios, simulations, and visualizations using a Python-based scripting language.
> 7. **VR Support**: Gaia Sky also supports Virtual Reality (VR) and Augmented Reality (AR) experiences, allowing users to immerse themselves in the universe like never before.
> 
> Overall, Gaia Sky is a powerful tool for astronomers, scientists, educators, and anyone interested in exploring the universe in an interactive and immersive way.


This looks very good. It is shorter than the answer given by the previous model, but just as informative. Also, the response was generated much faster than with Mistral, probably due to the difference in model sizes.

The next question is about the Linux installation.

>**Q: How do I install Gaia Sky on Linux?**
>
> According to the text, you can install Gaia Sky on Linux using one of the following methods:
> 
> 1. **Flatpak**: You can download and install the Flatpak package from the Gaia Sky downloads page.
> 2. **AppImage**: You can download and run the AppImage file, which will create a new directory with the exported application.
> 3. **Tar.gz archive**: You can export Gaia Sky into a tar.gz archive file by running a script, and then extract it to a directory.
> 
> Additionally, you can also build the source code from scratch using the instructions provided on the Gaia Sky downloads page.
> 
> It's worth noting that these installation methods are distro-agnostic, meaning they should work on most Linux distributions.

This time around, it got Flatpaks and AppImages right, but not the distro packages for Debian, Fedora or Arch. It looks like it only listed distro-agnostic installation methods because I was not specific about what Linux distribution I was using. I'm liking this instruct model more and more. It is quite fast too.

Finally, cubemaps:

> **Q: How are cubemaps used in Gaia Sky?**
> 
> According to the text, cubemaps are used in Gaia Sky to enhance 3D rendering and provide more realistic textures for objects. Specifically:
> 
> * Cubemaps can be generated from equirectangular images using a Python script.
> * In Gaia Sky, cubemaps are composed of six individual textures for the up, down, right, left, front, and back directions.
> * The "diffuseCubemap" property in Gaia Sky's configuration file points to the location of these six cubemap sides.
> * Gaia Sky automatically selects the appropriate image for each cubemap side based on the file name suffixes (e.g. _ft.jpg, _bk.jpg, etc.).
> 
> By using cubemaps, Gaia Sky can provide more realistic and detailed textures for objects in 3D space, enhancing the overall visual experience of the application.

This answer is much more specific than the one given by Mistral. It touches some right keys, but, I think, misses the global picture. However, this is very promising.

In the global picture, I like the compact responses of Llama better than those provided by Mistral. Also, Mistral is almost 3 times larger than Llama (22B vs 8B), so it is much slower on my machine.

## Performance

In my case, I'm pretty limited by my hardware, and responses tend to be slow with the larger model (Mistral). The speed is quite good with Llama (8B) though. True, I'm running this a very old computer for today's standards (Intel(R) Core(TM) i7-7700 (8) @ 4.20 GHz, NVIDIA GeForce GTX 1070 8 GB, 32 GB RAM), so it is what it is. On smaller models (1B to 5B), I found the responses to be mostly garbage. On larger instruct models with decent quantization, accuracy is greatly improved at the expense of your precious time.

## Conclusion

In this post, we've expanded on our previous post and developed an AI chatbot able to answer questions on Gaia Sky. The information is sourced from the Gaia Sky homepage and documentation. With the power of web scraping, embeddings, and Ollama, we've brought the Gaia Sky website and docs to life with smart, context-aware interactions. No more endless searches for answers. Instead, we now have a chatbot that knows exactly where to look and can provide concise, relevant responses. So go ahead and try it out---who knew scraping could be this useful?

It's pretty obvious to me that such small models are able to get most of the questions *almost* right, but they are most definitely not suited for professional settings. In this case, larger models (at least 70B, I reckon) would be required. For our purposes here, Mistral Small 3 instruct (22B) and Llama 3.1 instruct (8B) are enough.

Of course, you can always use an off-the-shelf no-code application like [AnythingLLM](https://anythingllm.com/) or [Open WebUI](https://openwebui.com/). Both support local models via Ollama, and both integrate RAG. I actually recommend using these if you are not too interested in the details.

