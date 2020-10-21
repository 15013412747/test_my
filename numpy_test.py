# -- coding: utf-8 --

import numpy as np

count_h = 5400
count_t = 1000

T = np.arange(count_h) + np.arange(count_t)[:, np.newaxis]

T2 = np.arange(count_h) + np.arange(10)[:, np.newaxis]

print(T2)
print(T.shape)

# T = np.arange(count_h) + np.arange(count_t)[:, np.newaxis]

print(T)
