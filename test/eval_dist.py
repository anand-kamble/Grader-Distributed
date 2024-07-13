# %%
#!pip install ragas datasets llama-index nest-asyncio
import os
import time
import concurrent.futures
import asyncio
from h11 import Data
from ragas.integrations.llama_index import evaluate
from ragas.metrics.critique import harmfulness
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,

)
import json
from llama_index.core.settings import Settings
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.llms.ollama import Ollama
from llama_index.core.llama_dataset import download_llama_dataset
from llama_index.core.llama_pack import download_llama_pack
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.ollama import OllamaEmbedding
from ragas.testset.evolutions import simple, reasoning, multi_context, conditional
from datasets import Dataset
from pandas import DataFrame
from typing import List
import nest_asyncio
nest_asyncio.apply()

################## CONSTANTS ##################

MACHINES = [
    "class01", "class02", "class03", "class04", "class05",
    "class06", "class07", "class08", "class09", "class10",
    "class11", "class12", "class13", "class14", "class15",
    "class16", "class17", "class18", "class19"
]

GENERATION_MODEL = "llama3"
EMBEDDING_MODEL = "llama3"
REQUEST_TIMEOUT = 240

# This is needed since I am using a single machine to create the
EMBEDDING_MACHINE = "class01"
# embeddings which will be used for all the machines.


# Used to store the VectorIndex so we don't have to compute it again.
PERSIST_DIR = "./index_storage"

BENCHMARK_LOG = "./benchmark_log.txt"

################## END OF CONSTANTS ##################


# Download the LLaMA dataset for evaluation, specifying the dataset name and the local storage path.
rag_dataset, documents = download_llama_dataset(
    "EvaluatingLlmSurveyPaperDataset", "./data"
)

# %%################## INITIALIZE EMBEDDING MODEL ##################
# Initialize the embedding model with the specified model name and the base URL of the embedding service.
embeddings = OllamaEmbedding(
    model_name=EMBEDDING_MODEL, base_url=f"http://{EMBEDDING_MACHINE}:11434")
# Update the global settings to use the initialized embeddings model for further processing.
Settings.embed_model = embeddings


# %%################## INITIALIZE VECTOR INDEX ##################
# Initialize the vector index as None. This will be used to store the vector index either loaded from storage or created anew.
vector_index = None

# Check if the persistent storage directory exists.
if os.path.exists(PERSIST_DIR):
    # If it exists, create a storage context with default settings and the specified persistent directory.
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    # Load the index from the storage using the created storage context.
    vector_index = load_index_from_storage(storage_context)
    print("Loaded existing index from storage")
else:
    # If the persistent directory does not exist, create a new vector index from the documents.
    vector_index = VectorStoreIndex.from_documents(documents)
    # Persist the newly created index to the specified persistent directory.
    vector_index.storage_context.persist(persist_dir=PERSIST_DIR)
    print("Created and saved new index")

# Create a vector index from the downloaded documents for efficient similarity searches.
# vector_index = VectorStoreIndex.from_documents(documents=documents)
# generator_llm = Ollama(base_url="http://class01:11434",
# model="llama3", request_timeout=240)
# query_engine = vector_index.as_query_engine(llm=generator_llm)

# For testing distributed evaluation I am using the same model for all the critic, evaluator and generator
# %%
rag_dataset_df: DataFrame = rag_dataset.to_pandas()
rag_dataset_df.to_dict().keys()


dataset = dict()

dataset["question"] = rag_dataset_df["query"].tolist()[:2]
dataset["ground_truth"] = rag_dataset_df["reference_answer"].tolist()[:2]

metrics = [
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
    harmfulness,
    # max_workers = 24 # Found this argument from the RunConfig dataclass.
]

# result = evaluate(
#     query_engine=query_engine,
#     metrics=metrics,
#     dataset=dataset,
#     llm=generator_llm,
#     embeddings=OllamaEmbedding(
#         model_name="phi3:latest", base_url="http://class01:11434"),
# )

# %%


