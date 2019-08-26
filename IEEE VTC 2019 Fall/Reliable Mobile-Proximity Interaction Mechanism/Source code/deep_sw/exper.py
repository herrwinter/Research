import csv
import numpy as np
import os
base_dir = os.getcwd()
raw_data = np.loadtxt(base_dir + '\\output_data.csv', delimiter=',', dtype=np.float64)