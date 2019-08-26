import csv
import os
import numpy as np
import tensorflow as tf

base_dir = os.getcwd()


predict = np.loadtxt(base_dir + '\\predict.csv', delimiter=',', dtype=np.float64)
before = np.loadtxt(base_dir + '\\output_datac.csv', delimiter=',', dtype=np.float64)
result = open('result.csv','a',newline='')
csv_writer = csv.writer(result)
csv_writer.writerow(before[0])
for row in range(8995):
    put = before[row] + predict[row]
    csv_writer.writerow(put)