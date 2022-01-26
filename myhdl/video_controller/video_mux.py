from myhdl import *

@block
def video_mux(sel, A, B, C, output):
  @always_comb
  def behavior():
    if sel == 0:
      output.next = A
    elif sel == 1:
      output.next = B
    else:
      output.next = C

  return instances()

def convert():
  sel = Signal(intbv(0)[2:])
  A,B,C = [Signal(intbv(0,0,60)) for _ in range(3)]
  output = Signal(intbv(0,0,60))

  inst = video_mux(sel=sel, A=A, B=B, C=C, output=output)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "../vhdl/video_controller/"
  toVHDL(inst, initial_value=True)
  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)

if __name__ == "__main__":
  convert()
