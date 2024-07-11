import asyncio
import concurrent.futures
from typing import List
from fastapi import responses
from llama_index.llms.ollama import Ollama
import time

class ollama_distributed():
    def __init__(self, model: str, machines: List[str] = [], request_timeout: int = 60):
        self.machines = machines
        self.model = model
        self.request_timeout = request_timeout
        self.executor = concurrent.futures.ThreadPoolExecutor()

    def get_llm(self, index):
        base_url = f"http://{self.machines[index]}:11434"
        print(f"Generated LLM with Base URL: {base_url}")
        return Ollama(base_url=base_url, model=self.model, request_timeout=self.request_timeout)

    def query(self, text: str, index: int):
        llm = self.get_llm(index)
        response = llm.complete(text)
        return response

    async def async_task(self, text, index):
        result = await asyncio.get_running_loop().run_in_executor(self.executor, self.query, text, index)
        return result

    async def main(self, queries):
        responses = []
        for i in range(len(queries)):
            task = asyncio.create_task(self.async_task(
                queries[i], i % len(self.machines)))
            responses.append(task)

        results = await asyncio.gather(*responses)
        self.executor.shutdown()
        return results

    def execute(self,queries):
        return asyncio.run(self.main(queries))


machines = [
    "class01", "class02", "class03", "class04", "class05",
    "class06", "class08", "class09", "class10",
    "class11", "class12", "class13", "class14", "class15",
    "class16", "class17", "class18", "class19"
]

queries = [
    "Summarize 'War and Peace' by Leo Tolstoy in detail, highlighting the main plot points, character arcs, and thematic elements.",
    "Explain the entire process of protein synthesis, from transcription to post-translational modification, including all key steps and molecular players involved.",
    "Analyze the impact of the Industrial Revolution on global economic structures, considering both short-term and long-term effects across different regions and industries.",
    "Describe the history of quantum mechanics, including key experiments, theoretical developments, and the contributions of major scientists.",
    "Create a comprehensive guide on the application of machine learning in healthcare, covering various use cases, ethical considerations, and potential future developments.",
    "Write a detailed comparison between classical Newtonian mechanics and Einstein’s theory of relativity, including mathematical formulations, experimental verifications, and practical implications.",
    "Develop a thorough critique of Shakespeare's use of language and dramatic techniques in 'Hamlet,' with specific examples and scholarly references.",
    "Explain the workings of a modern democratic government, detailing the roles and interactions between the executive, legislative, and judicial branches, using a specific country as an example.",
    "Provide an extensive overview of the history, cultural significance, and major milestones of the Olympic Games from ancient Greece to the present day.",
    "Write a detailed tutorial on how to set up and configure a Kubernetes cluster from scratch, including explanations of key concepts, best practices, and common pitfalls."
]



# ollama = ollama_distributed(
#     machines=machines, model="llama3", request_timeout=240)

# res = ollama.execute(queries)
# print("Results: ", res)


def benchmark(model, machines, queries, filename):
    with open(filename, "w") as file:
        for i in range(1, len(machines) + 1):
            subset_machines = machines[:i]
            ollama = ollama_distributed(machines=subset_machines, model=model, request_timeout=240)

            try:
                start_time = time.time()
                res = ollama.execute(queries)
                end_time = time.time()

                duration = end_time - start_time
                result = f"{i} machines: {duration} seconds"
                print(result)
                file.write(result + "\n")

            except Exception as e:
                error_message = f"Error with {i} machines: {str(e)}"
                print(error_message)
                file.write(error_message + "\n")

benchmark(model="llama3", machines=machines, queries=queries, filename="benchmark_timings.txt")