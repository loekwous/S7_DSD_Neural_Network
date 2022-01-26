import random
from colorama import Fore, init

init()

def get_poly(poly: list) -> str:
  highest_power = len(poly) - 1
  return_value = ""
  for i in range(len(poly)):
    return_value += str(poly[i]) + "x^" + str(highest_power-i)
    if i < len(poly)-1:
      return_value += " + "
  return return_value

def pretty_poly(poly: list) -> str:
  orig = get_poly(poly)
  orig = orig.replace("x^0", "")
  orig = orig.replace("+ -", "- ")
  return orig

def derive(poly: list) -> list:
  highest_power = len(poly) - 1
  return_list = []
  for i in range(len(poly) - 1):
    return_list.append(poly[i] * (highest_power-i))
  return return_list

def function(x, poly = [2, -2, 0]):
  highest_power = len(poly) - 1
  return_value = 0
  for i in range(len(poly)):
    return_value += poly[i] * x**(highest_power-i)
  return return_value

def der_function(x, poly= [2, -1, 0]):
  return function(x, poly)

def new_x(old_x, learning_rate, derivative) -> float:
  return old_x - (learning_rate * derivative)

def cost_function(output, expected) -> float:
  return 1/2 * (output - expected)**2

def der_cost_function(output, expected) -> float:
  return output - expected

poly = [2, 0, -1]

der_poly = derive(poly)

print(Fore.GREEN +"polynomial = " + pretty_poly(poly) + Fore.RESET)

x = random.random()
y = function(x, poly)
der = der_function(x, der_poly)

allowed_error = 1E-10

learning_rate = 0.001

dots = []

while abs(der) > allowed_error:
  y = function(x, poly)
  der = der_function(x, der_poly)
  if poly[0] < 0.0:
    der *=-1
  x = new_x(old_x=x, learning_rate=learning_rate, derivative=der)
  #print("x={:.5f}, y={:.5f}, der={:.5f}".format(x, y, der))

dots.append([x,y])
print("bottom of parabola -> x: {:.3f}, y: {:.3f}".format(x,y))
x_bottom = x
if ((y < 0 and poly[0] > 0.0) or (y > 0 and poly[0] < 0.0)) and len(poly) == 3:
  der = der_cost_function(y,0)
  while abs(der) > allowed_error:
    y = function(x, poly)
    der = der_cost_function(y, 0)
    x = new_x(old_x=x, learning_rate=learning_rate, derivative=der)
  dots.append([x,y])
  print("zero of parabola -> x: {:.3f}".format(x))
  diff = abs(x - x_bottom)
  if x > x_bottom:
    x_other = x_bottom - diff
  else:
    x_other = x_bottom + diff
  y = function(x_other, poly)
  dots.append([x_other,y])
  print("zero of parabola -> x: {:.3f}".format(x_other))

# ---------------------- plot parabola
func_list = []
x_list = []

colors = ["go", "yo", "yo"]

if len(dots) > 1:
  minimum = int((min(dots[1][0], dots[2][0]) - 1) * 1000)
  maximum = int((max(dots[1][0], dots[2][0]) + 1) * 1000)
else:
  minimum = int((dots[0][0] - 1) * 1000)
  maximum = int((dots[0][0] + 1) * 1000)

for i in range(minimum, maximum):
  x = i / 1000
  x_list.append(x)
  func_list.append(function(x, poly))

import matplotlib.pyplot as plt

for i in range(len(dots)):
  plt.plot(dots[i][0], dots[i][1], colors[i])

plt.plot(x_list, func_list)
plt.grid(True)
plt.show()
