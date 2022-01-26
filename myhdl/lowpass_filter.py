from myhdl import *
import math as m
import matplotlib.pyplot as plt


@block
def low_pass_filter(clk, din, dout, cutoff_frequency, sample_frequency, gain, clr=None, nrst=None):
  if cutoff_frequency >= (sample_frequency/2):
    raise ValueError("cutoff frequency must be between 0 and sample_frequency/2")
  r_value = (1.0 - (2.0 * m.pi * (cutoff_frequency/sample_frequency)))
  d_value = (gain + 1) / (gain - r_value)
  c_value = 1/d_value

  # make values workable for integers
  r_value = int(r_value * 1000)
  c_value = int(c_value * 1000)

  last_in_value = Signal(intbv(0, din.min, din.max))
  last_out_value = Signal(intbv(0, dout.min, dout.max))
  current_out_value = Signal(intbv(0, dout.min, dout.max))

  @always(clk.posedge)
  def update_output():
    """ Update output """
    dout.next = current_out_value

  @always_comb
  def update_current_value():
    """ Apply filter """
    calculated_value = r_value * last_out_value
    calculated_value += c_value * last_in_value
    calculated_value += c_value * din
    calculated_value //= 1000
    current_out_value.next = calculated_value

  @always(clk.posedge)
  def process():
    """ Update last values """
    last_out_value.next = current_out_value
    last_in_value.next = din

  return instances()

@block
def tb_low_pass_filter():

  CUTOFF_FREQUENCY = 1500
  SAMPLE_FREQUENCY = 48E3
  GAIN = 1.0

  PERIOD_SECONDS = 1/SAMPLE_FREQUENCY
  PERIOD = int(1/SAMPLE_FREQUENCY * 1E9)
  SAMPLES = 125

  INPUT_FREQUENCY_1 = 800
  INPUT_FREQUENCY_2 = 5000

  data_list = []
  for i in range(SAMPLES):
    data_list.append(400 + int(200*m.sin(2 * m.pi * INPUT_FREQUENCY_1 * (i * PERIOD_SECONDS)) + 50*m.sin(2 * m.pi * INPUT_FREQUENCY_2 * (i * PERIOD_SECONDS))))

  data_tuple = tuple(data_list)
  x_list = []
  for i in range(SAMPLES):
    x_list.append(i*PERIOD_SECONDS)


  plt.plot(x_list,data_list)
  plt.grid(True)
  plt.show()

  temp_data = Signal(intbv(0,-(2**10), 2**10-1))

  clk = Signal(False)
  din, dout = [Signal(intbv(0,-(2**10), 2**10-1)) for _ in range(2)]

  inst = low_pass_filter(clk=clk, din=din, dout=dout, cutoff_frequency=CUTOFF_FREQUENCY, sample_frequency=SAMPLE_FREQUENCY, gain=GAIN)


  @instance
  def stimuli():
    clk.next = False
    din.next = 0
    for i in range(SAMPLES):
      yield delay(PERIOD//2)
      clk.next = True
      temp_data.next = data_tuple[i]
      yield delay(PERIOD//2)
      clk.next = False
      din.next = temp_data
      print("data_tuple", i, "is", temp_data)
    yield StopSimulation()

  return instances()

def convert():
  CUTOFF_FREQUENCY = 10E3
  SAMPLE_FREQUENCY = 48.8E3
  GAIN = 1.0

  clk = Signal(False)
  din, dout = [Signal(intbv(0,-(2**23), 2**23-1)) for _ in range(2)]

  inst = low_pass_filter(clk=clk, din=din, dout=dout, cutoff_frequency=CUTOFF_FREQUENCY, sample_frequency=SAMPLE_FREQUENCY, gain=GAIN)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)
  toVHDL.std_logic_ports = True
  toVHDL.directory = "../vhdl/"
  toVHDL(inst, initial_value=True)

if __name__ == "__main__":

  tb = tb_low_pass_filter()
  tb.config_sim(trace=True)
  tb.run_sim()

  convert()
