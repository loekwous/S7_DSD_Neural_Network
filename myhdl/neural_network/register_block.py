from myhdl import *

@block
def register_block(clk, en, clr, input, output):

  reg = Signal(intbv(0, input.min, input.max))

  @always_comb
  def out_logic():
    """ Combinational part of register """
    output.next = reg

  @always(clk.posedge)
  def logic():
    """ Sequential part of register """
    if clr == True:
      reg.next = 0
    elif en == True:
      reg.next = input
    else:
      reg.next = reg
  return logic, out_logic

def convert():
  inp, outp = [Signal(intbv(val=0, min=-1024, max=1024)) for _ in range(2)]
  clk, en, clr = [Signal(False, delay=5) for _ in range(3)]

  inst = register_block(clk=clk, en=en, clr=clr, input=inp, output=outp)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)
  #toVHDL.std_logic_ports = True
  #toVHDL.directory = "../vhdl/neural_network"
  #toVHDL(inst, initial_value=True)

if __name__ == "__main__":
  convert()
