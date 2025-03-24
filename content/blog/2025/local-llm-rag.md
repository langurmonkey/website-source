+++
author = "Toni Sagrista Selles"
categories = ["AI"]
tags = ["LLM", "AI", "ollama", "RAG"]
date = 2025-03-24
linktitle = ""
title = "Local LLM with Retrieval-Augmented Generation"
description = "Let's build a simple RAG application using a local LLM through Ollama."
featuredpath = "date"
type = "post"
+++

Over the past few months I have been running local <abbr title="Large Language Model">LLMs</abbr> on my computer with various results, ranging from 'unusable' to 'pretty good'.
Local LLMs are becoming more powerful, but they don't inherently "know" everything. They're trained on massive datasets, but those are typically static. To make LLMs truly useful for specific tasks, you often need to augment them with *your own* data--data that's constantly changing, specific to your domain, or not included in the LLM's original training. The technique known as <abbr title="Retrieval Augmented Generation">RAG</abbr> aims to bridge this problem by embedding context information into a vector database that is later used to provide context to the LLM, so that it can *expand* its knowledge beyond the original training dataset. In this short article, we'll see how to build a very *primitive* local AI chatbot powered by Ollama with RAG capabilities.

<!--more-->

## Ingredients and set-up

In order to build our AI chatbot, we need the following ingredients:

- Ollama, to facilitate access to different LLMs.
- Chroma DB, our vector storage for our context.
- Langchain, to facilitate the integration of our RAG application with the LLM.

First, we need to install Ollama. On Arch Linux, it is in the `extra` repository. If you happen to have an NVIDIA GPU that supports CUDA, you're in luck. You can speed-up your inference but a significant factor! Otherwise, you can still just use the CPU. I have a (rather old) NVIDIA GPU, so I'm installing `ollama-cuda` as well.

```bash
pacman -S ollama ollama-cuda
```

Next, we need some LLM models to run locally. First, start the Ollama service.

```bash
systemctl start ollama.service
```

You can check whether the service is running with curl:

```bash
$ curl http://localhost:11434
Ollama is running%
```

Then, you need to get some LLM models. I have some installed that I use regularly:

```bash
$ ollama list
NAME                     ID              SIZE      MODIFIED    
llama3.1:8b              46e0c10c039e    4.9 GB    2 hours ago    
gemma3:12b               6fd036cefda5    8.1 GB    10 days ago    
phi4-mini:latest         78fad5d182a7    2.5 GB    10 days ago    
deepseek-coder-v2:16b    63fb193b3a9b    8.9 GB    10 days ago    
llama3.2:1b              baf6a787fdff    1.3 GB    4 weeks ago    
mistral-small:24b        8039dd90c113    14 GB     7 weeks ago    
phi4:latest              ac896e5b8b34    9.1 GB    7 weeks ago    
```

