## Repository Structure
For the structure of the repository I have refered the chats with Perplexity, and ChatGPT  
[Chat with Perplexity](https://www.perplexity.ai/search/best-folder-structure-for-full-tLSblRSNTY.tMZqA0wfocw)  
[Chat with ChatGPT](https://chatgpt.com/share/4b3f49f4-b81c-47df-811d-8cd0bcf489fc)  

---

# Agentic RAG

There is a bug in llama-index with SimpleDocumentLoader where I was not able to directly run it.
The work around which I found around this issue was using the following import statment:  
`from llama_index.readers.file.docs.base import PDFReader`  
And also installing the unstructured python package by:  
`pip install unstructured`
