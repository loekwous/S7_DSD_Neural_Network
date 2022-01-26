def function(x):
  return 2* x**2 - 2*x + 0.5

def der_function(x):
  return 4*x-2

def new_x(old_x, learning_rate, derivative) -> float:
  return old_x - (learning_rate * derivative)

def cost_function(expected, output) -> float:
  return (output - expected)**2

x = 5
y = function(x)
err = cost_function(0, y)

allowed_error = 1E-50

learning_rate = 0.01

while err > allowed_error:
  y = function(x)
  der = der_function(x)
  x = new_x(old_x=x, learning_rate=learning_rate, derivative=der)
  err = cost_function(expected=0, output=y)
  print("x={:.5f}, y={:.5f}, err={:.5f}".format(x, y, err))


# import random
# import matplotlib.pyplot as plt
# from typing import List


# def C(o,p) -> float:
#   return 1/2*(o-p)**2

# def dCdo(o,p) -> float:
#   return o - p

# def sigmoid(x) -> float:
#   #return x/(1+abs(x))
#   if x > 1.0:
#     return 1.0
#   elif x < 0.0:
#     return 0.0
#   else:
#     return x

# def dsigdx(x) -> float:
#   if x > 1.0:
#     return 0.0
#   elif x < 0.0:
#     return 0.0
#   else:
#     return 1

# def j(w1, i1, w2, i2, bias) -> float:
#   return w1*i1 + w2*i2 + bias

# def o(j) -> float:
#   return sigmoid(j)

# def dCdw1(output, predicted, w1, w2, i1, i2, bias) -> float:
#   return dCdo(output, predicted) * dsigdx(j(w1, i1, w2, i2, bias)) * i1

# def dCdw2(output, predicted, w1, w2, i1, i2, bias) -> float:
#   return dCdo(output, predicted) * dsigdx(j(w1, i1, w2, i2, bias)) * i2

# def dCdb(output, predicted, w1, w2, i1, i2, bias) -> float:
#   return dCdo(output, predicted) * dsigdx(j(w1, i1, w2, i2, bias))

# def new_weight(dcdw, learning_rate, old)-> float:
#   return old - (learning_rate * dcdw)

# def feed_forward(w1, w2, i1, i2, bias) -> float:
#   return sigmoid(j(w1, i1, w2, i2, bias))

# def funct(a,b)->int:
#   return 0.2*(a + b) + 0.2

# def get_training_data() -> list:
#   ri1 = random.random()
#   ri2 = random.random()
#   o = funct(ri1, ri2)
#   return [ri1, ri2, o]

# def error(output, predicted) -> float:
#   return C(output, predicted)

# start_w1 = random.random()
# start_w2 = random.random()
# start_bias = random.random()

# y_list = []
# x_list = []

# for i in range(1,8):

#   y_list.append([])
#   x_list.append([])

#   w1 = start_w1
#   w2 = start_w2
#   bias = start_bias

#   learning_rate = 0.13 * float(i)

#   print("learning rate: {:.2f} and w1: {:.5f} and w2: {:.5f} and bias: {:.5f}".format(learning_rate, w1, w2, bias))

#   last2_error = 1
#   last_error = 1
#   err = 1
#   it = 0
#   while last_error > 1E-15 and err > 1E-15 and last2_error > 1E-15:
#     if it % 20 == 0:
#       last2_error = last_error
#       last_error = err

#     i1, i2, predict = get_training_data()

#     out = feed_forward(w1, w2, i1, i2, bias)

#     err = error(out, predict)

#     accuracy = 1.0 - err/(1/2)

#     w1 = new_weight(dCdw1(out, predict, w1, w2, i1, i2, bias), learning_rate, w1)
#     w2 = new_weight(dCdw2(out, predict, w1, w2, i1, i2, bias), learning_rate, w2)
#     bias = new_weight(dCdb(out, predict, w1, w2, i1, i2, bias), learning_rate, bias)
#     print("w1: {:.5f} and w2: {:.5f} and bias: {:.5f}".format(w1, w2, bias), end=" ")
#     print("it: {:4.0f}, err: {:.10f}, acc: {:.5f}".format(it, err, accuracy), end="\r")
#     x_list[i-1].append(it)
#     y_list[i-1].append(err)
#     it += 1
#     #print("i1: {:.2f}, i2: {:.2f}, out: {:.2f}, err: {:.7f}".format(i1, i2, out, err))

#   print("")
#   print("------------------------------------")

# legend_list = []

# for i in range(len(y_list)):
#   for x in range(15, len(y_list[i])):
#     y_list[i][x-2] = (y_list[i][x-14] + y_list[i][x-13] +y_list[i][x-12] + y_list[i][x-11] + y_list[i][x-10] +y_list[i][x-9] + y_list[i][x-8] +y_list[i][x-7] + y_list[i][x-6] + y_list[i][x-5] + y_list[i][x-4] + y_list[i][x-3] +y_list[i][x-2] + y_list[i][x-1] + y_list[i][x-1]) / 15.0


# for i in range(len(y_list)):
#   legend_list.append("lr {:.2f}".format((i+1) * 0.13))
#   plt.plot(x_list[i], y_list[i])

# plt.xlabel("iterations")
# plt.ylabel("error")
# plt.legend(legend_list)
# plt.show()
