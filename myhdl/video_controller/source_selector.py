from myhdl import *

if __name__ == '__main__':
  from position_validator import Canvas
else:
  from .position_validator import Canvas

@block
def source_selector(sel, x1,y1, x2,y2, x_out, y_out):

  @always_comb
  def output_control():
    if sel == True:
      x_out.next = x2
      y_out.next = y2
    else:
      x_out.next = x1
      y_out.next = y1

  return instances()

def convert():
  sel = Signal(False)
  x1, x2, x_out = [Signal(intbv(0,0,Canvas.width)) for _ in range(3)]
  y1, y2, y_out = [Signal(intbv(0,0,Canvas.height)) for _ in range(3)]

  inst = source_selector(sel, x1, y1, x2, y2, x_out, y_out)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "../vhdl/video_controller/"
  toVHDL(inst, initial_value=True)
  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)

if __name__ == "__main__":
  convert()
