import requests
import random
import time
from task_scheduler import TaskScheduler


def call_api(machine: str):
    res = requests.get(f"http://{machine}:11434/")
    time.sleep(random.uniform(1, 5))
    return res.text


MACHINES = [
    "class01", "class02", "class03", "class04", "class05",
    "class06", "class07", "class08", "class09", "class10",
    "class11", "class12", "class13", "class14", "class15",
    "class16", "class17", "class18", "class19"
]

ts = TaskScheduler()

# Dynamically add tasks to the scheduler
for machine in MACHINES:
    ts.add_task(machine, call_api, machine)
    time.sleep(0.1)  # Simulate dynamic task addition

ts.execute_tasks()

results, failed_tasks = ts.get_results()

print("Results:", results)
print("Failed tasks:", failed_tasks)
