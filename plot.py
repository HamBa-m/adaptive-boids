# plot the variance history of the model
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

# load the data
data = pd.read_csv('variance_history.csv')
data = data.dropna()

# plot the data
plt.figure()
plt.plot(data['variance'], label='variance')
plt.xlabel('epoch')
plt.ylabel('variance')
plt.legend()
# save the plot
plt.savefig('figs/variance_history_' + str(time.time()) + '.png')
plt.show()