import os
from myhdl import *

from neural_network_info import ai_info
from clocked_neuron import neuron_clocked
from multiplexer import multiplexer
from bin_to_dec import bin_to_dec

if "TRACE_LOCATION" not in globals():
  TRACE_LOCATION = "traces/"

@block
def layer(clk, clr, we, sel_neuron, sel_input, sel_funct, data_in, data_out, n_inputs=1, n_neurons=10):
  min_num = data_out.min
  max_num = data_out.max
  # check number of outputs

  output_list = [Signal(intbv(0, min_num, max_num)) for _ in range(n_neurons)]
  neuron_select = [Signal(False) for _ in range(n_neurons)]


  neuron_selector = bin_to_dec(en=we, bin=sel_neuron, dec=neuron_select)
  # create list of neurons
  neuron_list = []
  for i in range(n_neurons):
    neuron_list.append(neuron_clocked(clk=clk, en=neuron_select[i], clr=clr, data=data_in, outp=output_list[i], sel=sel_input, funct=sel_funct, n_inputs=n_inputs))

  multiplex = multiplexer(inputs=output_list, sel=sel_neuron, outp=data_out)

  return neuron_list, multiplex, neuron_selector

@block
def tb_layer():
  clk, clr, we = [Signal(False) for _ in range(3)]
  data_in, data_out = [Signal(intbv(0,-2**31, 2**31-1)) for _ in range(2)]
  sel_neuron = Signal(intbv(0,0,ai_info.number_of_neurons_per_layer))
  sel_input = Signal(intbv(0, 0, 5))
  sel_funct = Signal(intbv(0, 0,3))
  inst = layer(clk=clk, clr=clr, we=we, sel_neuron=sel_neuron, sel_input=sel_input, sel_funct=sel_funct, data_in=data_in, data_out=data_out, n_inputs=5, n_neurons=5)


  @instance
  def stimuli():
    clk.next = False
  return instances()

def convert():
  clk, clr, we = [Signal(False) for _ in range(3)]
  data_in, data_out = [Signal(intbv(0,-2**31, 2**31-1)) for _ in range(2)]

  n_neurons = 5
  sel_neuron = Signal(intbv(0,0,n_neurons))
  sel_input = Signal(intbv(0, 0, 5))
  sel_funct = Signal(intbv(0, 0,3))
  inst = layer(clk=clk, clr=clr, we=we, sel_neuron=sel_neuron, sel_input=sel_input, sel_funct=sel_funct, data_in=data_in, data_out=data_out, n_inputs=5, n_neurons=n_neurons)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)


@block
def tb_layer():
  clk, clr, we = [Signal(False) for _ in range(3)]
  data_in, data_out = [Signal(intbv(0,-2**31, 2**31-1)) for _ in range(2)]

  n_neurons = 5
  n_inputs = 2
  sel_neuron = Signal(intbv(0,0,n_neurons))
  sel_input = Signal(intbv(0, 0, n_inputs))
  sel_funct = Signal(intbv(0, 0,3))
  inst = layer(clk=clk, clr=clr, we=we, sel_neuron=sel_neuron, sel_input=sel_input, sel_funct=sel_funct, data_in=data_in, data_out=data_out, n_inputs=n_inputs, n_neurons=n_neurons)


  @instance
  def stimuli():
    clr.next = False
    clk.next = False
    sel_neuron.next = 0
    sel_input.next = 0
    sel_funct.next = 0
    data_in.next = 0
    we.next = False

    input_data_list = [[128, 128],[256,512], [128, 256], [256, 128], [0, 128]]
    weight_data_list = [-1024, 2048]

    for i in range(n_neurons):
      print("expected_output {} = {}".format(i, (input_data_list[i][0] * weight_data_list[0])//1024 + (input_data_list[i][1] * weight_data_list[1])//1024))

    #clear device
    yield delay(10)
    clr.next = True
    yield delay(10)
    clk.next = True
    yield delay(10)
    clk.next = False
    clr.next = False

    for neuron in range(n_neurons):
      sel_neuron.next = neuron
      we.next = True
      yield delay(10)
      for inp in range(n_inputs):
        sel_funct.next = 0 # input
        sel_input.next = inp
        data_in.next = input_data_list[neuron][inp]
        clk.next = False
        yield delay(10)
        clk.next = True
        yield delay(10)
      for weight in range(n_inputs):
        sel_funct.next = 1 # weight
        sel_input.next = weight
        data_in.next = weight_data_list[weight]
        clk.next = False
        yield delay(10)
        clk.next = True
        yield delay(10)

    yield delay(100)
    yield StopSimulation()

  return instances()

def test():

  vcd_path = os.path.join(os.getcwd(), TRACE_LOCATION, tb_layer.__name__ + ".vcd")
  if os.path.exists(vcd_path):
    #print("Removed old vcd file")
    os.remove(vcd_path)

  inst = tb_layer()
  inst.config_sim(trace=True, directory=TRACE_LOCATION)
  inst.run_sim()


if __name__ == "__main__":
  test()
  convert()
