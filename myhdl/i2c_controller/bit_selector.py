from myhdl import *


@block
def bit_selector(input, sel, output):


  @always_comb
  def logic():
    value = input[sel]
    output.next = value

  return instances()


def convert():
  input = Signal(intbv(0, 0, 256))
  sel = Signal(intbv(0,0,len(input)))
  output = Signal(False)

  inst = bit_selector(input, sel, output)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)

if __name__ == "__main__":
  convert()
