from myhdl import *
import math
from position_validator import Triangle, Canvas
import matplotlib.pyplot as plt
import numpy as np

def get_sample_tuple(n_samples, max_val=Triangle.bottom - Triangle.top - 2):
  temp_samples = []
  a = 2 * max_val / (n_samples-1)
  for i in range(n_samples):
    if i <= n_samples/2:
      temp_samples.append(int(i*a))
    else:
      temp_samples.append(int((max_val) - a*(i - (n_samples/2))))

  return tuple(temp_samples)

@block
def triangle_generator(clk, clear, dout, n_samples=33):

  samples = get_sample_tuple(n_samples)
  x_axis = np.linspace(0, n_samples - 1, n_samples)
  y_axis = np.array(samples)
  plt.plot(x_axis, y_axis)
  plt.grid()
  plt.show()
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
def tb_tri_gen(period, clk, clear, dout, samples):

  inst = triangle_generator(clk=clk, clear=clear, dout=dout, n_samples=samples)

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
    if dout != 0:
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
  SAMPLES = Triangle.right - Triangle.left
  clk = Signal(bool(0))
  clear = Signal(bool(0))
  dout = Signal(intbv(0,0, Canvas.height))
  inst = triangle_generator(clk=clk, clear=clear, dout=dout, n_samples=SAMPLES)
  toVHDL.std_logic_ports = True
  toVHDL.directory = "../vhdl/video_controller/"
  toVHDL(inst, initial_value=True)
  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)

if __name__ == "__main__":
  PERIOD = 20
  SAMPLES = Triangle.right - Triangle.left
  clk = Signal(bool(0))
  clear = Signal(bool(0))
  dout = Signal(intbv(0,0, Canvas.height))

  tb = tb_tri_gen(clk=clk, clear=clear, dout=dout, period=PERIOD, samples=SAMPLES)
  tb.config_sim(trace=True)
  tb.run_sim(SAMPLES * PERIOD + 6 * PERIOD)

  Main()
