import os
from myhdl import *
from colorama import Fore, init

init()

if "TRACE_LOCATION" not in globals():
  TRACE_LOCATION = "traces/"

if __name__ == '__main__':
  from neural_network_info import ai_info
else:
  try:
    from neural_network_info import ai_info
  except:
    from .neural_network_info import ai_info

@block
def absolute(input, output):
  @always_comb
  def logic():
    if input >= 0:
      output.next = input
    else:
      output.next = input * -1
    if __debug__:
      print("abs:",int(input), int(output.next))
  return logic

@block
def divider(numerator, denominator, outcome):
  max_outcome = outcome.max - 1
  @always_comb
  def logic():
    if denominator != 0:
      outcome.next = numerator // denominator
    else:
      outcome.next = 0
    if __debug__:
      print("divider: num", int(numerator), "den", int(denominator), "out", int(outcome.next))
  return logic

@block
def multiplier(input, weight, output):
  @always_comb
  def logic():
    """ Single multiplier """
    product = (input * weight) // ai_info.fixed_point_division
    output.next = product
  return logic

@block
def adder(a,b,c):
  @always_comb
  def logic():
    """ Single adder """
    sum = a + b
    c.next = sum
  return logic

@block
def parallel_multiplier(inputs, weights, outputs):
  """ Parallel multiplier """
  number_of_inputs = len(inputs)
  multipliers = []
  for i in range(number_of_inputs):
    multipliers.append(multiplier(inputs[i], weights[i], outputs[i]))

  return multipliers

@block
def list_adder(output, inputs):
  """ Parallel adder """
  number_of_inputs = len(inputs)
  number_of_signals = number_of_inputs - 2
  number_of_adders = number_of_inputs - 1

  # create signals
  sigs =  []#[Signal(intbv(0,min=inputs[0].min * (2+i),max=inputs[0].max * (2+i))) for i in range(number_of_signals)]
  minimum = inputs[0].min - (inputs[1].min if inputs[1].min >=0 else abs(inputs[1].min))
  maximum = inputs[0].max + inputs[1].max
  sigs.append(Signal(intbv(0, min=minimum, max=maximum)))
  for i in range(1, number_of_signals):
    minimum = inputs[i].min - (sigs[i-1].min if sigs[i-1].min >=0 else abs(sigs[i-1].min))
    maximum = inputs[i].max + sigs[i-1].max
    sigs.append(Signal(intbv(0, min=minimum, max=maximum)))
  adders = []
  adders.append(adder(inputs[0], inputs[1], sigs[0]))
  adders += [adder(inputs[i+1], sigs[i-1], sigs[i]) for i in range(1, number_of_adders - 1)]
  adders.append(adder(inputs[number_of_inputs-1], sigs[number_of_signals-1], output))

  return adders

@block
def step_activation(input, output):
  @always_comb
  def logic():
    """ Step activation function"""
    if input >= 0:
      # Set to fixed point division value, because that represents 1
      output.next = ai_info.fixed_point_division
    else:
      output.next = 0
  return logic

@block
def sigmoid_activation(input, output):

  offset = ai_info.fixed_point_division // 2

  input_multiplied = Signal(intbv(0, input.min*512, input.max*512))
  absolute_input = Signal(intbv(1, input.min*512, input.max*512))
  denom = Signal(intbv(0, input.min*512, input.max*512))
  fract = Signal(intbv(0, input.min*512, input.max*512))

  mult_inst = multiplier(input, offset, input_multiplied)
  abs_inst = absolute(input, absolute_input)
  denom_add = adder(absolute_input, ai_info.fixed_point_division, denom)
  div_inst = divider(input_multiplied, denom, fract)
  fract_add = adder(fract, offset, output)

  return mult_inst, abs_inst, denom_add, div_inst, fract_add

@block
def ramp_activation(input, output):
  @always_comb
  def logic():
    """ Ramp activation function"""
    if input >= 0:
      output.next = (ai_info.fixed_point_division) if (input > ai_info.fixed_point_division) else input
    else:
      output.next = 0
  return logic

@block
def forward_input(input, output):
  @always_comb
  def logic():
    """ Forward input """
    output.next = input
  return logic

