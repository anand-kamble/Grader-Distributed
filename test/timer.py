import time
import numpy as np
from contextlib import contextmanager
from collections import defaultdict
import pandas as pd

class PerfCounterTimer:
    timings = defaultdict(list)

    columns = ["name", "min", "mean", "std", "count"]
    df = pd.DataFrame(columns=columns)

    def __init__(self, name=""):
        self.name = name

    @contextmanager
    def timeit(self, count: int = 1):
        start_time = time.perf_counter()
        yield
        end_time = time.perf_counter()
        # Time for each occurrence
        elapsed_time = (end_time - start_time) / count
        PerfCounterTimer.timings[self.name].append(elapsed_time)

    @classmethod
    def reset(cls):
        cls.timings = defaultdict(list)

    def __call__(self, count: int = 1):
        return self.timeit(count)

    @classmethod
    def report(cls, msg="") -> defaultdict:
        out_dict = defaultdict(dict)
        if msg:
            print(f"\n{msg}")
        for name, times in cls.timings.items():
            out_dict[name] = {}
            mean_total_time = np.mean(times)
            std_total_time = np.std(times)
            min_total_time = np.min(times)
            out_dict[name]["mean"] = mean_total_time
            out_dict[name]["std"] = std_total_time
            out_dict[name]["min"] = min_total_time
            counter = len(times)
            out_dict[name]["count"] = counter
            print(
                f"Name: {name}, Count: {counter}, Total Time: {min_total_time:7.4f} seconds, "
                + f"Timings: {mean_total_time / counter:7.4f} each"
            )
        print()
        # Update the DataFrame with the new data
        data_dict = defaultdict(dict)
        for name, times in cls.timings.items():
            mean_total_time = np.mean(times)
            std_total_time = np.std(times)
            min_total_time = np.min(times)
            counter = len(times)
            data_dict[name]["name"] = name
            data_dict[name]["mean"] = mean_total_time
            data_dict[name]["std"] = std_total_time
            data_dict[name]["min"] = min_total_time
            data_dict[name]["count"] = counter

        # Update the DataFrame with data from data_dict
        new_rows = pd.DataFrame.from_dict(data_dict, orient="index")
        cls.df = pd.concat([cls.df, new_rows], ignore_index=True)

    @classmethod
    def get_dataframe(cls) -> pd.DataFrame:
        return cls.df

    # ----------------------------------------------------------------------
    # def update_dataframe(df: pd.DataFrame | None, data_dict: defaultdict) -> pd.DataFrame:
    #     """
    #     Appends data from a dictionary to a DataFrame and returns the updated DataFrame.

    #     Parameters:
    #     df (pd.DataFrame): The pre-initialized DataFrame.
    #     data_dict (dict): The dictionary containing data to append.

    #     Returns:
    #     pd.DataFrame: The updated DataFrame with the new data appended.
    #     """
    #     # Initialize the DataFrame if it does not exist
    #     print("data_dict")
    #     pprint(data_dict)
    #     print()
    #     if df is None:
    #         df = pd.DataFrame(columns=["name"] + list(data_dict.keys()))

    #     # Convert data_dict to a DataFrame-compatible format
    #     data_to_append = pd.DataFrame(data_dict, columns=["name"] + list(data_dict.keys()))

    # Append the data to the DataFrame
    # updated_df = pd.concat([df, data_to_append], ignore_index=True)

    # return updated_df


# ----------------------------------------------------------------------

if __name__ == "__main__":
    # Usage example
    timer = PerfCounterTimer()

    # Simulating multiple timed blocks
    with PerfCounterTimer("gordon").timeit():
        time.sleep(0.5)
    with PerfCounterTimer("gordon").timeit():
        time.sleep(0.5)

    with PerfCounterTimer("frances").timeit():
        time.sleep(0.7)
    with PerfCounterTimer("frances").timeit():
        time.sleep(0.7)

    with PerfCounterTimer("ggordon").timeit():
        time.sleep(0.3)
    with PerfCounterTimer("ggordon").timeit():
        time.sleep(0.3)

    # Print the report
    PerfCounterTimer.report()