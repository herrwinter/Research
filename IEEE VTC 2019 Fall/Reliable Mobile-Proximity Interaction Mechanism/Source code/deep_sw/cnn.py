import csv
import os
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.examples.tutorials.mnist import input_data

base_dir = os.getcwd()
raw_arm_data = np.loadtxt(base_dir+'\\arm_data.csv', delimiter=',', dtype=np.float64)
raw_leg_data = np.loadtxt(base_dir+'\\leg_data.csv', delimiter=',', dtype=np.float64)
output_data = np.loadtxt(base_dir+'\\output_data.csv', delimiter=',', dtype=np.float64)

arm_count = 0
leg_count = 0


for row in range(len(output_data)):
    arm_count, leg_count = make_information(output_data[row][0], raw_arm_data, raw_leg_data, arm_count, leg_count)




def make_information(y_timestamp, arm_data, leg_data, arm_count, leg_count):
    count = 0
    for in_arm_count in range(arm_count, len(arm_data)):  # arm data 찾기
        if (arm_data[in_arm_count][9] >= y_timestamp):
            count = in_arm_count
            break

    arm_count = count

    arm_temp1 = arm_data[arm_count - 1][0:9]
    arm_temp2 = arm_data[arm_count - 2][0:9]
    arm_temp3 = arm_data[arm_count - 3][0:9]
    arm_temp4 = arm_data[arm_count - 4][0:9]
    arm_temp5 = arm_data[arm_count - 5][0:9]

    f = open('arm_input.csv', 'a', newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow(arm_temp1)
    csv_writer.writerow(arm_temp2)
    csv_writer.writerow(arm_temp3)
    csv_writer.writerow(arm_temp4)
    csv_writer.writerow(arm_temp5)


    for in_leg_count in range(leg_count, len(leg_data)):  # leg_data 찾기
        if leg_data[in_leg_count][9] >= y_timestamp:
            count = in_leg_count
            break

    leg_count = count

    leg_temp1 = leg_data[leg_count - 1][0:9]
    leg_temp2 = leg_data[leg_count - 2][0:9]
    leg_temp3 = leg_data[leg_count - 3][0:9]
    leg_temp4 = leg_data[leg_count - 4][0:9]
    leg_temp5 = leg_data[leg_count - 5][0:9]

    f1 = open('leg_input.csv', 'a', newline='')
    csv_writer = csv.writer(f1)
    csv_writer.writerow(leg_temp1)
    csv_writer.writerow(leg_temp2)
    csv_writer.writerow(leg_temp3)
    csv_writer.writerow(leg_temp4)
    csv_writer.writerow(leg_temp5)


    return arm_count, leg_count
