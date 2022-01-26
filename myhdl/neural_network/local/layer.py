import random

class Neuron: # early declaration
  pass

class Layer: # early declaration
  pass

class Neuron:
  def __init__(self, n_inputs = 1, n_weights = 1, activation_type="step", previous_layer: Layer = None, number_in_layer = 0):

    if activation_type not in ["relu", "ramp", "sigmoid"]:
      raise ValueError("activation type is not supported")
    else:
      self._activation_type = activation_type
    if previous_layer is None and (n_weights != 1 or n_inputs != 1):
      raise ValueError("n_inputs, n_weights and previous layer are None, this is not possible")
    self._previous_layer = previous_layer
    self._n_inputs = n_inputs if previous_layer is None else len(previous_layer)
    self._n_weights = n_weights if previous_layer is None else len(previous_layer)
    self._weights = [(random.random() if previous_layer is not None else 1.0) for _ in range(self._n_weights)]
    self._inputs = [0 for _ in range(self._n_inputs)]
    if self._previous_layer is not None:
      self._bias = random.random()
    else:
      self._bias = 0.0
    self._next_layer = None
    self._number_in_layer = number_in_layer
  def set_next_layer(self, next_layer: Layer):
    self._next_layer = next_layer
  def get_bias(self)->float:
    return self._bias
  def set_bias(self, bias):
    self._bias = bias
  def get_weights(self) -> list:
    return self._weights
  def get_weight(self, n) -> float:
    return self._weights[n]
  def get_inputs(self) -> list:
    return self.inputs
  def set_input(self, n, x):
    if n >= 0 and n < self._n_inputs:
      self._inputs[n] = x
    else:
      raise ValueError("Index out of range: inputs[n]")

  def set_weight(self, n, x):
    if n >= 0 and n < self._n_weights:
      self._weights[n] = x
    else:
      raise ValueError("Index out of range: weights[n]")

  def _activation(self, x):
    if self._previous_layer is not None:
      if self._activation_type == "relu":
        if x > 0:
          return x
        else:
          return 0.0
      elif self._activation_type == "ramp":
        if x <= 0:
          return 0.0
        elif x > 1.0:
          return 1.0
        else:
          return x
      elif self._activation_type == "sigmoid":
        return (x)/(1+abs(x))
    else:
      return x
  def der_activation(self, x):
    if self._activation_type == "relu":
      if x > 0:
        return 1.0
      else:
        return 0.0
    elif self._activation_type == "ramp":
      if x <= 0:
        return 0.0
      elif x > 1.0:
        return 0.0
      else:
        return 1.0
    elif self._activation_type == "sigmoid":
      return 1/((1+abs(x))**2)

  def der_sum(self, respect_to_weight = None, respect_to_input = None):
    if type(respect_to_input) == type(respect_to_weight):
      raise ValueError("both inputs cannot be the same rtw '{}' and rti '{}'".format(type(respect_to_input), type(respect_to_weight)))
    if respect_to_input is not None:
      return self._weights[respect_to_input]
    elif respect_to_weight is not None:
      return self._inputs[respect_to_weight]
    else:
      raise RuntimeError("one of the inputs should not be None")

  def get_sum(self) ->float:
    sum = 0
    for i in range(self._n_inputs):
      sum += self._weights[i] * self._inputs[i]
    return sum + self._bias
  def get_output(self) ->float:
    return self._activation(self.get_sum())
  def process(self) -> Neuron:
    if self._previous_layer is not None:
      prev_layer_len = len(self._previous_layer)
      for i in range(prev_layer_len):
        if not self._previous_layer.is_input():
          self._inputs[i] = self._previous_layer.get_neuron(i).process().get_output()
        else:
          self._inputs[i] = self._previous_layer.get_neuron(i).process().get_sum()
    return self
  def __len__(self):
    return len(self._inputs)
  def calc_der(self, respect_to_weight = None, respect_to_input = None, predicted = 0, is_bias: bool = False) -> float:
    if type(respect_to_input) == type(respect_to_weight) and not is_bias:
      raise ValueError("both inputs cannot be the same rtw '{}' and rti '{}'".format(type(respect_to_input), type(respect_to_weight)))
    der = self.der_activation(self.get_sum())

    if respect_to_input is not None:
      der *= self.der_sum(respect_to_input)

    elif respect_to_weight is not None:
      der *= self.der_sum(respect_to_weight)
    elif is_bias is False:
      RuntimeError("None of the options is enabled")

    der_forwarded = 0

    if self._next_layer is not None:
      for i in range(len(self._next_layer)):
          der_forwarded += self._next_layer.get_neuron(i).calc_der(respect_to_input=self._number_in_layer, predicted=predicted)
    else:
      der_forwarded = 2*(predicted[self._number_in_layer] - self.get_output())
    return der * der_forwarded


class Layer:
  def __init__(self,n_neurons, n_inputs = 2, n_weights = 1, activation_type="ramp", last_layer: Layer = None):
    self._n_neurons = n_neurons
    self._n_weights = n_weights
    self._n_inputs = n_inputs
    self._neurons = [Neuron(n_inputs, n_weights, activation_type, previous_layer=last_layer, number_in_layer=i) for i in range(n_neurons)]
    self._is_input = True if last_layer is None else False
  def is_input(self):
    return self._is_input
  def get_neuron(self, n) -> Neuron:
    if n >= 0 and n <= self._n_neurons:
      return self._neurons[n]
    else:
      raise ValueError("Index out of range: neurons[n]")
  def __len__(self) -> int:
    return self._n_neurons