@block
def neuron(output: Signal = None, inputs = None, weights = None, bias = None):

  processes = []

  if output == None or inputs == None:
    raise ValueError("inputs and output should not be None")
  elif weights is None:
    if isinstance(inputs, list):
      raise ValueError("If there are no weights or bias, there should be one input (input layer)")
    else:
      neuron_type = "input"
  else:
    if len(inputs) != len(weights):
      raise ValueError("the length of inputs should be equal to the length of weights")
    neuron_type = "general"

  if neuron_type == "general":
    sum_minimum = 0
    sum_maximum = 0
    for i in range(len(inputs)):
      sum_maximum += inputs[i].max * weights[i].max
    sum_minimum = -(sum_maximum)
    sum_output = Signal(intbv(0, min=sum_minimum, max=sum_maximum))
  else:
    sum_output = Signal(intbv(0, -(2**(ai_info.signed_bus_width - 1 + len(inputs))), 2**(ai_info.signed_bus_width - 1 + len(inputs)) - 1))



  # Check what type of activation we are using for output logic
  if ai_info.activation_type == "step":
    processes.append(step_activation(sum_output, output))
  elif ai_info.activation_type == "ramp":
    processes.append(ramp_activation(sum_output, output))
  elif ai_info.activation_type == "sig":
    processes.append(sigmoid_activation(sum_output, output))
  else:
    raise RuntimeError("activation_type \"" + str(ai_info.activation_type) + "\" is not yet supported")

  if neuron_type == "input":
    processes.append(forward_input(inputs, sum_output))
  else:
    multiplied_signals = [Signal(intbv(val=0, min=-(2**(ai_info.signed_bus_width - 1)), max=2**(ai_info.signed_bus_width - 1)-1)) for _ in range(len(inputs))]
    processes.append(parallel_multiplier(inputs, weights, multiplied_signals))
    if bias is not None:
      processes.append(list_adder(inputs=multiplied_signals+[bias], output=sum_output))
    else:
      processes.append(list_adder(inputs=multiplied_signals, output=sum_output))

  return processes



@block
def neuron_wrapper(o, in2,in1, in3, in4, in5,w1,w2,w3,w4, w5):
  inputs = [in1,in2,in3,in4,in5]
  weights = [w1,w2, w3,w4,w5]
  output = o

  return neuron(output=output, inputs=inputs, weights=weights)

def convert():
  weight1, weight2, w3, w4, w5 = [Signal(intbv(0, -(2**(ai_info.signed_bus_width - 1)), 2**(ai_info.signed_bus_width - 1) - 1)) for _ in range(5)]
  inp1, inp2, inp3, inp4, inp5 = [Signal(intbv(0, -(2**(ai_info.signed_bus_width - 1)), 2**(ai_info.signed_bus_width - 1) - 1)) for _ in range(5)]
  output = Signal(intbv(0, -(2**(ai_info.signed_bus_width - 1)), 2**(ai_info.signed_bus_width - 1) - 1))
  inst = neuron_wrapper(w1=weight1, w2=weight2, w3=w3, w4=w4, w5=w5,in1=inp1, in2=inp2, in3=inp3, in4=inp4, in5=inp5,  o=output)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)
  toVHDL.std_logic_ports = True
  toVHDL.directory = "../vhdl/neural_network/"
  toVHDL(inst, initial_value=True)

