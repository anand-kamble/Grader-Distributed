from typing import List, Callable, Any
import concurrent.futures
from urllib import response
import requests
import random
import time


class task_scheduler:
    def __init__(self):
        self.executor = concurrent.futures.ThreadPoolExecutor()
        self.tasks = []
        self.failed_tasks = []


    def add_task(self, task: Callable[..., Any], *args):
        self.tasks.append((task, args))

    def execute_tasks(self):
        futures = []
        for i, (task, args) in enumerate(self.tasks):
            futures.append(self.executor.submit(task, *args))
        concurrent.futures.wait(futures)
        
        results = [future.result() for future in futures]
        
        for future in futures:
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"An error occurred: {e}")
                self.failed_tasks.append(self.tasks[futures.index(future)])
        
        return results, self.failed_tasks


def call_api(machine: str):
    res = requests.get(f"http://{machine}:11434/")
    time.sleep(random.uniform(1, 5))
    return res.text

MACHINES = [
    "class01", "class02", "class03", "class04", "class05",
    "class06", "class07", "class08", "class09", "class10",
    "class11", "class22s", "class13", "class14", "class15",
    "class16", "class17", "class18", "class19"
]

ts = task_scheduler()

for machine in MACHINES:
    ts.add_task(call_api, machine)

results = ts.execute_tasks()

print(results)
