# plot the variance history of the model
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import time

# load the data
data = pd.read_csv('statistics.csv')
data = data.dropna()

# add a time column (steps)
data['time'] = range(len(data))

# plot the data in subplots
plt.figure(figsize=(12, 8))
plt.subplot(2, 2, 1)
sns.lineplot(x='time', y='cohesion', data=data)
plt.title('Cohesion')
plt.xlabel('Time')
plt.ylabel('Cohesion')
plt.subplot(2, 2, 2)
sns.lineplot(x='time', y='separation', data=data)
plt.title('Separation')
plt.xlabel('Time')
plt.ylabel('Separation')
plt.subplot(2, 2, 3)
sns.lineplot(x='time', y='alignment_variance', data=data)
plt.title('Alignment Variance')
plt.xlabel('Time')
plt.ylabel('Alignment Variance')
plt.subplot(2, 2, 4)
sns.lineplot(x='time', y='clusters', data=data)
plt.title('Clusters')
plt.xlabel('Time')
plt.ylabel('Clusters')
plt.tight_layout()
plt.show()