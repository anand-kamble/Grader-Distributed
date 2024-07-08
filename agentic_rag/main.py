# %%
import os
from llama_index.core.tools import QueryEngineTool
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.settings import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.readers.file.docs.base import PDFReader

# %%
documents = SimpleDirectoryReader("documents/").load_data(show_progress=True)
# %%
available_machines = ['class01', 'class02']

# %%
embeddings:list[OllamaEmbedding] = list()

for machine in available_machines:
    embeddings.append(OllamaEmbedding(base_url=f"http://{machine}:11434", model_name="llama3",
                                      ))

# %%
embeddings[0].get_text_embedding_batch(["hello world", "goodbye world"])