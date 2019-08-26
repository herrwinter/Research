import csv
import os
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
save_file  = os.path.join(BASE_DIR, '\model\model.ckpt')

class Machine:
    def __init__(self):
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

        # input, output data
        self.X = tf.placeholder(tf.float32)
        self.Y = tf.placeholder(tf.float32)

        # weight, bias
        self.W1 = tf.Variable(tf.random_uniform([90, 30], -1., 1.))
        self.W2 = tf.Variable(tf.random_uniform([30, 30], -1., 1.))
        self.W3 = tf.Variable(tf.random_uniform([30, 30], -1., 1.))
        self.W4 = tf.Variable(tf.random_uniform([30, 51], -1., 1.))

        self.b1 = tf.Variable(tf.zeros([30]))
        self.b2 = tf.Variable(tf.zeros([30]))
        self.b3 = tf.Variable(tf.zeros([30]))
        self.b4 = tf.Variable(tf.zeros([51]))

        self.L1 = tf.add(tf.matmul(self.X, self.W1), self.b1)
        self.L1 = tf.nn.relu(self.L1)

        self.L2 = tf.add(tf.matmul(self.L1, self.W2), self.b2)
        self.L2 = tf.nn.relu(self.L2)

        self.L3 = tf.add(tf.matmul(self.L2, self.W3), self.b3)
        self.L3 = tf.nn.softmax(self.L3)

        # learning model
        self.model = tf.add(tf.matmul(self.L3, self.W4), self.b4)

    def init_tf(self):
        self.init = tf.initialize_all_variables()
        self.sess = tf.Session()
        self.sess.run(self.init)

    # model learning
    def learning(self, x_data, y_data, epoch):
        cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=self.Y, logits=self.model))

        optimizer = tf.train.AdamOptimizer(learning_rate=0.00001)
        train_op = optimizer.minimize(cost)

        self.init_tf()

        for step in range(epoch):
            self.sess.run(train_op, feed_dict={self.X: x_data, self.Y: y_data})

            if (step + 1)%1 == 0:
                print(step + 1, self.sess.run(cost, feed_dict={self.X: x_data, self.Y: y_data}))

        self.model_weight_save()
        return self.sess, self.model

    # Save model's weights
    def model_weight_save(self):
        saver = tf.train.Saver()
        saver.save(self.sess, save_file)

        print(os.getcwd())
        print("Model saved in file: ", save_file)

    # using model learned, do testing
    def test(self, test_x_data):
        #print(self.sess.run(self.model, feed_dict={self.X: test_x_data}))
        predict = open('predict.csv','a',newline='')
        pre = self.sess.run(self.model, feed_dict={self.X: test_x_data})
        for row in range(8995):
            csv_writer = csv.writer(predict)
            csv_writer.writerow(pre[row])

        # csv_writer = csv.writer(predict)
        # csv_writer.writerow())
        # # # predected Cell number
        #predict_value = self.get_predict_result(test_x_data)
        #print('predict_value : ', predict_value)
        #
        # real Cell number
        #real_value = self.get_real_value(test_y_data)
        #print('real_value : ', real_value)
        #
        # # compare between predicted value and real value
        # is_correct = tf.equal(predict_value, real_value)
        # accuracy = tf.reduce_mean(tf.cast(is_correct, tf.float32))
        # print('accuracy: %.2f' % self.sess.run(accuracy * 100,
        #                                        feed_dict={self.X: test_x_data, self.Y: test_y_data}))

    # # One hot encoding(predict cell)
    # def get_predict_result(self, x_data):
    #      prediction = tf.argmax(self.model, 1) + 1
    #      return self.sess.run(prediction, feed_dict={self.X: x_data})
    #
    # # One hot encoding(real cell)
    # def get_real_value(self, y_data):
    #     target = tf.argmax(y_data, 1) + 1
    #     return self.sess.run(target)

    def read_training_data(self):
        self.init_tf()
        saver = tf.train.Saver()
        save_file = os.path.join(BASE_DIR, '\model\model.ckpt')
        saver.restore(self.sess, save_file)


# Learning progress based on number of sets
def merge_training_data():
    base_dir = os.getcwd()
    raw_arm_data = np.loadtxt(base_dir+'\\arm_data.csv', delimiter=',', dtype=np.float64)
    raw_leg_data = np.loadtxt(base_dir+'\\leg_data.csv', delimiter=',', dtype=np.float64)
    output_data = np.loadtxt(base_dir+'\\output_data.csv', delimiter=',', dtype=np.float64)

    arm_count = 0
    leg_count = 0
    x = [[0]*90 for i in range(8995)]
    y = [[0]*51 for i in range(8995)]
    # merge function
    for row in range(len(output_data)-1):
        x[row], arm_count, leg_count = merge_data(output_data[row+1][0],
                                                  raw_arm_data, raw_leg_data, arm_count, leg_count)

    for row in range(len(output_data)-1):
        y[row][0:51] = output_data[row+1][1:52]-output_data[row][1:52]

    return x,y

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

    return temp, arm_count, leg_count


def read_learning_data(input, output):
    x_data = input
    scaler = MinMaxScaler()
    x_data_scaled = scaler.fit_transform(x_data)

    y_data = output

    return x_data_scaled, y_data

def read_test_data(input, output):

    test_x_data = input
    scaler = MinMaxScaler()
    test_x_data = test_x_data.reshape(8995,90)
    x_data_scaled = scaler.fit_transform(test_x_data)
    test_y_data = output

    return x_data_scaled, test_y_data

# Main function start
machine = Machine()

# Select epoch num
epoch = 100

# input data generate into input.csv
input, output = merge_training_data()
input = np.array(input)
output = np.array(output)

input = input.reshape(8995,90,1)
output = output.reshape(8995,51,1)
# Learning Step(3 lines)
#x_data, y_data = read_learning_data(input,output)
#machine.learning(x_data, y_data, epoch)
#machine.test(x_data)

# Testing Step(3 lines)
x_data, y_data = read_test_data(input,output)
machine.read_training_data()
machine.test(x_data)

