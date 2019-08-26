import os
import numpy as np
import matplotlib.pyplot as plt

base_dir = os.getcwd()
test_data = np.loadtxt(base_dir + '/input_new.csv', delimiter=',', dtype=np.float32)
title = "Gyro-sensor "

# state = "(car out->in)"
state = "1"
# state = "(walking-sit)"


# title = "Accelerometer sensor "
# y1 = test_data[:, 1:2]
# y2 = test_data[:, 2:3]
# y3 = test_data[:, 3:4]

# title = "Orientation sensor "
# y1 = test_data[:, 4:5]
# y2 = test_data[:, 5:6]
# y3 = test_data[:, 6:7]

# title = "Gyro sensor "
# y1 = test_data[:, 7:8]
# y2 = test_data[:, 8:9]
# y3 = test_data[:, 9:10]

# title = "Magno sensor "
y1 = test_data[:, 6:9]
# y2 = test_data[:, 11:12]
# y3 = test_data[:, 12:13]


# plt.axis([0, 60, -50,50])

plt.title(title+state)
x = test_data[:, 10:11]
plt.plot(x, y1, label="x-axis")
# plt.plot(x, y2, label="y-axis")
# plt.plot(x, y3, label="z-axis")
plt.grid()
plt.legend()
plt.xlabel("time")
plt.ylabel("value")
plt.axis([0, 10, -3,3])
plt.show()


