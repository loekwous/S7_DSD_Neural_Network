import os
from myhdl import *

if "TRACE_LOCATION" not in globals():
  TRACE_LOCATION = "traces/"

@block
def tri_state_controller(write, read, tri_out):

  tri_out_driver = tri_out.driver()

  @always_comb
  def control_out():
    if tri_out == False:
      read.next = False
    else:
      read.next = True

  @always_comb
  def input_control():
      if write == True:
        tri_out_driver.next = None
      else:
        tri_out_driver.next = False


  return instances()

@block
def tb_tristate():
  write, read, rw= [Signal(bool(0)) for _ in range(3)]
  tri_out = TristateSignal(False)
  inst = tri_state_controller(rw, write, read, tri_out)

  @instance
  def stimuli():
    rw.next = True
    yield delay(25)
    write.next = True
    yield delay(20)
    write.next = False
    yield delay(20)
    rw.next = False
    yield delay(25)
    write.next = True
    yield delay(20)
    write.next = False
    yield delay(20)
    yield StopSimulation()

  return instances()

def test():
  vcd_path = os.path.join(os.getcwd(), TRACE_LOCATION, tb_tristate.__name__ + ".vcd")
  if os.path.exists(vcd_path):
    #print("Removed old vcd file")
    os.remove(vcd_path)
  tb = tb_tristate()
  tb.config_sim(trace=True, directory=TRACE_LOCATION)
  tb.run_sim()

def convert():
  write, read, rw = [Signal(bool(0)) for _ in range(3)]
  tri_out = TristateSignal(False)
  inst = tri_state_controller(rw, write, read, tri_out)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)

if __name__ == "__main__":

  test()
  convert()
