from typing import List, Callable, Any
import concurrent.futures
from timer import PerfCounterTimer
import multiprocessing


class TaskScheduler:

    def __init__(self, max_workers: int = multiprocessing.cpu_count(), timeout: int = 60):
        self.executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=max_workers
        )
        self.tasks = []
        self.failed_tasks = []
        self.futures = []
        self.timer = PerfCounterTimer()
        self.timeout = timeout

    def add_task(self, id: str, task: Callable[..., Any], *args):
        with PerfCounterTimer(id).timeit():
            future = self.executor.submit(task, *args)
            self.futures.append(future)
            self.tasks.append((task, args))
            future.add_done_callback(self._task_done)

    def _task_done(self, future):
        try:
            result = future.result()
            print(f"Task completed with result: {result}")
        except Exception as e:
            print(f"An error occurred: {e}")
            self.failed_tasks.append(self.tasks[self.futures.index(future)])

    def execute_tasks(self):
        concurrent.futures.wait(self.futures, timeout=self.timeout)

    def get_results(self):
        results = []
        for future in self.futures:
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"An error occurred: {e}")
                self.failed_tasks.append(
                    self.tasks[self.futures.index(future)])
        PerfCounterTimer.report()
        return results, self.failed_tasks
