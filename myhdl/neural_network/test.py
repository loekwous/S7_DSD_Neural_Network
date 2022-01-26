# def cotofl(val: int):
#   return float(val)/1024.0

# def cotofi(val: float):
#   return int(val*1024)


# def sigmoid(val: int):
#   return (1000*val)/(1 + val) / 1000

# val = 4.0

# fixed_val = cotofi(val)


# fixed_new_val = sigmoid(fixed_val)

# new_val = cotofl(fixed_new_val)

from matplotlib import pyplot as plt

def get_dv(polynomial: list):
  dv = []
  highest_power = len(polynomial) - 1
  for i in range(len(polynomial)-1):
    dv.append(polynomial[i] * (highest_power - i))
  return dv

def convert(x: float, polynomial: list) -> float:
  highest_power = len(polynomial) - 1
  output = 0
  for i in range(len(polynomial)):
    output += polynomial[i] * x**(highest_power - i)
  return output


polynomial = [2, 3, 1]

dv_polynomial = get_dv(polynomial)

x_list = []
y_list = []
ydv_list = []
zero_list = []


for i in range(-500,500):
  x = i/100.0
  x_list.append(x)
  zero_list.append(0)
  y_list.append(convert(x, polynomial))
  ydv_list.append(convert(x, dv_polynomial))

plt.plot(x_list, y_list)
plt.plot(x_list, ydv_list)
plt.plot(x_list, zero_list)
plt.show()
