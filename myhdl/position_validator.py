from myhdl import *


class Canvas:
  width = int(80)
  height = int(60)

class Square:
  left = int(0)
  right = int(80/3 - 1)
  top = int(60/3)
  bottom = int(2*60/3)

class Triangle:
  left = int(80/3)
  right = int(2*80/3) -1
  top = int(60/3)
  bottom = int(2*60/3)

class Sine:
  left = int(2*80/3)
  right = int(79)
  top = int(60/3)
  bottom = int(2*60/3)

@block
def position_validator(x_pos, sq, sine, tri):
  @always_comb
  def behavior():
    if x_pos < Canvas.width:
      if x_pos >= Square.left and x_pos <= Square.right:
        sq.next = True
      else:
        sq.next = False

      if x_pos >= Triangle.left and x_pos <= Triangle.right:
        tri.next = True
      else:
        tri.next = False

      if x_pos >= Sine.left and x_pos <= Sine.right:
        sine.next = True
      else:
        sine.next = False
    else:
      sq.next = False
      sine.next = False
      tri.next = False

  return instances()

@block
def tb_position_validator():
  x_counter = Signal(intbv(0,0,80))
  sq, sine, tri = [Signal(bool(0)) for _ in range(3)]

  inst = position_validator(x_pos=x_counter, sq=sq, sine=sine, tri=tri)

  @instance
  def stimuli():
    for x in range(80):
      x_counter.next = x
      yield delay(10)
  return instances()

def Main():
  x_pos = Signal(intbv(0,0,80))
  sq, sine, tri = [Signal(bool(0)) for _ in range(3)]

  inst = position_validator(x_pos=x_pos, sq=sq, sine=sine, tri=tri)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "../vhdl/video_controller/"
  toVHDL(inst, initial_value=True)
  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_values=True)

if __name__ == "__main__":

  tb = tb_position_validator()
  tb.config_sim(trace=True)
  tb.run_sim(10*80 + 10)

  Main()
