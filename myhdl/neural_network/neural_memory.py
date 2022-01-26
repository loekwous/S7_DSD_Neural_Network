from myhdl import *
import math

if __name__ == '__main__':
  from neural_network_info import *
else:
  from .neural_network_info import *

@block
def neural_memory(clk, we, write_address, read_address, din, dout):
  n_layers = ai_info.number_of_layers
  n_neurons_layer = ai_info.number_of_neurons_per_layer
  n_inputs = ai_info.number_of_inputs
  n_weights = ai_info.number_of_inputs
  memory_locations = (n_inputs + n_layers) * n_neurons_layer * n_layers
  databus_bit_width = ai_info.signed_bus_width

  memory = [Signal(intbv(0)[databus_bit_width:]) for _ in range(memory_locations)]

  @always(clk.posedge)
  def input_logic():
    if we == True:
      memory[write_address].next = din
    else:
      dout.next = memory[read_address]

  return instances()

def convert():
  n_layers = ai_info.number_of_layers
  n_neurons_layer = ai_info.number_of_neurons_per_layer
  n_inputs = ai_info.number_of_inputs
  n_weights = ai_info.number_of_inputs
  memory_locations = (n_inputs + n_layers) * n_neurons_layer * n_layers
  databus_bit_width = ai_info.signed_bus_width
  addressbus_bit_width = math.ceil(math.log(memory_locations,2))
  clk, we = [Signal(False) for _ in range(2)]
  write_address, read_address = [Signal(intbv(0)[addressbus_bit_width:]) for _ in range(2)]
  din, dout = [Signal(intbv(0)[databus_bit_width:]) for _ in range(2)]

  inst = neural_memory(clk=clk, we=we, write_address=write_address, read_address=read_address, din=din, dout=dout)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)
  toVHDL.std_logic_ports = True
  toVHDL.directory = "../vhdl/neural_network/"
  toVHDL(inst, initial_value=True)


if __name__ == "__main__":
  convert()
