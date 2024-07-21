# Benchmark.py

In this file I have created a ollama_distributed class which has following methods to distribute the querying tasks.

## `get_llm`
Generate an Ollama object with unique base url which will use a specified machine. This is using the `self.machines` array to generate the URL, these machines are specified while constructing the `ollama_distributed` class.

```python
    def get_llm(self, index):
        base_url = f"http://{self.machines[index]}:11434"
        print(f"Generated LLM with Base URL: {base_url}")
        return Ollama(base_url=base_url, model=self.model, request_timeout=self.request_timeout)
```

## `query`

This is simple function which queries the given text to the machine specified by index.

```python
    def query(self, text: str, index: int):
        llm = self.get_llm(index)
        response = llm.complete(text)
        return response
```

## `async_task`

This function is converting the `query` function into an asynchronous function using the `asyncio` library. 

```python
    async def async_task(self, text, index):
        result = await asyncio.get_running_loop().run_in_executor(self.executor, self.query, text, index)
        return result
```

## `main`

The main method in this class which creates and executes the tasks for all the provided queries across all the machines and then gathers the results. It ensures that the queries are distributed evenly across the available machines.

```python 

async def main(self, queries):
        responses = []
        for i in range(len(queries)):
            task = asyncio.create_task(self.async_task(
                queries[i], i % len(self.machines)))
            responses.append(task)

        results = await asyncio.gather(*responses)
        self.executor.shutdown()
        return results

```

# Improvments 

Currently this method evenly distributes the qureies across all the machines which is like the `Round Robin` algorithm, but it can have bottnecks in case one machine gets stuck.  
In next version I will be trying to implement the dynamic distribution to make it more efficient.