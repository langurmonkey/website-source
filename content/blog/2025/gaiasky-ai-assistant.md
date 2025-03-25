+++
author = "Toni Sagrista Selles"
categories = ["AI"]
tags = ["LLM", "AI", "ollama", "RAG"]
date = 2025-03-25
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

## Step 1: Scraping the Websites

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

## Step 2: Storing Embeddings with ChromaDB
Once we've scraped the content, it’s time to turn that raw text into something that the machine can understand. This is where embeddings come into play.


- We use the `langchain` library to split the scraped text into manageable chunks. This is done using the `RecursiveCharacterTextSplitter`, which splits the content into chunks of a predefined size (to avoid overloading the model). I tuned this by trial and error, and ended up with a chunk size of 1000, and a chunk overlap of 200.

- The text is then passed through an embedding model, specifically the "BAAI/bge-base-en-v1.5" model from [HuggingFace](https://huggingface.co/BAAI/bge-base-en-v1.5), which transforms it into a high-dimensional vector representation.

- Finally, we store these vectors in a vector database, Chroma DB. The vectors are indexed so that when we query the database, it can efficiently retrieve the most relevant pieces of text. For the retrieval, I'm using 5 results (`search_kwargs` in `as_retriever()` method). I tried with 2 and 3, but it seemed that most models didn't get enough context.

This is where the magic happens. By converting text into vectors, we enable the chatbot to compare and understand the semantic meaning of different pieces of text. The advantage here is that embeddings can capture the relationships between words and concepts, even if they’re not an exact match — meaning the chatbot can intelligently pull out relevant context to answer your questions.

The relevant code consists of the concatenated texts we produced in the previous step (we called it `doc_text`), and the location for our disk database:

```python
def store_embeddings(texts, db_path):
    """Tokenizes, embeds, and stores the texts in a ChromaDB vector store."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.create_documents([texts])
    if not documents:
        raise ValueError("No documents found to embed. Check the scraper output.")
    
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")
    vector_store = Chroma.from_documents(documents, embeddings, persist_directory=db_path)
    return vector_store

print("Storing embeddings in ChromaDB...")
db_path = "chroma_db"
vector_store = store_embeddings(doc_text, db_path)
```

## Step 3: Querying with Ollama

Now that we’ve got our indexed data, it’s time to query it. But instead of just returning raw search results, we want to use an LLM (Large Language Model) to generate smart, context-aware answers. Enter Ollama.

- We use `langchain`’s `RetrievalQA` chain to combine the Chroma vector store with an LLM.

- The LLM we’re using is locally hosted through Ollama. The model takes the relevant text retrieved from Chroma and uses that context to generate responses to user queries.

- We use a simple interface where the user can ask questions, and the chatbot pulls from the stored content to generate an answer. If it doesn’t have enough context to answer, it will graciously let you know, but more often than not, it’s ready to impress with its knowledge.

By combining Chroma with an LLM, we ensure that the chatbot not only returns raw text but generates contextually appropriate answers. The power of an LLM with RAG lies in its ability to take a set of relevant documents and provide a coherent, informative response. So, when you ask, “What’s the internal reference system of Gaia Sky?” the chatbot can retrieve the most relevant content and synthesize it into a helpful response.

The relevant code lives in the `query_with_ollama(vector_store, llm_model)` method.

```python
def query_with_ollama(vector_store, model_name):
    """Uses an Ollama model to retrieve and answer user queries based on stored embeddings."""
    retriever = vector_store.as_retriever(search_kwargs={"k": n_results})  # Avoid exceeding stored docs
    qa_chain = RetrievalQA.from_chain_type(llm=OllamaLLM(model=model_name), retriever=retriever)
    
    while True:
        query = input(colored("Ask a question (type 'exit' to quit): ", "yellow", attrs=["bold"]))
        if query.lower() == "exit" or query.lower() == "quit" or query.lower() == "bye":
            break
        answer = qa_chain.invoke({"query": query})
        print(answer["result"])

print("Connecting to Ollama for queries...")
query_with_ollama(vector_store, llm_model)
```
This method contains the context retrieval code and the question-answer loop. The actual model to use is pulled from the user (code not shown). After starting, the program presents the available models, and the user needs to select one of them.

## Step 4: Implementation details
This is not actually a step, but hey. One of the coolest aspects of this setup is the flexibility it provides. You can scrape the website and generate embeddings only when needed by using a command-line flag (`--scrape`). If you’ve already scraped the site and generated embeddings, the system will load the existing embeddings from disk, saving you time and resources. It’s efficient, and you don’t have to redo the work every time you launch the chatbot.

## Testing -- Mistral 24B

This time around I tested the program with the [Mistral-small 24B](https://ollama.com/library/mistral-small) model. I think this is at the limit of what my computer can handle (see [conclusion](#conclusion)).

On a first pass, we run the program with the `--scrape` flag to gather the information from the websites and create the embeddings.

```bash
$ gsai.py --scrape
Welcome to the Gaia Sky AI assistant! We connect to Ollama to use a local LLM.

Available models:
 [0] gemma3:12b
 [1] qwen2.5:7b
 [2] deepseek-r1:14b
 [3] llama3.1:8b
 [4] mistral-small:24b

Select model (default 0): 4
Using model: mistral-small:24b

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
> According to the provided text, the main features of Gaia Sky are:
> 
> *   It's a real-time, 3D astronomy visualization platform for desktop and VR.
> *   It runs on Windows, Linux, and macOS.
> *   It's open source and free.
> *   It enables exploration of the universe using scientific datasets.
> *   It has a high object count.

The answer, although incomplete, is fairly decent. It contains a nice summary of the *most important* features.


Then, I asked for something more technical. Specifically, I asked the model to explain how cubemaps are used in Gaia Sky.
    
> **Q: How does Gaia Sky use cubemaps?**
> 
> Gaia Sky uses cubemaps in several ways:
> 
> 1. **Skyboxes**: Cubemaps are implemented in skyboxes to create immersive backgrounds.
> 2. **Reflections**: Cubemaps are used for reflections, but there is a noted issue with reflection directions that needs fixing.
> 3. **Planetarium Mode**: The planetarium mode also works with the cubemap system used in Panorama mode, allowing users to adjust the cubemap side resolution.
> 
> Additionally, Gaia Sky supports spherical mirror projection by defining a warp mesh file, which contains distortion data to compensate for the non-planar nature of the projection surface.

This is a very good answer. It nails all the places where cubemaps are used, so 10/10. Extra point for brevity.


I asked again about the main features of Gaia Sky, just to see if the answer would be different.

> **Q: What are the main features of Gaia Sky?**
> 
> Based on the provided context, the main features of Gaia Sky version 3.5.6 include:
> 
> 1. **Film Grain Filter**: A new filter that is disabled by default.
> 2. **Maximum Age for Download Files**: Users can set a maximum age limit of 6 hours for downloaded files.
> 3. **Improved Recursive Grid**: Enhanced with traveling pulses and a noise mask, along with an 'animate' setting to toggle animation on and off.
> 4. **Initial Notice**: A notice about Gaia Sky contacting the server to get dataset updates list.
> 5. **Shader Compilation Error Handling**: Improved handling of shader compilation errors.
> 6. **Elevation Representation**: Added a new ‘regular’ mode for elevation representation without tessellation, which is now the default mode.
> 7. **Discontinued Parallax Mapping**: The parallax mapping elevation type has been discontinued in favor of vertex displacement.
> 8. **Full Support for Point Lights**: Full support for point lights, including their use for stars and true depth-tested close-by stars with light glow enabled.
> 
> These features highlight the enhancements and improvements made to Gaia Sky in version 3.5.6.

And different it was, indeed. It seemed to source these features directly from the Gaia Sky 3.5.6 [release notes](http://gaiasky.space/downloads/releases/v3.5.6/). This version was published in October 2023, and I have no idea why this was provided as context. Almost every release has a 'features' section, so I reckon this was due to chance. Maybe increasing the number of results would help here?

Finally, I asked for Gaia Sky VR. A pretty general question.


> **Q: What is Gaia Sky VR?**
> 
> Based on the provided context, Gaia Sky VR refers to the virtual reality (VR) capabilities of Gaia Sky, a real-time, 3D astronomy visualization platform. The updates mentioned include features like an in-scene VR user interface with mouse interaction, support for gamepad and VR controller interactions, and specific mappings for Valve Index VR controllers. These enhancements allow users to explore the universe in VR using Gaia Sky on Windows, Linux, and macOS.

And again, a weird answer. I'm not sure what it refers to with 'the updates mentioned'. However, the text is almost correct, with some quirkiness (mouse interaction, gamepad).

## Testing -- Gemma3 12B

[Gemma 3 (12B)](https://ollama.com/library/gemma3) by Google features half the number of parameters of Mistral-small. It is built on Gemini technology for text and image processing. Let's see how it performs.

First, the main features of Gaia Sky. Here, I missed the question mark at the end.

> **Q: What are the main features of Gaia Sky**
> 
> Here's a summary of the main features of Gaia Sky, based on the provided context:
> 
> **Gaia Sky 3.5.6 Features:**
> 
> *   Film grain filter (disabled by default)
> *   Improved recursive grid with travelling pulses and a noise mask
> *   Option to toggle animation on/off for the recursive grid
> *   Elevation representation without tessellation (new default mode)
> *   Full support for point lights for stars
> *   True depth-tested close-by stars
> *   Contacting the server for dataset updates
> 
> **Gaia Sky 3.5.5 Features:**
> 
> *   New user interface mode (old UI still available)
> *   "Play camera path" action (bound to Alt+C)
> *   Better star close-up shader
> *   Option to render stars as spheres
> *   Revamped shader include directive
> *   Shader libraries moved to shader/lib
> *   Retire Gaia FOV camera modes
> *   Adjusted default atmosphere exposure value
> *   Disabled fading scrollbars
> *   Prepared PBR shaders (iridescence, transmission, thickness - still inactive)

It selects two *seemingly random* versions and lists their features. This looks like an error in the context selection, clearly. So I increased the number of results from 5 to 10, and ask again. Same result 🤷‍♂️.

Then, for the cubemaps question.

> **Q: How does Gaia Sky use cubemaps?**
> 
> Here's a breakdown of how Gaia Sky utilizes cubemaps, synthesized from the provided text:
> 
> **What are Cubemaps?**
> 
> *   Cubemaps are an alternative to traditional equirectangular textures (the standard spherical projection) for rendering surfaces like planets and moons in Gaia Sky.
> *   They help eliminate visual artifacts (distortions) that appear at the poles when using regular textures on spherical models. Alternatives like icospheres or octahedronspheres can introduce seams instead.
> 
> **How Gaia Sky Uses Them:**
> 
> *   **Artifact Reduction:** The primary benefit is avoiding the "stretched" look at the poles.
> *   **Supported Channels:** Gaia Sky supports using cubemaps for multiple texture channels:
>     *   Diffuse (main color)
>     *   Specular (highlights/reflections)
>     *   Normal (surface details/bumps)
>     *   Emissive (glow)
>     *   Metallic
>     *   Roughness
>     *   Height (for parallax/depth effect)
> *   **Cloud Layers:** The diffuse cubemap can be specifically applied to the cloud layer, enhancing their appearance.
> 
> Essentially, Gaia Sky uses cubemaps to achieve more realistic and visually appealing renderings of celestial bodies by eliminating texture distortion and offering flexibility in how surface details and lighting are represented.

This is fine, but misses reflections and sky boxes entirely.

I wonder whether embedding is the problem here. It seemed to work well enough with Mistral, so maybe the differences come down to the size of the models.

<!-- I tried the *Linq-Embed-Mistral* embedding model, which is currently listed [second](Linq-AI-Research/Linq-Embed-Mistral) on HuggingFace's MTEB leaderboard. -->


## Conclusion

With the power of web scraping, embeddings, and Ollama, you can bring any website or documentation to life with smart, context-aware interactions. No more endless searches for answers. Instead, you’ll have a chatbot that knows exactly where to look and can provide concise, relevant responses. So go ahead and try it out — who knew scraping could be this useful?

However, this is *slow*. True, I'm running this on a very old computer for today's standards (Intel(R) Core(TM) i7-7700 (8) @ 4.20 GHz, NVIDIA GeForce GTX 1070 8 GB, 32 GB RAM), but the performance is far from ideal. On small models (1 to 5 billion parameters), the responses are almost useless. On larger models like the Mistral 24B, accuracy is greatly improved, but it takes its time to generate long responses.
