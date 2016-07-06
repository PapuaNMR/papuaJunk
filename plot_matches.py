#!/usr/bin/env python

import argparse
import numpy as np
import matplotlib.pyplot as plt 

GB1_42Hz = [2, 4, 3, 2, 1, 3, 1, 1, 1, 3, 3, 2, 1, 5, 3, 2, 2, 3, 1, 1, 3, 7, 5, 1, 5, 2, 3, 1, 4, 3, 1, 2, 3, 4, 4, 2, 1, 3, 2, 1, 1, 2, 3, 5, 1, 5, 3, 3, 4, 3, 5, 1, 2, 1, 4, 1]

GB1_35Hz = [1, 2, 3, 1, 1, 3, 1, 1, 1, 3, 3, 1, 1, 5, 3, 2, 2, 3, 1, 1, 2, 5, 5, 1, 4, 2, 3, 1, 4, 3, 1, 2, 2, 4, 3, 1, 1, 3, 2, 1, 1, 2, 3, 4, 1, 5, 3, 3, 4, 3, 4, 1, 2, 1, 4, 1]

GB1_5_9Hz = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 3, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 0]


MBP_42Hz = [6, 4, 13, 9, 11, 9, 11, 12, 18, 3, 7, 5, 1, 17, 10, 3, 5, 11, 17, 4, 4, 11, 16, 10, 12, 11, 8, 3, 4, 13, 9, 3, 10, 10, 12, 3, 12, 9, 15, 12, 10, 12, 5, 8, 9, 14, 9, 6, 9, 0, 11, 14, 9, 11, 12, 6, 6, 10, 13, 10, 3, 2, 12, 12, 10, 12, 3, 13, 2, 2, 6, 16, 7, 11, 12, 17, 9, 9, 9, 11, 12, 5, 10, 16, 4, 15, 12, 11, 12, 13, 17, 3, 7, 3, 1, 9, 12, 2, 13, 12, 15, 8, 15, 3, 12, 7, 10, 2, 7, 9, 9, 4, 11, 14, 3, 13, 11, 14, 7, 11, 8, 14, 15, 14, 2, 9, 10, 13, 14, 11, 11, 9, 18, 12, 3, 6, 2, 2, 2, 10, 2, 3, 8, 9, 6, 3, 6, 9, 13, 10, 7, 11, 6, 16, 14, 1, 4, 15, 9, 12, 3, 5, 3, 2, 1, 5, 16, 11, 2, 16, 2, 12, 9, 3, 8, 11, 5, 14, 7, 10, 16, 12, 3, 5, 3, 1, 5, 9, 4, 12, 14, 15, 12, 2, 8, 2, 11, 9, 12, 17, 13, 6, 2, 0, 2, 7, 14, 12, 18, 4, 6, 13, 1, 2, 10, 5, 12, 9, 8, 12, 1, 2, 17, 9, 12, 2, 9, 2, 8, 13, 13, 12, 9, 16, 8, 9, 11, 5, 16, 11, 14, 13, 12, 12, 2, 16, 10, 11, 3, 10, 12, 10, 3, 12, 1, 4, 15, 5, 13, 4, 7, 11, 8, 11, 6, 12, 6, 14, 1, 12, 2, 11, 11, 2, 11, 15, 5, 14, 12, 8, 1, 5, 11, 10, 3, 14, 12, 7, 11, 12, 12, 9, 7, 12, 4, 8, 1, 10, 2, 5, 8, 6, 12, 13, 6, 11, 9, 7, 1, 4, 11, 11, 10, 17, 15, 12, 7, 1, 13, 5, 9, 14]


