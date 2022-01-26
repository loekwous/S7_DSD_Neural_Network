import random
from layer import Layer

class Network:
  def __init__(self, n_hidden_layers=1, n_inputs =2, n_neuron_p_layer= 3, n_outputs = 1, activation_type="ramp"):
    self._n_inputs = n_inputs
    self._n_outputs = n_outputs
    self._layers = []
    self._layers.append(Layer(n_neurons=n_inputs, n_inputs=1, activation_type=activation_type))
    for i in range(1, n_hidden_layers + 1 ):
        self._layers.append(Layer(n_neurons=n_neuron_p_layer, last_layer=self._layers[i-1], activation_type=activation_type))
    self._layers.append(Layer(n_neurons=n_outputs, last_layer=self._layers[len(self._layers)-1], activation_type=activation_type))
    for layer in range(1, len(self._layers)-1):
      for neuron in range(len(self._layers[layer])):
        self._layers[layer].get_neuron(neuron).set_next_layer(self._layers[layer+1])

  def feed_forward(self):
    for i in range(len(self._layers[-1])):
      self._layers[-1].get_neuron(i).process()

  def set_input(self, n, value):
    self._layers[0].get_neuron(n).set_input(0, value)

  def get_output(self, n) -> float:
    return self._layers[-1].get_neuron(n).get_output()

  def __get_der_error(self, predicted: list):
    if len(predicted) != self._n_outputs:
      raise ValueError("Length of predicted list should be equal to number of outputs")

    sum = 0
    for i in range(self._n_outputs):
      sum += (self.get_output(i) - predicted[i])
    return sum

  def __get_error(self, predicted: list) -> float:
    if len(predicted) != self._n_outputs:
      raise ValueError("Length of predicted list should be equal to number of outputs")

    sum = 0
    for i in range(self._n_outputs):
      sum += (self.get_output(i) - predicted[i])**2
    return sum

  def __update_weight(self, derivative: float, learning_rate: float, old_weight: float) -> float:
    return old_weight + (derivative * learning_rate)

  def back_propagation(self, predicted: list, learning_rate: float) -> float:
    for lay in range(1, len(self._layers)):

      # run backprop for every layer
      for neuron in range(len(self._layers[lay])):
        current_neuron = self._layers[lay].get_neuron(neuron)
        der = current_neuron.calc_der(is_bias=True, predicted=predicted)
        old_bias = current_neuron.get_bias()
        new_bias = self.__update_weight(der, learning_rate, old_bias)
        current_neuron.set_bias(new_bias)
        #update weights
        for weight in range(len(current_neuron)):
          der = current_neuron.calc_der(respect_to_weight=weight, predicted=predicted)
          old_weight = current_neuron.get_weight(n=weight)
          new_weight = self.__update_weight(der, learning_rate,old_weight)
          self._layers[lay].get_neuron(neuron).set_weight(n=weight, x=new_weight)
    error = self.__get_error(predicted)
    return error

  def print_layout(self):
    print("")
    for i in range(1, len(self._layers)):
      print("================================")
      print("layer: {}".format(i))
      for neuron in range(len(self._layers[i])):
        print("neuron: {}".format(neuron))
        print("bias: {}".format(self._layers[i].get_neuron(neuron).get_bias()))
        for weight in range(len(self._layers[i].get_neuron(neuron).get_weights())):
          print("weight {}: {}".format(weight, self._layers[i].get_neuron(neuron).get_weight(weight)))
        print("--------------------------------")
    print("<<================================>>")
    print("")


def predict(a) -> list:
  #q1 = 0.2*a*a - 0.1*a + 0.0125
  q1 = 0.2*a + 0.1*a*a
  return q1


if __name__ == "__main__":
  network = Network(n_hidden_layers=1, n_inputs=1, n_neuron_p_layer=10, n_outputs=1, activation_type="sigmoid")

  network.print_layout()

  learning_rate = 0.04
  error_list = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
  len_error_list = len(error_list)

  x_list = []
  y_list = []
  i = 0

  stop = False

  while sum(error_list) > 1E-5 and stop is False:
  #for x in range(10000):


    r1 = random.random() * 2

    predicted = predict(r1)

    network.set_input(0, r1)

    network.feed_forward()

    out = network.get_output(0)

    error = network.back_propagation([predicted], learning_rate=learning_rate)
    error_list[i%len_error_list] = error
    if i % len_error_list == 0:
      x_list.append(i)
      y_list.append(error)

    print("iteration: {}, err: {:.10f}, learning_rate: {:.5f}".format(i, error, learning_rate), end="\r")
    i += 1
    if i == 1E6:
      stop = True

network.print_layout()

from matplotlib import pyplot as plt

plt.plot(x_list,y_list)
plt.xlabel("samples")
plt.ylabel("error")
plt.show()


test_x_list = []
test_y1_list = []
test_ay1_list = []


for i in range(100):
  x = 0.01 * i

  test_x_list.append(x)
  test_y1_list.append(predict(x))
  network.set_input(0, x)
  network.feed_forward()
  test_ay1_list.append(network.get_output(0))

plt.plot(test_x_list, test_y1_list,)
plt.plot(test_x_list, test_ay1_list)
plt.legend(["pr1", "ai1"])
plt.show()
