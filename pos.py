import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

num = 2

rng = np.array([1.8, 3.0, 3.0])
survey = np.array([3.63, 4.38])

A = np.array([[0, 3.63], [2.45, 3.63]])

B = np.zeros((num, 1))
for x in range(int(num)):
    B[x][0] = 0.5 * ((math.pow(rng[0], 2)) - (math.pow(rng[x + 1], 2)) + (math.pow(survey[x], 2)))


A_transpose = A.transpose()
C = A_transpose.dot(A)

res1 = (np.linalg.inv(C)).dot(A_transpose).dot(B)
# print(res1)

Q, R = np.linalg.qr(A)
res2 = (np.linalg.inv(R)).dot(Q.transpose()).dot(B)
# print(res2)

res = np.add(res1, res2)
print(res)

style.use('fivethirtyeight')
fig = plt.figure()
plt.scatter(0, 0)
plt.scatter(0, 3.63)
plt.scatter(2.45, 3.63)

def animate(i):
    plt.axis([0, 5, 0, 5])
    plt.xlabel('X_axis')
    plt.ylabel('Y_axis')
    plt.scatter(res[0][0], res[1][0])


ani = animation.FuncAnimation(plt.gcf(), animate)

plt.show()