I would recommend using `llama3.1:8b` ([link](https://ai.meta.com/blog/meta-llama-3-1/)) for this experiment, especially if you run a machine with little RAM. It is quite compact and works reasonably well[^1]. Get it with:

```bash
ollama pull llama3.1:8b
```

That's it for our LLM. Now, let's create a new directory for our RAG chatbot project, and let's install the dependencies.

```bash
mkdir rag-chat && cd rag-chat
pipenv install ollama langchain langchain-ollama chromadb overrides
```

This should install `python-ollama`, Langchain together with the `-ollama` hook, and Chroma DB.

## Ollama model setup

The code in this post is available [here](https://codeberg.org/langurmonkey/rag-llm). Now, let's create a file, `rag-chat.py`.

First, our chatbot will list all the available models and will ask for the model we want to use. This part is simple:

```python
#!python
# Import required libraries
from langchain_ollama import OllamaEmbeddings, OllamaLLM
import chromadb, requests, os, ollama

OLLAMA_URL = "http://localhost:11434"

models = ollama.list()
model_names = []
for m in models.models:
    model_names.append(m.model)

print("Available models:\n -", '\n - '.join(model_names))

# Ask the user the LLM model to use
llm_model = input("Model to use: ")

```

[^1]: https://artificialanalysis.ai/models/llama-3-1-instruct-8b

## Vector storage

Now, we need to initialize the ChromaDB client with a persistent storage. Our vector storage will be in the directory `chroma_db/`.

```python
# Configure ChromaDB
# Initialize the ChromaDB client with persistent storage in the current directory
chroma_client = chromadb.PersistentClient(path=os.path.join(os.getcwd(), "chroma_db"))

# Custom embedding function for ChromaDB (using Ollama)
class ChromaDBEmbeddingFunction:
    """
    Custom embedding function for ChromaDB using embeddings from Ollama.
    """
    def __init__(self, langchain_embeddings):
        self.langchain_embeddings = langchain_embeddings

    def __call__(self, input):
        # Ensure the input is in a list format for processing
        if isinstance(input, str):
            input = [input]
        return self.langchain_embeddings.embed_documents(input)

# Initialize the embedding using Ollama embeddings, with the chosen model
embedding = ChromaDBEmbeddingFunction(
    OllamaEmbeddings(
        model=llm_model,
        base_url=OLLAMA_URL
    )
)

# Define a collection for the RAG workflow
collection_name = "rag_collection_1"
collection = chroma_client.get_or_create_collection(
    name=collection_name,
    metadata={"description": "A collection for RAG with Ollama"},
    embedding_function=embedding  # Embedding function we defined before
)

```

## Provide context for retrieval

Once we have Chroma DB set up, with our collection and embedding function, we need to populate it. Here, we'll just use an array with text, but you could fetch this information from files easily.

In my example, I use a totally made up text (1), the abstract to a paper about characterizing atmospheres with JWST (2), and some information about the new Gaia Sky website. The first is made up, so the model can't know it. The second is a paper which came out much later than the model was published. The third is about the new Gaia Sky website, which was also created after the model.

```python
# Function to add documents to the ChromaDB collection
def add_documents_to_collection(documents, ids):
    """
    Add documents to the ChromaDB collection.
    
    Args:
        documents (list of str): The documents to add.
        ids (list of str): Unique IDs for the documents.
    """
    collection.add(
        documents=documents,
        ids=ids
    )

# Example: Add sample documents to the collection
documents = [
    "The Mittius is a sphere of radius 2 that is used to disperse light in all directions. The Mittius is very powerful and sometimes emits light in various wavelengths on its own. It is a completely fictional object whose only purpose is testing RAG in a local LLM.",
    "The newly accessible mid-infrared (MIR) window offered by the James Webb Space Telescope (JWST) for exoplanet imaging is expected to provide valuable information to characterize their atmospheres. In particular, coronagraphs on board the JWST Mid-InfraRed instrument (MIRI) are capable of imaging the coldest directly imaged giant planets at the wavelengths where they emit most of their flux. The MIRI coronagraphs have been specially designed to detect the NH3 absorption around 10.5 microns, which has been predicted by atmospheric models. We aim to assess the presence of NH3 while refining the atmospheric parameters of one of the coldest companions detected by directly imaging GJ 504 b. Its mass is still a matter of debate and depending on the host star age estimate, the companion could either be placed in the brown dwarf regime or in the young Jovian planet regime. We present an analysis of MIRI coronagraphic observations of the GJ 504 system. We took advantage of previous observations of reference stars to build a library of images and to perform a more efficient subtraction of the stellar diffraction pattern. We detected the presence of NH3 at 12.5 sigma in the atmosphere, in line with atmospheric model expectations for a planetary-mass object and observed in brown dwarfs within a similar temperature range. The best-fit model with Exo-REM provides updated values of its atmospheric parameters, yielding a temperature of Teff = 512 K and radius of R = 1.08 RJup. These observations demonstrate the capability of MIRI coronagraphs to detect NH3 and to provide the first MIR observations of one of the coldest directly imaged companions. Overall, NH3 is a key molecule for characterizing the atmospheres of cold planets, offering valuable insights into their surface gravity. These observations provide valuable information for spectroscopic observations planned with JWST.",
    "Gaia Sky has a new website built with Hugo. It contains download pages for all new and old versions of the software, and a full listing of all the catalogs and datasets offered with the software. The datasets can be downloaded in-app with the provided dataset manager."

]
doc_ids = ["doc_mittius", "doc_paper_jwst", "doc_gaiasky_web"]

# Documents only need to be added once or whenever an update is required. 
# This line of code is included for demonstration purposes:
add_documents_to_collection(documents, doc_ids)
```

## Finally, the chat logic

Now we have our vector storage set up. Let's build the chat logic!

```python
# Function to query the ChromaDB collection
def query_chromadb(query_text, n_results=3):
    """
    Query the ChromaDB collection for relevant documents.
    
    Args:
        query_text (str): The input query.
        n_results (int): The number of top results to return.
    
    Returns:
        list of dict: The top matching documents and their metadata.
    """
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    return results["documents"], results["metadatas"]

# Function to interact with the Ollama LLM
def query_ollama(prompt):
    """
    Send a query to Ollama and retrieve the response.
    
    Args:
        prompt (str): The input prompt for Ollama.
    
    Returns:
        str: The response from Ollama.
    """
    llm = OllamaLLM(model=llm_model)
    return llm.invoke(prompt)

# RAG pipeline: Combine ChromaDB and Ollama for Retrieval-Augmented Generation
def rag_pipeline(query_text):
    """
    Perform Retrieval-Augmented Generation (RAG) by combining ChromaDB and Ollama.
    
    Args:
        query_text (str): The input query.
    
    Returns:
        str: The generated response from Ollama augmented with retrieved context.
    """
    # Step 1: Retrieve relevant documents from ChromaDB
    retrieved_docs, metadata = query_chromadb(query_text)
    context = " ".join(retrieved_docs[0]) if retrieved_docs else "No relevant documents found."

    # Step 2: Send the query along with the context to Ollama
    augmented_prompt = f"Context: {context}\nQuestion: {query_text}\nAnswer: "
    print(augmented_prompt)

    response = query_ollama(augmented_prompt)
    return response

# Example usage
# Define a query to test the RAG pipeline
query = input("Query: ")
while query != "/bye":
    response = rag_pipeline(query)
    print(response)
    query = input("Query: ")
```

That's it! In this part, we ask the user to provide a query. Then, the script uses this query to fetch some context from our local Chroma DB, adds the context to the prompt (in `augmented_prompt`), and sends the query to Ollama. Then, we wait for the response and print it out.

Here is an example output (I'm omitting the context print). I ask it about JWST and exoplanets, the imaginary object Mittius, and the new Gaia Sky website. I have highlighted the response lines:

```bash {hl_lines=["22-36","43-48",54]}
$ rag-chat.py
Available models:
 - llama3.1:8b
 - gemma3:12b
 - phi4-mini:latest
 - deepseek-coder-v2:16b
 - llama3.2:1b
 - mistral-small:24b
 - phi4:latest
Model to use: llama3.1:8b
Insert of existing embedding ID: doc_mittius
Insert of existing embedding ID: doc_paper_jwst
Insert of existing embedding ID: doc_gaiasky_web
Add of existing embedding ID: doc_mittius
Add of existing embedding ID: doc_paper_jwst
Add of existing embedding ID: doc_gaiasky_web

Query: JWST and exoplanets.
Context: [...]
Question: JWST and exoplanets.
Answer: 
The James Webb Space Telescope (JWST) will play a significant role in exoplanet
research by providing new capabilities for characterizing their atmospheres.
The telescope\'s Mid-InfraRed instrument (MIRI) coronagraphs are capable of
imaging cold directly imaged giant planets and detecting specific molecules,
such as ammonia (NH3), which is a key indicator of surface gravity.

In the provided text, JWST is mentioned in the context of:

1. The newly accessible mid-infrared (MIR) window offered by JWST for exoplanet
   imaging.
2. The MIRI coronagraphs on board JWST are capable of detecting NH3 around
   10.5 microns.
3. Future spectroscopic observations planned with JWST will be guided by the
   valuable information obtained from these observations.

Overall, JWST is expected to provide new insights into exoplanet atmospheres and help scientists refine their understanding of these distant worlds.

Query: What is the radius of the Mittius?
Context: [...]
Question: What is the radius of the Mittius?
Answer:
The question doesn't relate to the provided text at all (about Gaia Sky
and MIRI coronagraphs) but rather mentions a fictional object called
"Mittius" which was mentioned in a separate context. The answer should
be taken directly from that initial context.

According to the initial description, the radius of the Mittius is 2.

Query: How was the new Gaia Sky website built?
Context: [...]
Question: How was the new Gaia Sky website built?
Answer: 
The new Gaia Sky website was built with Hugo.

Query: /bye
```

As you can see, even this small 8B parameter model pretty much nails all three answers. There is a weird rambling in the second question about the given context not including the Mittius info, but it still gets the answer right but referencing the 'initial' context.


## Conclusion

As we've seen, with very little effort we can build a rudimentary RAG system on top of Ollama. This enables us to use context information in our queries in an automated manner, with the help of Chroma DB. In our small test, we've used the Llama3.1 8B model, which is rather small. Using a larger model, like the Mistral-small (24B), or even the Gemma3 (12B) should improve the results at the expense of performance.

The code in this post is partially based on [this medium article](https://medium.com/@arunpatidar26/rag-chromadb-ollama-python-guide-for-beginners-30857499d0a0).
