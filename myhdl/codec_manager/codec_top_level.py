import os
from myhdl import *

from config_rom import rom_content
from controller import codec_controller
from counter import counter

if "TRACE_LOCATION" not in globals():
  TRACE_LOCATION = "traces/"

@block
def codec_top_level(clk, nrst, start, ready, i2c_success, i2c_start, i2c_ready, i2c_address, i2c_rw, i2c_data, i2c_data_address):

  cnt_clear, cnt_up, cnt_top = [Signal(False) for _ in range(3)]
  count_sig = Signal(intbv(0,0,4))

  inst_counter = counter(clk, cnt_clear, cnt_up, count_sig, cnt_top)
  inst_rom = rom_content(count_sig, i2c_address, i2c_rw, i2c_data_address, i2c_data)
  inst_controller = codec_controller(clk, nrst, start, ready, i2c_start, i2c_ready, i2c_success, cnt_clear, cnt_up, cnt_top)

  return instances()

@block
def tb_codec_top_level():
  clk, nrst, start, ready = [Signal(False) for _ in range(4)]
  i2c_start, i2c_ready, i2c_success = [Signal(False) for _ in range(3)]
  i2c_address = Signal(intbv(0)[7:])
  i2c_rw = Signal(False)
  i2c_address = Signal(intbv(0)[7:])
  i2c_rw = Signal(False)
  i2c_data, i2c_data_address = [Signal(intbv(0)[8:]) for _ in range(2)]

  inst = codec_top_level(clk, nrst, start, ready, i2c_success, i2c_start, i2c_ready, i2c_address, i2c_rw, i2c_data, i2c_data_address)

  @always(delay(10))
  def clock_gen():
    clk.next = not clk

  @instance
  def stimuli():
    nrst.next = True
    yield delay(15)
    nrst.next = False
    yield delay(20)
    nrst.next = True
    yield delay(80)
    start.next = True
    yield delay(20)
    start.next = False
    for i in range(3):
      yield delay(150)
      i2c_ready.next = True
      i2c_success.next = True
      while(i2c_start == False):
        yield delay(1)
      i2c_ready.next = False
      i2c_success.next = False
    yield delay(150)
    i2c_ready.next = True
    i2c_success.next = True

    yield delay(300)

    yield StopSimulation()

  return instances()

def test():
  vcd_path = os.path.join(os.getcwd(), TRACE_LOCATION, tb_codec_top_level.__name__ + ".vcd")
  if os.path.exists(vcd_path):
    #print("Removed old vcd file")
    os.remove(vcd_path)
  inst = tb_codec_top_level()
  inst.config_sim(trace=True, directory=TRACE_LOCATION)
  inst.run_sim()

def convert():
  clk, nrst, start, ready = [Signal(False) for _ in range(4)]
  i2c_start, i2c_ready, i2c_success = [Signal(False) for _ in range(3)]
  i2c_address = Signal(intbv(0)[7:])
  i2c_rw = Signal(False)
  i2c_address = Signal(intbv(0)[7:])
  i2c_rw = Signal(False)
  i2c_data, i2c_data_address = [Signal(intbv(0)[8:]) for _ in range(2)]

  inst = codec_top_level(clk, nrst, start, ready, i2c_success, i2c_start, i2c_ready, i2c_address, i2c_rw, i2c_data, i2c_data_address)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)

if __name__ == "__main__":
  test()
  convert()
