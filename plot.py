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
# cohesion,separation,alignment_variance,clusters,isolated,peripheral,central
plt.figure(figsize=(12, 8))
plt.subplot(2, 2, 1)
plt.plot(data['time'], data['cohesion'])
plt.title('Cohesion')
plt.xlabel('Time')
plt.ylabel('Variance')
plt.subplot(2, 2, 2)
plt.plot(data['time'], data['separation'])
plt.title('Separation')
plt.xlabel('Time')
plt.ylabel('Variance')
plt.subplot(2, 2, 3)
plt.plot(data['time'], data['alignment_variance'])
plt.title('Alignment')
plt.xlabel('Time')
plt.ylabel('Variance')
plt.subplot(2, 2, 4)
plt.plot(data['time'], data['clusters'], label='Clusters')
plt.plot(data['time'], data['isolated'], label='Isolated')
plt.plot(data['time'], data['connected'], label='Connected')
plt.title('Clusters')
plt.xlabel('Time')
plt.ylabel('Variance')
plt.legend()
plt.show()