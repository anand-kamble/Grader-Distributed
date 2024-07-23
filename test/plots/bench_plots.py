#%%
from matplotlib.pylab import rand
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

#%%
random = pd.read_csv("../results/static_results_with_10000_1721760000.3070996.csv")
# %%
random["base_url"].hist()
# %%
timings = random["end_time"] - random["start_time"]
# %%
dfs = {base_url:data for base_url, data in random.groupby("base_url")}
average_durations = {base_url:np.mean(data["end_time"] - data["start_time"]) for base_url, data in dfs.items()}

# %% Plot the Average durations for each base URL
plt.figure(figsize=(10, 6),dpi=600)
plt.bar(average_durations.keys(), average_durations.values(), color='blue')
plt.xlabel('Base URL')
plt.ylabel('Average Duration (seconds)')
plt.title('Average Duration for each query with Round Robin')
plt.xticks(rotation=90)
plt.show()

#%% Plot the number of queries for each base URL
plt.figure(figsize=(10, 6),dpi=600)
plt.xlabel('Base URL')
plt.ylabel('Number of Queries')
plt.title('Number of Queries for Each Machine with Round Robin')
random_copy = random.copy()
random_copy["base_url"].value_counts().sort_index().plot(kind='bar')
# %%
