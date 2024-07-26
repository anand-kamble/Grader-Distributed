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


# Test

For running the tests first go into the test directory.
```bash
cd test
```

1. Start all the Ollama servers.
```bash
. ./spawn_ollamas.sh
```

Make sure to run this command from a non classroom computer, I am using `laforge` machine which is in the intelligence lab.

2. Start the benchmark in a new terminal by going into the test folder.
```bash
python benchmark.py
```

OR

```bash
python eval_dist.py
```

# Benchmarking

All the benchmarking is done using `llama-index` and `Ollama`.
You can find the details in the [benchmark.md](./test/benchmark.md)