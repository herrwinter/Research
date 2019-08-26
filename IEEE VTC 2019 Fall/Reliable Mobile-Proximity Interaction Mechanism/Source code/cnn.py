import csv
import os
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.utils import np_utils
from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense, LSTM, Embedding, Dropout
from keras.preprocessing import sequence
from keras.utils import np_utils
from keras.layers.convolutional import Conv1D
from keras.layers import GlobalAveragePooling1D
from keras.layers import MaxPooling1D

def merge_training_data():
    base_dir = os.getcwd()
    raw_arm_data = np.loadtxt(base_dir+'\\arm_data.csv', delimiter=',', dtype=np.float64)
    raw_leg_data = np.loadtxt(base_dir+'\\leg_data.csv', delimiter=',', dtype=np.float64)
    output_data = np.loadtxt(base_dir+'\\output_data.csv', delimiter=',', dtype=np.float64)

    arm_count = 0
    leg_count = 0
    y = [[0]*53 for i in range(8995)]

    # merge function
    for row in range(len(output_data)-1):
        arm_count, leg_count = merge_data(output_data[row+1][0], raw_arm_data, raw_leg_data, arm_count, leg_count)

    for row in range(len(output_data)-1):
        y[row][0:52] = output_data[row+1][0:52]-output_data[row][0:52]
        y_out = open('output.csv', 'a', newline='')
        csv_writer = csv.writer(y_out)
        csv_writer.writerow(y[row])

def merge_data(y_timestamp, arm_data, leg_data, arm_count, leg_count):
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

    temp = []
    temp.extend(arm_temp1)
    temp.extend(arm_temp2)
    temp.extend(arm_temp3)
    temp.extend(arm_temp4)
    temp.extend(arm_temp5)
    temp.extend(leg_temp1)
    temp.extend(leg_temp2)
    temp.extend(leg_temp3)
    temp.extend(leg_temp4)
    temp.extend(leg_temp5)

    f = open('input.csv', 'a', newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow(temp)

    return arm_count, leg_count


def read_learning_data():
    base_dir = os.getcwd()
    raw_x_data = np.loadtxt(base_dir + '/input.csv', delimiter=',', dtype=np.float64)
    raw_y_data = np.loadtxt(base_dir + '/output.csv', delimiter=',', dtype=np.float64)


    x_data = raw_x_data[:, 0:90]
    scaler = MinMaxScaler()
    x_data_scaled = scaler.fit_transform(x_data)

    y_data = raw_y_data[:, 1:53]

    return x_data_scaled, y_data

def read_test_data():
    base_dir = os.getcwd()
    test_data = np.loadtxt(base_dir + '/test.csv', delimiter=',', dtype=np.float64)
    test_x_data = test_data[:, 0:90]
    test_y_data = test_data[:, 1:53]

    return test_x_data, test_y_data

#merge_training_data()

x_data, y_data = read_learning_data()

x_data = x_data.reshape(8995,90,1)
#y_data = y_data.reshape(8995,51,1)
model = Sequential()
model.add(Conv1D(128,3,activation='sigmoid', input_shape = (90,1), padding = 'same', strides = 3))
model.add(Conv1D(128,3,activation='sigmoid'))
model.add(MaxPooling1D(3))
model.add(Conv1D(64,3,activation='sigmoid'))
model.add(Conv1D(64,3,activation='sigmoid'))
model.add(GlobalAveragePooling1D())
model.add(Dropout(0.1))
model.add(Dense(51,activation = 'sigmoid'))

model.compile(loss = 'binary_crossentropy', optimizer = 'rmsprop', metrics = ['accuracy'])
model.fit(x_data,y_data,batch_size = 64, epochs = 10)


#2d 아직안됌
# X = tf.placeholder(tf.float32)
# Y_Label = tf.placeholder(tf.float32)
#
#
# kernel1 = tf.Variable(tf.truncated_normal(shape = [1,3,1,1],stddev=0.1))
# bias1 = tf.Variable(tf.truncated_normal(shape = [1],stddev = 0.1)) #shapee = [kerner_size]
# conv1 = tf.nn.conv2d(X, kernel1, strides=[1,1,1,1],padding = 'SAME') + bias1
# activation1 = tf.nn.relu(conv1) # conv1 output
#
# Loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels = Y_Label, logits = activation1))
# train_step = tf.train.AdamOptimizer(0.005).minimize(Loss)
#
# correct_prediction = tf.equal(tf.argmax(activation1, 1), tf.argmax(Y_Label,1))
# accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))
#
# with tf.Session() as sess:
#     print("strart...")
#     sess.run(tf.global_variables_initializer())
#     for i in range(10000):
#         sess.run(train_step, feed_dict = {X: x_data, Y_Label:y_data})
#         if i%100:
#             print(sess.run(accuracy,feed_dict = {X: x_data, Y_Label:y_data}))