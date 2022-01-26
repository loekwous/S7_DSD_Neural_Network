from myhdl import *

@block
def mux_3input(in0, in1, in2, sel, output):
  if 2**(sel.max-1) < 3:
    raise ValueError(" sel should be bigger to reach every input")

  @always_comb
  def logic():
    if sel == 0:
      output.next = in0
    elif sel == 1:
      output.next = in1
    else:
      output.next = in2

  return instances()


def convert():
  in0, in1, in2, output = [Signal(intbv(0, 0, 1024)) for _ in range(4)]
  sel = Signal(intbv(0,0,3))

  inst = mux_3input(in0, in1, in2, sel, output)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)

if __name__ == "__main__":
  convert()