def create_query_engine(machine: str):
    generator_llm = Ollama(
        base_url=f"http://{machine}:11434", model=GENERATION_MODEL, request_timeout=REQUEST_TIMEOUT)
    query_engine = vector_index.as_query_engine(llm=generator_llm)
    print(f"Created query engine for machine: {machine}")
    return query_engine, generator_llm

# %%


def split_dataset(num_machines: int = len(MACHINES)):
    total_size = len(dataset['question'])
    # num_machines = len(MACHINES[:num_machines])

    # If the number of questions is less than the number of machines,
    # assign at least one question to each machine, if available
    if total_size < num_machines:
        split_datasets = []
        for i in range(total_size):
            split_dataset = {
                "question": [dataset['question'][i]],
                "ground_truth": [dataset['ground_truth'][i]]
            }
            split_datasets.append(split_dataset)

        # Fill remaining machines with empty datasets
        for _ in range(num_machines - total_size):
            split_datasets.append({"question": [], "ground_truth": []})
    else:
        split_size = total_size // num_machines
        split_datasets = []

        for i in range(num_machines):
            start = i * split_size
            end = (i + 1) * split_size if i != num_machines - 1 else total_size
            split_dataset = {
                "question": dataset['question'][start:end],
                "ground_truth": dataset['ground_truth'][start:end]
            }
            split_datasets.append(split_dataset)

    return split_datasets

# %%


def evaluate_on_machine(machine: str, split_dataset):
    query_engine, generator_llm = create_query_engine(machine=machine)
    metrics = [
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
        harmfulness,
    ]
    print(f"Starting evaluation on machine: {machine}")
    print(f"Split dataset: {split_dataset}")
    if split_dataset["question"] == [] or split_dataset["ground_truth"] == []:
        print(f"Empty dataset for machine: {machine}")
        return None

    result = evaluate(
        raise_exceptions=False,
        query_engine=query_engine,
        metrics=metrics,
        dataset=split_dataset,
        llm=generator_llm,
        embeddings=OllamaEmbedding(
            model_name=EMBEDDING_MODEL, base_url=f"http://{machine}:11434")
    )
    return result

# %%


def distribute_evaluation():
    split_datasets = split_dataset()
    results = []

    for i, base_url in enumerate(MACHINES):
        result = evaluate_on_machine(base_url, split_datasets[i])
        results.append(result)
        print(f"Evaluated on machine: {base_url}")
        print(result)

    return results


# %%
executor = concurrent.futures.ThreadPoolExecutor()


async def async_task(base_url, split_datasets):
    result = await asyncio.get_running_loop().run_in_executor(executor, evaluate_on_machine, base_url, split_datasets)
    print(f"Evaluated on machine: {base_url}")

    return result


async def main(num_machines):
    responses = []
    # for i in range(len(queries)):
    #     task = asyncio.create_task(self.async_task(
    #         queries[i], i % len(self.machines)))
    #     responses.append(task)

    split_datasets = split_dataset(num_machines)
    results = []

    for i, base_url in enumerate(MACHINES[:num_machines]):
        task = asyncio.create_task(async_task(base_url, split_datasets[i]))
        responses.append(task)

    results = await asyncio.gather(*responses)
    return results


def execute(num_machines):
    return asyncio.run(main(num_machines))


# %%
def benchmark():
    results = {}

    with open(BENCHMARK_LOG, "w") as f:
        f.write("Benchmark started\n")
        num_machines_list = [1, 2, 4, 8, 16, 19]

        for num_machines in num_machines_list:
            try:
                start_time = time.time()
                execute(num_machines)
                end_time = time.time()
                elapsed_time = end_time - start_time
                results[num_machines] = elapsed_time
                f.write(
                    f"Time taken with {num_machines} machines: {elapsed_time} seconds")
            except Exception as e:
                error_message = f"Error with {num_machines} machines: {str(e)}"
                f.write(error_message + "\n")
        
        f.write("\nBenchmark completed\n")
        
    executor.shutdown()
        
    return results

benchmark_results = benchmark()

# %%
