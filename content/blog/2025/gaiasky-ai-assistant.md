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

In my last [post](/blog/2025/local-llm-rag), I explored the concept of Retrieval-Augmented Generation (RAG) to enable a locally running generative AI model to access and incorporate new information. To achieve this, I used hardcoded documents as context, which were then embedded as vectors and persisted into Chroma DB. These vectors are used during inference to use as context for a local LLM chatbot.
But using a few hardcoded sentences is hardly elegant or particularly exciting. It's alright for educational purposes, but that's as far as it goes. However, if we need to build a *minimally useful system*, we need to be more sophisticated than this. In this new post, I set out to create a local Gaia Sky assistant by using the [Gaia Sky documentation site](http://docs.gaiasky.space) and the [Gaia Sky homepage](https://gaiasky.space) as supplementary information, and leveraging Ollama to generate context-aware responses. So, let’s dive into the topic and explain how it all works.

The source code used in this post is available [in this repository](https://codeberg.org/langurmonkey/gaiasky-ai).

<!--more-->

## Scraping the Websites

The first thing we need to do is extract useful content from our sources. Since we use websites, this is where web scraping comes into play:

- We’re using the `requests` library to fetch the HTML content from a given URL.

- First, we get all the internal links for every URL by recursively scraping the content (with `BeautifulSoup`) and looking for all `a` tags (anchors) that don't point to internal anchors. This happens in `get_all_doc_links(base_url)`.

- ~~Then, we extract the text from every page by extracting the tags `h1`, `h2`, `h3`, `h4`, `h5`, `p`, `li`, `td`, and `article`. This step required a little bit of trial and error. Once we have the text for each page, we concatenate everything and return it. This is implemented mostly in `extract_text_from_page(url)`~~. At first, I wrote my own code to retrieve content from a URL and convert it to text. Of course, this code was less than impressive, and even though it worked, the results were not optimal. Since then I experimented with other methods to extract text from websites, like the libraries `newspaper3K`, `goose3`, and `html2text`. I settled for the latter, as it produces Markdown-formatted documents which are particularly well suited for LLMs. You can see the very different results from the previous method by inspecting the [history of this post](https://codeberg.org/langurmonkey/website-source/commits/branch/master/content/blog/2025/gaiasky-ai-assistant.md). The initial scraping behavior can still be accessed in the application with the flag ``--local-scraper``.

- As we mentioned earlier, we make sure to avoid non-HTML files and internal page anchors (those pesky # URLs that only point to a specific section). This ensures that we only scrape actual webpages that contain relevant data.

With this method, we capture all the relevant documentation---every corner of the site. Since the process is recursive, we don’t miss any pages (unless they’re blocked or have weird redirect loops, but that's a discussion for another time).

The code box below shows the link gathering, scraping, and text extraction.

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
    """Extracts meaningful text from a given URL using html2text."""
    import html2text
    try:
        response = requests.get(url)
        h = html2text.HTML2Text()
        h.ignore_links = False  # Set this to True to ignore links
        return h.handle(response.text)
    except:
        return None

def scrape_urls(base_urls, local_scraper=False):
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

- Finally, we store these vectors in a vector database, Chroma DB. The vectors are indexed so that when we query the database, it can efficiently retrieve the most relevant pieces of text. For the retrieval, I'm using a default of 6 results (`search_kwargs` in `as_retriever()` method). I tried with 2 and 3, but it seemed that most models didn't get enough context.

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

- We use a simple interface where the user can ask questions, and the chatbot pulls from the stored content to generate and stream an answer. If it doesn’t have enough context to answer, it will graciously let you know, but more often than not, it’s ready to impress with its knowledge.

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

- **Temperature** -- The temperature controls the randomness of the model's responses, with lower values making answers more deterministic and factual, while higher values increase creativity and variability. We use a default low temperature value of 0.3 to get more correct and less creative responses. The temperature can be set with the argument `-t`.
- **Number of results** -- The number of results parameter (`n_results` or `k`) determines how many relevant documents are retrieved from the vector database to provide context for the model's response, with higher values increasing the available information but potentially adding noise. We use the default of 6 results, but this can be changed with the `-k` argument.

The relevant code that does the actual querying lives in the `query_with_ollama(vector_store, llm_model)` method. The code below includes the relevant parameters at the top.

```python

system_prompt = (
    "You are a customer support agent, helping users by following directives and answering questions. "
    "Use the given context to answer the question. "
    "If you don't know the answer, say you don't know. "
    "Keep the answer concise and to the point. "
    "Context: {context}"
)

# In the real program, both n_results and temp can be set with program arguments.
# Number of results to retrieve from the vector store.
n_results = 6
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

```
This method contains the context retrieval code and the question-answer loop. The actual **LLM model** to use, stored in `llm_model`, is **user-defined** (code not shown here). After starting, the program presents the available models, and the user needs to select one of them. This happens in the `chatbot()` function, which is the final piece of the puzzle. It gets the vector store object---either we have just ingested it from scraping (if `--scrape` is used) or we have retrieved it from the database, if the program is called with no arguments. Then, it prompts the user for the model to use, and calls `query_with_ollama(...)`.

```python
def chatbot(vector_store):
    # List available models
    try:
        models = ollama.list()
        model_names = [m.model for m in models.models]
    except:
        print(f"{colored('ERROR', 'red')}: Ollama service is not running.")
        exit(1)

    # Print the available models with index numbers
    print("Available models:")
    for i, name in enumerate(model_names):
        print(f" [{colored(i, 'green')}] {name}")

    # Loop until a valid selection is made
    while True:
        choice = input(f"\nSelect model (default {colored('0', 'green')}): ").strip()

        if choice == "":  # Default to 0 if empty input
            llm_model = model_names[0]
            break

        if choice.isdigit():  # Check if input is a number
            index = int(choice)
            if 0 <= index < len(model_names):  # Check if index is valid
                llm_model = model_names[index]
                break

        print("Invalid selection. Please enter a valid number.")

    print(f"LLM model: {colored(llm_model, 'yellow', attrs=['bold'])}")
    print(f"Embed model: {colored(embed_model, 'yellow', attrs=['bold'])}")

    print("Connecting to Ollama for queries...")
    query_with_ollama(vector_store, llm_model)

````


## Implementation details

The scraping function is hidden behind a flag (`--scrape`). When it is used, the websites are scraped, their information is extracted, embedded into vectors and ingested in the database. When no arguments are used, the program starts the chatbot. Of course, **you need to run at least once with `--scrape` before using the chatbot**. But if you’ve already scraped the site and generated embeddings, the system will load the existing embeddings from disk, saving you time and resources. It’s efficient, and you don’t have to redo the work every time you launch the chatbot.

If you change the embed model, remember to nuke the database (`rm -rf chroma_db`) and re-do the scraping!

Finally, by using `stream=True` in the creation of `OllamaLLM`, and calling `chain.stream()` instead of `chain.query()`, we can stream the response as it is generated, token-by-token. This is the style most web chatbots use.

## Evaluation

In this section we test the system with [`mistral-small:22b-instruct-2409-q4_K_M`](https://ollama.com/library/mistral-small:22b-instruct-2409-q4_K_M), a small instruct LLM with capabilities comparable to larger models, and with [`llama3.1:8b-instruct-q5_K_M`](https://ollama.com/library/llama3.1:8b-instruct-q5_K_M), a much smaller but better quantized model(Q5-K-M vs Q4-K-M), also specifically trained for instruct.

I ask each model 3 questions:

- The usages of Gaia Sky.
- How to install Gaia Sky on Linux.
- How are cubemap textures used in Gaia Sky.

Here are links to the relevant sections.

- [Mistral Small 3](#mistral-small)
    - [Usages](#mistral-small-usages)
    - [Linux installation](#mistral-small-linux)
    - [Cubemaps](#mistral-small-cubemaps)
- [Llama 3.1](#llama31)
    - [Usages](#llama31-usages)
    - [Linux installation](#llama31-linux)
    - [Cubemaps](#llama31-cubemaps)

{{< notice "Note" >}}
You can install these models directly with Ollama:
```
ollama pull mistral-small:22b-instruct-2409-q4_K_M llama3.1:8b-instruct-q5_K_M
```
{{</ notice >}}

Remember, if you want to try out the chatbot yourself, download it from [this repository](https://codeberg.org/langurmonkey/gaiasky-ai).

<a name="mistral-small"></a>
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

Done! Run the script without arguments to start the chatbot.
```

Then, we run `gsai.py` without the flag to access the chatbot directly and start asking questions. These are documented in the quoted blocks below.

First, I asked about what can Gaia Sky be used for. This is a general type of question, so let's see how it fares.

<a name="mistral-small-usages"></a>
> **Q: State the possible usages of Gaia Sky.**
>
>  Gaia Sky is a powerful and versatile software tool that can be used for a variety of purposes, especially in the fields of astronomy, education, and scientific research. Here are some of its potential usages:
> 
> 1. **Educational Tool**: Gaia Sky can be used to teach students about astronomy, celestial mechanics, and the universe. It provides an interactive and visually engaging way to learn about different astronomical objects and phenomena.
> 
> 2. **Research in Astronomy**: Scientists and researchers can use Gaia Sky to visualize and analyze complex datasets from space missions like Gaia, allowing them to gain insights into stellar evolution, galactic structure, and other astrophysical processes.
> 
> 3. **Data Visualization**: The software offers advanced data visualization capabilities, enabling users to create detailed 3D models of celestial objects and phenomena. This is particularly useful for presenting research findings or educational content in a compelling manner.
> 
> 4. **Virtual Tours**: Gaia Sky can be used to create virtual tours of the universe, allowing users to explore different regions of space, from our solar system to distant galaxies.
> 
> 5. **Public Outreach**: Astronomy enthusiasts and science communicators can use Gaia Sky to create engaging presentations and demonstrations for public events, such as star parties or science festivals.
> 
> 6. **Simulations**: Researchers can use the software to run simulations of various astronomical scenarios, helping them understand how different factors influence celestial phenomena.
> 
> 7. **Planetarium Software**: Gaia Sky can be used in planetariums to provide immersive and interactive experiences for visitors, enhancing their understanding of astronomy through visual storytelling.
> 
> 8. **Scientific Collaboration**: The software facilitates collaboration among researchers by providing a common platform to share and discuss data, simulations, and findings.
> 
> 9. **Artistic Visualizations**: Artists can use Gaia Sky to create stunning visual representations of astronomical objects and scenes for artistic purposes or multimedia projects.
> 
> 10. **Space Mission Support**: Gaia Sky can be used by teams involved in space missions to plan observations, analyze data, and support mission operations.
> 
> These uses highlight the flexibility and power of Gaia Sky as a tool for both educational and professional applications in astronomy and related fields.

This answer is not concise, but it is quite alright. It captures all important features of Gaia Sky and gives a short description for each. However, I think it might be overselling Gaia Sky a tiny bit, but hey. Also, this model is quite slow on my computer, more on that later.

Next, I ask how to install Gaia Sky on Linux. We have several options to install the software on Linux, including APT, DEB and AUR packages, Flatpak, AppImage, and tarballs. Let's see if the model captures these well.

<a name="mistral-small-linux"></a>
> **Q: How do I install Gaia Sky on Linux?**
>
> To install Gaia Sky on a Linux system, you have several options depending on your distribution and preferences. Here are the most common methods:
> 
> **Using Flatpak**
> 1. **Install Flatpak**: If you don't already have Flatpak installed, you can install it using your package manager. For example, on Debian-based systems (like Ubuntu), you would use:
>    ```sh
>    sudo apt update
>    sudo apt install flatpak
>    ```
> 
> 2. **Add the Flathub repository**:
>    ```sh
>    flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
>    ```
> 
> 3. **Install Gaia Sky**:
>    ```sh
>    flatpak install flathub space.gaiasky.GaiaSky
>    ```
> 
> 4. **Run Gaia Sky**:
>    ```sh
>    flatpak run space.gaiasky.GaiaSky
>    ```
> 
> **Using AppImage**
> 1. **Download the AppImage**: Go to the [Gaia Sky downloads page](https://gaiasky.space/downloads) and download the latest `.AppImage` file for Gaia Sky.
> 
> 2. **Make the AppImage executable**: Open a terminal, navigate to the directory where you downloaded the AppImage, and run:
>    ```sh
>    chmod +x GaiaSky-*.AppImage
>    ```
> 
> 3. **Run the AppImage**:
>    ```sh
>    ./GaiaSky-*.AppImage
>    ```
> 
> **Using Unix Installer**
> 1. **Download the installer**: Go to the [Gaia Sky downloads page](https://gaiasky.space/downloads) and download the `.run` file for the Unix installer.
> 
> 2. **Make the installer executable**: Open a terminal, navigate to the directory where you downloaded the installer, and run:
>    ```sh
>    chmod +x GaiaSky-*.run
>    ```
> 
> 3. **Run the installer**:
>    ```sh
>    ./GaiaSky-*.run
>    ```
> 
> 4. **Follow the on-screen instructions** to complete the installation.
> 
> **Using TAR.GZ Package**
> 1. **Download the TAR.GZ package**: Go to the [Gaia Sky downloads page](https://gaiasky.space/downloads) and download the `.tar.gz` file for Gaia Sky.
> 
> 2. **Extract the package**: Open a terminal, navigate to the directory where you downloaded the TAR.GZ file, and run:
>    ```sh
>    tar -xzf GaiaSky-*.tar.gz
>    ```
> 
> 3. **Move the extracted folder** to your desired installation location (e.g., `/opt`):
>    ```sh
>    sudo mv GaiaSky /opt/GaiaSky
>    ```
> 
> 4. **Create a symbolic link** in `/usr/local/bin`:
>    ```sh
>    sudo ln -s /opt/GaiaSky/gaiasky /usr/local/bin/gaiasky
>    ```
> 
> 5. **Run Gaia Sky**:
>    ```sh
>    gaiasky
>    ```
> 
> **Using Distro-Specific Packages (DEB, RPM, AUR)**
> For distro-specific packages, you can usually install them directly using your package manager:
> 
> - **Debian/Ubuntu**:
>   ```sh
>   sudo apt update
>   sudo apt install gaia-sky
>   ```
> 
> - **RedHat/Fedora**:
>   ```sh
>   sudo dnf install gaia-sky
>   ```
> 
> - **Arch Linux**:
>   ```sh
>   yay -S gaia-sky
>   ```
> 
> Choose the method that best suits your needs and preferences.

Wow, lots of awesome info and formatting here. It gets most of the information right, but it misses the mark on the installation for Debian and RedHat (we have no packages in their repositories), and Arch Linux (the package is actually called `gaiasky`, not `gaia-sky`). Other than that, I think this is a good answer.

To be fair, this was a rather open question, so it would be surprising that such a small model were able to capture all the info perfectly.

Finally, I asked for something much more technical and specific---I asked it to explain how cubemaps are used in Gaia Sky.
    
<a name="mistral-small-cubemaps"></a>
> **Q: Explain how cubemap textures are used in Gaia Sky.**
> 
>  Cubemaps are a type of texture that maps an entire environment onto a cube's six faces, providing a full 360-degree view. In Gaia Sky, cubemaps are primarily used to create realistic and immersive environments for planets and other celestial bodies. Here’s how they are utilized:
> 
> 1. **Environment Mapping:**
>    Cubemaps are employed for environment mapping, which involves projecting the surrounding scene onto a sphere or cube. This technique is particularly useful for rendering reflections on surfaces, such as water or metallic objects, giving them a more realistic appearance.
> 
> 2. **Skyboxes:**
>    One common use of cubemaps in Gaia Sky is to create skyboxes. A skybox is a cube that surrounds the scene and displays an environment map on its faces. This technique is used to simulate distant scenery, such as the sky or outer space, without needing to render far-off objects in detail.
> 
> 3. **Planetary Surfaces:**
>    Cubemaps can also be applied to planetary surfaces to create detailed and varied textures. By mapping different environments (like oceans, mountains, or forests) onto the faces of a cube, Gaia Sky can generate diverse and realistic planetary landscapes.
> 
> 4. **Lighting and Shadows:**
>    Cubemaps are used in lighting calculations to simulate how light interacts with the environment. This includes creating realistic shadows and highlights based on the surrounding scene, enhancing the overall visual quality of the rendered objects.
> 
> **Implementation Steps:**
> 1. **Creation of Cubemap Textures:**
>    - Developers create cubemap textures using specialized software that can render 360-degree environments. These tools often allow for the creation of high-quality, seamless textures.
> 
> 2. **Loading Cubemaps in Gaia Sky:**
>    - The created cubemaps are then loaded into Gaia Sky. This process involves specifying which texture should be applied to which face of the cube (positive X, negative X, positive Y, negative Y, positive Z, and negative Z).
> 
> 3. **Application in Shaders:**
>    - The shaders in Gaia Sky are programmed to use these cubemaps for various effects, such as reflections, environment lighting, and skybox rendering. This is done by sampling the cubemap texture within the shader code based on the viewing direction or other parameters.
> 
> **Benefits:**
> - **Realism:** Cubemaps help create highly realistic environments by providing detailed textures and reflections.
> - **Performance:** Instead of rendering distant objects, which can be computationally expensive, cubemaps allow for quick and efficient simulation of the environment.
> - **Flexibility:** They can be easily swapped out to change the appearance of an environment without altering the underlying geometry.
> 
> In summary, cubemap textures play a crucial role in Gaia Sky by enabling the creation of immersive, realistic environments through techniques like environment mapping and skybox rendering.

This is perhaps too detailed, and sources information from outside of the context, but it is mostly correct, if a little verbose. I'm happy with this answer.

All in all, I think this Mistral model is a little too verbose. You can see specks of larger models, like the good formatting, or the effort to produce complete and exhaustive answers. However, the accuracy is not always on point. I wonder if using a model with better quantization (Q6?) would solve this.

<a name="llama31"></a>
### Llama 3.1 instruct, 8B Q5-K-M

Now we test the [Llama 3.1 instruct (8B, Q5-K-M)](https://ollama.com/library/llama3.1:8b-instruct-q5_K_M) model, an instruct-specific model that is much smaller than Mistral Small 3 (24B). However, this time around I stepped up the quantization a bit by using Q5_K_M, which should improve accuracy over the basic Q4_0.

First, let's ask about the usages:

<a name="llama31-usages"></a>
> **Q: State the possible usages of Gaia Sky.**
>
> Gaia Sky is a free, open-source planetarium software that can be used for various purposes, including:
> 
> 1. **Educational purposes**: Gaia Sky can be used in educational settings to teach astronomy and astrophysics concepts to students.
> 2. **Research and scientific visualization**: The software's advanced features make it suitable for researchers who need to visualize complex astronomical data, such as star catalogs, galaxy distributions, or planetary systems.
> 3. **Public outreach and engagement**: Gaia Sky can be used in public events, exhibitions, or planetariums to showcase the wonders of the universe and promote interest in astronomy among the general public.
> 4. **Personal entertainment**: Users can simply enjoy exploring the night sky, viewing celestial objects, and experiencing the thrill of space travel within the software's virtual environment.
> 5. **Artistic and creative projects**: Gaia Sky's capabilities make it an attractive tool for artists, designers, and filmmakers who need to create realistic astronomical environments or simulate complex astrophysical phenomena.
> 6. **Professional training and development**: The software can be used by professionals in fields like astronomy, space exploration, or related industries to improve their knowledge and skills through interactive simulations and visualizations.
> 
> These are just a few examples of the many possible usages of Gaia Sky. Its versatility and flexibility make it an excellent tool for various applications across different domains.

This is a good response. Not too long, and very well organized. Everything in it is correct, too. Also, Llama 3.1 was very fast in generating it.

The next question is about the Linux installation.

<a name="llama31-linux"></a>
>**Q: How do I install Gaia Sky on Linux?**
>
> To install Gaia Sky on Linux, you can follow these steps for the different package types:
>
> **Flatpak**
> 
> 1. Install Flatpak if you haven't already:
>    ```bash
>    sudo apt-get install flatpak
>    ```
> 2. Add the Flathub repository:
>    ```
>    flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
>    ```
> 3. Install Gaia Sky from Flathub:
>    ```bash
>    flatpak install flathub space.gaiasky.GaiaSky
>    ```
> 4. Run Gaia Sky:
>    ```
>    flatpak run space.gaiasky.GaiaSky
>    ```
> 
> **AppImage**
> 
> 1. Download the AppImage file from the official website: https://gaiasky.space/downloads/
> 2. Make the AppImage executable:
>    ```bash
>    chmod +x gaiasky_x86_64.AppImage
>    ```
> 3. Run Gaia Sky:
>    ```
>    ./gaiasky_x86_64.AppImage
>    ```
> 
> **Unix Installer (tarball)**
> 
> 1. Download the tarball from the official website: https://gaiasky.space/downloads/
> 2. Extract the contents of the tarball to a directory of your choice:
>    ```bash
>    tar -xvf gaiasky.tar.gz
>    ```
> 3. Run Gaia Sky:
>    ```
>    ./gaiasky.sh
>    ```
> 
> **DEB (Debian and derivatives)**
> 
> 1. Download the DEB package from the official website: https://gaiasky.space/downloads/
> 2. Install the package using dpkg:
>    ```bash
>    sudo dpkg -i gaiasky_3.6.7_amd64.deb
>    ```
> 3. Run Gaia Sky:
>    ```
>    gaiasky
>    ```
> 
> **RPM (RedHat and derivatives)**
> 
> 1. Download the RPM package from the official website: https://gaiasky.space/downloads/
> 2. Install the package using rpm:
>    ```bash
>    sudo rpm -i gaiasky-3.6.7-x86_64.rpm
>    ```
> 3. Run Gaia Sky:
>    ```
>    gaiasky
>    ```
> 
> **AUR (Arch Linux and derivatives)**
> 
> 1. Install the AUR helper of your choice (e.g., yay, yay-bin).
> 2. Clone the Gaia Sky AUR package repository:
>    ```bash
>    git clone https://aur.archlinux.org/gaiasky.git
>    ```
> 3. Navigate to the cloned repository directory:
>    ```
>    cd gaiasky
>    ```
> 4. Build and install the package:
>    ```bash
>    makepkg -si
>    ```
> 5. Run Gaia Sky:
>    ```
>    gaiasky
>    ```

This answer is **fracking excellent**. It nails everything. It includes all Linux packages we offer, and the instructions for each are on point. I'm super impressed. The quality of this response is much better than the one generated by the (much larger) Mistral Small 3 22B.

Finally, we ask it what cubemaps are used for:

<a name="llama31-cubemaps"></a>
> **Q: How are cubemap textures used in Gaia Sky?**
> 
> In Gaia Sky, cubemap textures are used to display planetary surfaces and other 3D models with high detail and realism. Here's an overview of how they work:
> 
> **What is a cubemap?**
> 
> A cubemap is a type of texture that represents the surface of a 3D object from all six sides (top, bottom, left, right, front, and back). It's called a "cubemap" because it's essentially a cube with six faces, each containing a different view of the object.
> 
> **How are cubemaps used in Gaia Sky?**
> 
> In Gaia Sky, cubemaps are used to display planetary surfaces, such as Earth or other planets. When you load a planet into the game, Gaia Sky generates a cubemap texture that represents the surface of the planet from all six sides. This allows for more detailed and realistic rendering of the planet's surface.
> 
> **How do cubemaps improve graphics in Gaia Sky?**
> 
> Cubemaps offer several benefits over traditional textures:
> 
> 1. **Higher detail**: Cubemaps can display much higher levels of detail than traditional textures, making planetary surfaces look more realistic.
> 2. **Realistic lighting**: Cubemaps take into account the way light interacts with the surface of the planet, creating a more realistic and immersive experience.
> 3. **Improved performance**: Because cubemaps are pre-computed and stored in memory, they can be rendered much faster than traditional textures, reducing the load on your graphics card.
> 
> **How to use cubemap textures in Gaia Sky**
> 
> To use cubemap textures in Gaia Sky, you'll need to:
> 
> 1. Load a planet or other 3D model into the game.
> 2. Adjust the graphics settings to enable cubemaps (this may require updating to a newer version of Gaia Sky).
> 3. Select the desired level of detail and lighting for the cubemap texture.
> 
> By using cubemap textures, Gaia Sky can create stunningly realistic planetary surfaces that draw you in and make you feel like you're exploring the cosmos itself!

The format and wording of this answer look like it comes from a larger model. However, I think the content misses the point a bit. It does not look like it sources this information from the [Cubemaps section](https://gaia.ari.uni-heidelberg.de/gaiasky/docs/master/Cubemaps.html) in our documentation, which may be an issue with the embedding, the context size, or the context retrieval. I tried reducing the number of results from 10 to 5 before running the query again:

> **How are cubemaps used in Gaia Sky?**
> 
> Cubemaps are used in Gaia Sky to texture planets, moons, and other spherical or semi-spherical objects. They help eliminate artifacts that happen at the poles with UV sphere models, providing a more seamless appearance. Cubemaps can be used instead of regular equirectangular (spherically projected) images.

This time around, the answer is much more concise and correct.

In the global picture, I like the responses of Llama better than those provided by Mistral. Also, Mistral is almost 3 times larger than Llama (22B vs 8B), so it is much slower on my machine.

## Performance

In my case, I'm pretty limited by my hardware, and responses tend to be slow with the larger model (Mistral). The speed is quite good with Llama (8B) though. True, I'm running this a very old computer for today's standards (Intel(R) Core(TM) i7-7700 (8) @ 4.20 GHz, NVIDIA GeForce GTX 1070 8 GB, 32 GB RAM), so it is what it is. 

Here are the performance stats for both models. I asked them both to generate a short text (~100 words) about the meaning of life.

<span style="font-size: small">

| Model                      | Total Duration       | Prompt Eval Rate | Eval Count   | Eval Duration      | Eval Rate |
| -------------------------- | -------------------- | ---------------- | ------------ | ------------------ | --------- |
| `mistral-small:22b-instruct-2409-q4_K_M` | 24.575599226s        | 53.56 tokens/s    | 67 token(s)   | 23.194348749s      | 2.89 tokens/s |
| `llama3.1:8b-instruct-q5_K_M`    | 7.825027246s         | 109.12 tokens/s   | 119 token(s)  | 7.526260082s       | 15.81 tokens/s |

</span>

I found the responses provided by smaller models (1B to 5B) to be mostly garbage. On larger instruct models with decent quantization, accuracy is greatly improved at the expense of your precious time.

## Conclusion

In this post, we've expanded on our previous post and developed an AI chatbot able to answer questions on Gaia Sky. The information is sourced from the Gaia Sky homepage and documentation. With the power of web scraping, embeddings, and Ollama, we've brought the Gaia Sky website and docs to life with smart, context-aware interactions. No more endless searches for answers. Instead, we now have a chatbot that knows exactly where to look and can provide concise, relevant responses. So go ahead and try it out---who knew scraping could be this useful?

It's pretty obvious to me that such small models are able to get most of the questions *almost* right, but they are most definitely not suited for professional settings. In this case, larger models (at least 70B, I reckon) would be required. For our purposes here, Mistral Small 3 instruct (22B) and Llama 3.1 instruct (8B) are enough.

I don't want to finish without mentioning off-the-shelf options that accomplish the same goals. There exist no-code software packages like [AnythingLLM](https://anythingllm.com/) and [Open WebUI](https://openwebui.com/) that support local models via Ollama and integrate RAG. I actually recommend using these if you are not too interested in the nitty-gritty details.

