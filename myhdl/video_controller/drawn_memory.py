import os
from myhdl import *

if "TRACE_LOCATION" not in globals():
  TRACE_LOCATION = "traces/"

class DrawnInputs:
  def __init__(self):
    self.clr = Signal(bool(0))
    self.sq_t = Signal(bool(0))
    self.tri_t = Signal(bool(0))
    self.sin_t = Signal(bool(0))

class DrawnOutputs:
  def __init__(self):
    self.sq_o, self.sin_o, self.tri_o = [Signal(bool(0)) for _ in range(3)]

@block
def drawn_memory(clk, inputs: DrawnInputs, outputs: DrawnOutputs):

  sq_reg, tri_reg, sin_reg = [Signal(bool(0)) for _ in range(3)]

  @always_comb
  def update_output():
    outputs.sin_o.next = sin_reg
    outputs.sq_o.next = sq_reg
    outputs.tri_o.next = tri_reg

  @always(clk.posedge)
  def update_regs():
    if inputs.clr == True:
      sq_reg.next = False
      tri_reg.next = False
      sin_reg.next = False
    else:
      if inputs.sq_t == True:
        sq_reg.next = not sq_reg

      if inputs.tri_t == True:
        tri_reg.next = not tri_reg

      if inputs.sin_t == True:
        sin_reg.next = not sin_reg

  return instances()

@block
def tb_drawn_memory(clk, inputs: DrawnInputs, outputs: DrawnOutputs):

  inst = drawn_memory(clk, inputs, outputs)
  last_si, last_sq, last_tri = [Signal(False) for _ in range(3)]

  @instance
  def stimuli():
    while True:
      yield delay(5)
      clk.next = False
      inputs.sin_t.next = not inputs.sin_t
      inputs.sq_t.next = not inputs.sq_t
      inputs.tri_t.next = not inputs.tri_t
      yield delay(10)
      clk.next = True
      yield delay(2)
      output_condition = (last_si != outputs.sin_o) and (last_sq != outputs.sq_o) and (last_tri != outputs.tri_o)
      input_condition = inputs.sin_t and inputs.sq_t and inputs.tri_t
      if (input_condition and output_condition) or (not input_condition and not output_condition):
        if __name__ == "__main__":
          print(now(), "Update okay")
      else:
        assert False, "Updated value is incorrect"
      yield delay(3)
      last_si.next = outputs.sin_o
      last_tri.next = outputs.tri_o
      last_sq.next = outputs.sq_o

  return instances()

def convert():
  clk = Signal(bool(0))
  inputs = DrawnInputs()
  outputs = DrawnOutputs()
  inst = drawn_memory(clk=clk, inputs=inputs, outputs=outputs)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "../vhdl/video_controller/"
  toVHDL(inst, initial_value=True)
  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)

def test():
  clk = Signal(bool(0))
  inputs = DrawnInputs()
  outputs = DrawnOutputs()
  inst = drawn_memory(clk=clk, inputs=inputs, outputs=outputs)

  vcd_path = os.path.join(os.getcwd(), TRACE_LOCATION, tb_drawn_memory.__name__ + ".vcd")
  if os.path.exists(vcd_path):
    print("Removed old vcd file")
    os.remove(vcd_path)

  try:
    tb = tb_drawn_memory(clk=clk, inputs=inputs, outputs=outputs)
    tb.config_sim(trace=True, directory=TRACE_LOCATION)
    tb.run_sim(100)
    return True
  except:
    return False

if __name__ == "__main__":
  test()
  convert()