@block
def tb_neuron():
  w1, w2, w3, w4, w5 = [Signal(intbv(0, -(2**(ai_info.signed_bus_width - 1)), 2**(ai_info.signed_bus_width - 1) - 1)) for _ in range(5)]
  inp1, inp2, inp3, inp4, inp5 = [Signal(intbv(0, -(2**(ai_info.signed_bus_width - 1)), 2**(ai_info.signed_bus_width - 1) - 1)) for _ in range(5)]
  output = Signal(intbv(0, -(2**(ai_info.signed_bus_width - 1)), 2**(ai_info.signed_bus_width - 1) - 1))
  inst = neuron_wrapper(w1=w1, w2=w2, w3=w3, w4=w4, w5=w5,in1=inp1, in2=inp2, in3=inp3, in4=inp4, in5=inp5,  o=output)

  @instance
  def stimuli():
    for i in range(-200, 200):
      w1.next = 2 * i
      w1.next = 4 * i
      w3.next = 6 * i
      w4.next = 8 * i
      w5.next = 10 * i
      inp1.next = 1 * abs(i)
      inp2.next = 2 * abs(i)
      inp3.next = 3 * abs(i)
      inp4.next = 4 * abs(i)
      inp5.next = 5 * abs(i)
      yield delay(10)
      sum_outcome = int(2 * 1 * i * abs(i)) // ai_info.fixed_point_division
      sum_outcome += int(4 * 2 * i * abs(i)) // ai_info.fixed_point_division
      sum_outcome += int(6 * 3 * i * abs(i)) // ai_info.fixed_point_division
      sum_outcome += int(8 * 4 * i * abs(i)) // ai_info.fixed_point_division
      sum_outcome += int(10 * 5 * i * abs(i)) // ai_info.fixed_point_division
      #print("%d Input sum = %d output = %d" % (now(), sum_outcome, output))
      if ai_info.activation_type == "step":
        if (output == ai_info.fixed_point_division) and sum_outcome < 0:
          raise AttributeError("Output became high while not matching with the input")
      elif ai_info.activation_type == "ramp":
        if (output == ai_info.fixed_point_division) and sum_outcome < (ai_info.fixed_point_division - 1):
          raise AttributeError("Output became high while not matching with the input")
        elif output == 0 and sum_outcome >= ai_info.fixed_point_division:
          raise AttributeError("Output is not high while it should be with this input")
      yield delay(10)
    print(Fore.GREEN + "Passed neuron test" + Fore.RESET)
    yield StopSimulation()

  return instances()

@block
def tb_multiplier():
  input, weight = [Signal(intbv(0,-2048,2048)) for _ in range(2)]
  output = Signal(intbv(0, -8388608, 8388608))
  inst = multiplier(input, weight, output)

  @instance
  def stimuli():
    for i in range(-2048, 2048):
      input.next = i
      weight.next = i
      yield delay(10)
      if i**2//1024 != output:
        raise RuntimeError("Output is not valid")
    print(Fore.GREEN + "Passed multiplier test" + Fore.RESET)
    yield StopSimulation()

  return inst, stimuli

@block
def tb_adder():
  a,b = [Signal(intbv(0,-1024, 1024), delay=5) for _ in range(2)]
  c = Signal(intbv(0, -2048, 2048), delay=5)
  inst = adder(a,b,c)

  @instance
  def stimuli():
    for i in range(-1024, 1024):
      a.next = i
      b.next = i
      for i in range(10):
        yield delay(1)
      if c != (a+b):
        raise RuntimeError("C is not correct")
      for i in range(10):
        yield delay(1)

    print(Fore.GREEN + "passed adder test" + Fore.RESET)
    yield StopSimulation()

  return inst, stimuli

def test_multiplier():
  vcd_path = os.path.join(os.getcwd(), TRACE_LOCATION, tb_multiplier.__name__ + ".vcd")
  if os.path.exists(vcd_path):
    #print("Removed old vcd file")
    os.remove(vcd_path)

  inst = tb_multiplier()
  inst.config_sim(trace=True, directory=TRACE_LOCATION)
  inst.run_sim()

def test_adder():

  vcd_path = os.path.join(os.getcwd(), TRACE_LOCATION, tb_adder.__name__ + ".vcd")
  if os.path.exists(vcd_path):
    #print("Removed old vcd file")
    os.remove(vcd_path)

  inst = tb_adder()
  inst.config_sim(trace=True, directory=TRACE_LOCATION)
  inst.run_sim()

def test():
  vcd_path = os.path.join(os.getcwd(), TRACE_LOCATION, tb_neuron.__name__ + ".vcd")
  if os.path.exists(vcd_path):
    #print("Removed old vcd file")
    os.remove(vcd_path)

  tb = tb_neuron()
  tb.config_sim(trace=True, directory=TRACE_LOCATION)
  tb.run_sim()

if __name__ == "__main__":
  test_adder()
  test_multiplier()
  test()
  convert()