MBP_35Hz = [6, 4, 10, 9, 9, 8, 11, 9, 16, 3, 5, 5, 1, 14, 8, 2, 3, 11, 15, 4, 2, 10, 15, 8, 11, 10, 8, 3, 3, 13, 8, 3, 9, 10, 12, 2, 10, 8, 10, 12, 8, 10, 4, 7, 9, 10, 7, 5, 5, 0, 10, 13, 8, 9, 10, 5, 6, 10, 10, 6, 3, 2, 10, 12, 8, 11, 3, 10, 2, 1, 6, 15, 7, 9, 11, 13, 7, 8, 7, 11, 9, 4, 9, 14, 4, 15, 10, 10, 12, 10, 13, 2, 6, 3, 1, 9, 10, 1, 12, 12, 11, 6, 11, 3, 7, 5, 7, 2, 7, 8, 7, 4, 11, 12, 2, 10, 9, 12, 6, 10, 8, 13, 12, 11, 2, 7, 10, 10, 12, 10, 11, 7, 16, 10, 3, 4, 2, 2, 1, 7, 2, 2, 6, 7, 5, 2, 4, 7, 10, 8, 6, 11, 6, 15, 13, 1, 4, 11, 7, 11, 3, 5, 2, 2, 1, 5, 15, 11, 1, 12, 2, 11, 8, 3, 8, 10, 5, 12, 7, 7, 13, 12, 3, 3, 3, 1, 4, 9, 3, 10, 12, 13, 10, 2, 7, 2, 9, 8, 12, 11, 9, 6, 1, 0, 2, 7, 12, 11, 13, 4, 6, 11, 1, 2, 8, 5, 10, 9, 8, 11, 1, 2, 13, 9, 10, 2, 9, 2, 6, 12, 11, 10, 7, 14, 8, 8, 10, 5, 14, 9, 12, 13, 10, 11, 2, 14, 10, 10, 2, 9, 10, 7, 2, 10, 1, 3, 11, 5, 10, 3, 7, 9, 7, 10, 5, 12, 6, 11, 1, 10, 2, 10, 11, 2, 8, 11, 4, 11, 10, 6, 1, 5, 11, 8, 3, 11, 9, 6, 9, 12, 11, 8, 7, 10, 3, 6, 1, 7, 1, 4, 7, 5, 11, 13, 5, 11, 6, 7, 1, 4, 11, 8, 7, 15, 13, 10, 6, 1, 10, 4, 5, 13]

MBP_4_8Hz = [2, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1, 3, 1, 4, 1, 1, 1, 2, 5, 1, 1, 2, 4, 1, 2, 2, 4, 1, 1, 5, 2, 1, 1, 2, 2, 0, 4, 3, 2, 4, 1, 1, 0, 3, 4, 2, 2, 1, 1, 0, 1, 4, 2, 2, 1, 2, 2, 2, 3, 2, 1, 1, 1, 2, 1, 1, 2, 3, 2, 1, 2, 2, 0, 2, 4, 3, 3, 2, 1, 1, 1, 1, 1, 2, 1, 2, 3, 1, 4, 3, 3, 1, 1, 1, 1, 3, 2, 1, 1, 3, 5, 2, 2, 1, 1, 2, 2, 0, 1, 3, 2, 2, 2, 2, 0, 2, 2, 3, 1, 2, 3, 5, 5, 1, 2, 2, 3, 3, 5, 3, 2, 2, 2, 1, 0, 1, 1, 1, 0, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 5, 1, 3, 1, 2, 2, 2, 2, 1, 0, 1, 2, 2, 1, 1, 3, 2, 5, 1, 1, 2, 1, 2, 2, 1, 1, 2, 4, 1, 2, 1, 1, 1, 5, 1, 2, 1, 1, 1, 0, 2, 2, 2, 2, 4, 2, 2, 2, 1, 0, 1, 1, 2, 5, 2, 2, 2, 2, 1, 0, 2, 3, 3, 5, 3, 1, 1, 1, 3, 2, 3, 1, 0, 2, 2, 1, 2, 2, 1, 2, 1, 1, 1, 3, 3, 1, 5, 3, 2, 2, 1, 2, 2, 3, 1, 1, 2, 3, 0, 3, 1, 1, 1, 3, 1, 1, 2, 1, 2, 2, 1, 3, 2, 3, 0, 3, 1, 3, 3, 2, 2, 2, 1, 5, 1, 3, 1, 1, 4, 0, 1, 1, 2, 1, 2, 4, 2, 2, 2, 3, 1, 1, 1, 2, 1, 2, 1, 2, 2, 5, 2, 2, 1, 3, 1, 1, 1, 2, 1, 3, 2, 3, 1, 1, 1, 2, 1, 5]


combo = np.column_stack((GB1_5_9Hz, GB1_35Hz, GB1_42Hz))

bins = np.arange(min(GB1_5_9Hz), max(GB1_42Hz)+2)
print bins
plt.hist(combo, bins, label=['5.9 Hz Resolution', '35 Hz Resolution', '42 Hz Resolution'])
plt.legend(loc='upper right')
plt.show()

combo = np.column_stack((MBP_4_8Hz, MBP_35Hz, MBP_42Hz))

bins = np.arange(min(MBP_4_8Hz), max(MBP_42Hz)+2)
print bins
plt.hist(combo, bins, label=['4.8 Hz Resolution', '35 Hz Resolution', '42 Hz Resolution'])
plt.legend(loc='upper right')
print len(MBP_42Hz)
plt.show()
