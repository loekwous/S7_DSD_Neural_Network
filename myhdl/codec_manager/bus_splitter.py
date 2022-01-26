from myhdl import *

@block
def splitter(din, a0, a1, a2, a3, a4, a5, a6, a7, a8, a9):

  @always_comb
  def logic():
    a0.next = din[0]
    a1.next = din[1]
    a2.next = din[2]
    a3.next = din[3]
    a4.next = din[4]
    a5.next = din[5]
    a6.next = din[6]
    a7.next = din[7]
    a8.next = din[8]
    a9.next = din[9]
  return logic

def convert():
  a0, a1, a2, a3, a4, a5, a6, a7, a8, a9 = [Signal(False) for _ in range(10)]
  din = Signal(intbv(0)[10:])
  inst = splitter(din, a0, a1, a2, a3, a4, a5, a6, a7, a8, a9)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)

if __name__ == "__main__":
  convert()
