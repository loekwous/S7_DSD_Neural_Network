import os
from myhdl import *

if "TRACE_LOCATION" not in globals():
  TRACE_LOCATION = "traces/"

@block
def open_drain_output(clk_in, scl_out):

  dr = scl_out.driver()

  @always_comb
  def input_control():
      """ Open drain SCL output"""
      if clk_in == False and (scl_out == True or scl_out == False or scl_out == None):
        dr.next = False
      else:
        dr.next = None

  return instances()

@block
def tb_open_drain():
  clk_in = Signal(False)
  tri_out = TristateSignal(False)
  inst = open_drain_output(clk_in, tri_out)

  @instance
  def stimuli():
    for i in range(10):
      clk_in.next = False
      yield delay(10)
      clk_in.next = True
      yield delay(10)
    yield StopSimulation()

  return instances()

def test():
  vcd_path = os.path.join(os.getcwd(), TRACE_LOCATION, tb_open_drain.__name__ + ".vcd")
  if os.path.exists(vcd_path):
    #print("Removed old vcd file")
    os.remove(vcd_path)
  tb = tb_open_drain()
  tb.config_sim(trace=True, directory=TRACE_LOCATION)
  tb.run_sim()

def convert():
  clk_in = Signal(False)
  tri_out = TristateSignal(False)
  inst = open_drain_output(clk_in, tri_out)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)

if __name__ == "__main__":

  test()
  convert()
