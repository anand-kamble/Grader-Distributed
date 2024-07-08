# Start of section to add

import os
# import openai

# os.environ["OPENAI_API_KEY"] = "<Your API Key goes here>"


from llama_index.core.tools import QueryEngineTool
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.settings import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

 