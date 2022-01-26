import matplotlib.pyplot as plt

x_left = []
x_right = []
left_data = []
right_data = []

with open("samples16.txt", "r") as f:
  lines = f.readlines()
  for i in range(1, len(lines)):
    line = lines[i]
    list_of_data = line.split(",")
    if int(list_of_data[1]) == 1:
      # l = int(list_of_data[2])
      # if l > (2**23-1):
      #   l = -(2**24) + l
      # left_data.append(float(l))
      # if l > 1E6:
      #   print("right top: {}".format(l))
      # x_left.append(float(list_of_data[0]))
      pass
    else:
      r = int(list_of_data[2])
      if r > (2**23-1):
        r = -(2**24) + r
      right_data.append(float(r))
      x_right.append(float(list_of_data[0]))

#plt.plot(x_left, left_data)
plt.plot(x_right, right_data)
plt.legend(["right"])
plt.show()
