import math
import os
from myhdl import *

if "TRACE_LOCATION" not in globals():
  TRACE_LOCATION = "traces/"

@block
def audio_rectifier(clk, en, audio_in, audio_out):
  div = 14
  @always(clk.posedge)
  def logic():
    if en == True:
      if audio_in >=0:
        audio_out.next = audio_in >> div
      else:
        audio_out.next = 0

  return instances()


@block
def tb_audio_rectifier():

  clk, en = [Signal(False) for _ in range(2)]
  n_samples = 100
  audio_list = tuple([int((2**23-1) * math.sin((1.0/n_samples)*2*math.pi * i)) for i in range(n_samples)])

  audio_in = Signal(intbv(0, -2**23, 2**23))
  audio_out = Signal(intbv(0, 0, 1024))

  inst = audio_rectifier(clk, en, audio_in, audio_out)

  @instance
  def stimuli():
    en.next = True
    for i in range(n_samples):
      clk.next = True
      yield delay(10)
      clk.next = False
      audio_in.next = audio_list[i]
      yield delay(10)
    yield StopSimulation()

  return instances()

def test():
  vcd_path = os.path.join(os.getcwd(), TRACE_LOCATION, tb_audio_rectifier.__name__ + ".vcd")
  if os.path.exists(vcd_path):
    #print("Removed old vcd file")
    os.remove(vcd_path)
  inst = tb_audio_rectifier()
  inst.config_sim(trace=True, directory=TRACE_LOCATION)
  inst.run_sim()



def convert():
  clk, en = [Signal(False) for _ in range(2)]
  audio_in = Signal(intbv(0, -2**23, 2**23))
  audio_out = Signal(intbv(0, 0, 1024))

  inst = audio_rectifier(clk, en, audio_in, audio_out)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)

if __name__ == "__main__":
  test()
  convert()
