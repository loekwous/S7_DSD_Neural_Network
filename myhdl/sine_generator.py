from myhdl import *
import math
from position_validator import Sine, Canvas
import matplotlib.pyplot as plt
import numpy as np

@block
def sine_generator(clk, clear, dout, n_samples=33):

  max_val = Sine.bottom - Sine.top
  temp_samples = [int((max_val/2-1) + (max_val/2-2)*math.sin(2* math.pi / (n_samples-1) * i)) for i in range(n_samples)]
  x_axis = np.linspace(0, n_samples - 1, n_samples)
  y_axis = np.array(temp_samples)
  plt.plot(x_axis, y_axis)
  plt.grid()
  plt.show()
  samples = tuple(temp_samples)
  counter = Signal(intbv(0, 0, n_samples))

  @always(clk.posedge)
  def counting_management():
    if clear == True:
      counter.next = 0
    else:
      if counter < n_samples - 1:
        counter.next = counter + 1
      else:
        counter.next = 0

  @always_comb
  def signal_generator():
    dout.next = samples[counter]

  return instances()

@block
def tb_sine_gen(period, clk, clear, dout, samples):

  inst = sine_generator(clk=clk, clear=clear, dout=dout, n_samples=samples)

  @instance
  def stimuli():

    yield delay(period//2)
    clk.next = True
    yield delay(period//2)
    clear.next = True
    clk.next = False
    yield delay(period//2)
    clk.next = True
    yield delay(period//2)
    if dout != 127 + 127*math.sin(0):
      print("clear is not working")
    clk.next = False
    clear.next = False

    for i in range(samples):
      yield delay(period//2)
      clk.next = True
      yield delay(period//2)
      clk.next = False
      print(now(), "i=", i, "dout=", int(dout))

  return instances()

def Main():
  SAMPLES = Sine.right - Sine.left

  clk = Signal(bool(0))
  clear = Signal(bool(0))
  dout = Signal(intbv(0,0,Canvas.height))
  inst = sine_generator(clk=clk, clear=clear, dout=dout, n_samples=SAMPLES)
  toVHDL.std_logic_ports = True
  toVHDL.directory = "../vhdl/video_controller/"
  toVHDL(inst, initial_value=True)
  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)

if __name__ == "__main__":

  SAMPLES = 100

  clk = Signal(bool(0))
  clear = Signal(bool(0))
  dout = Signal(intbv(0,0,Canvas.height))

  PERIOD = 20
  tb = tb_sine_gen(period=PERIOD, clk=clk, clear=clear, dout=dout, samples=SAMPLES)
  tb.config_sim(trace=True)
  tb.run_sim(SAMPLES * PERIOD + 6 * PERIOD)
  Main()
