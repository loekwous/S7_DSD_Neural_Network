import os
from myhdl import *

if "TRACE_LOCATION" not in globals():
  TRACE_LOCATION = "traces/"

@block
def counter(clk_i2c, en, ready, bit_select):
  counter = Signal(intbv(bit_select.max-1, bit_select.min-1, bit_select.max))

  max_val = counter.max -1
  min_val = counter.min

  @always_comb
  def output_logic():
    if counter >= 0:
      bit_select.next = counter
    else:
      bit_select.next = 0

  @always_comb
  def ready_logic():
    ready.next = True if counter == min_val else False

  @always(clk_i2c.negedge)
  def count_logic():
    if en == True:
      if counter > min_val:
        counter.next = counter - 1
    else:
      counter.next = max_val

  return instances()

@block
def tb_counter():
  clk_i2c, en, ready = [Signal(False) for _ in range(3)]
  bit_select  = Signal(intbv(0, 0, 8))

  inst = counter(clk_i2c, en, ready, bit_select)

  max_val = bit_select.max -1

  @instance
  def stimuli():
    en.next = False
    for i in range(max_val):
      clk_i2c.next = False
      yield delay(10)
      clk_i2c.next = True
      yield delay(10)
    en.next = True
    for i in range(max_val *2):
      clk_i2c.next = False
      yield delay(10)
      clk_i2c.next = True
      yield delay(10)
    en.next = False
    for i in range(max_val):
      clk_i2c.next = False
      yield delay(10)
      clk_i2c.next = True
      yield delay(10)
    yield StopSimulation()

  return instances()

def test():
  vcd_path = os.path.join(os.getcwd(), TRACE_LOCATION, tb_counter.__name__ + ".vcd")
  if os.path.exists(vcd_path):
    #print("Removed old vcd file")
    os.remove(vcd_path)
  inst = tb_counter()

  inst.config_sim(trace=True, directory=TRACE_LOCATION)
  inst.run_sim()

def convert():
  clk_i2c, en, ready = [Signal(False) for _ in range(3)]
  bit_select  = Signal(intbv(0, 0, 8))

  inst = counter(clk_i2c, en, ready, bit_select)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)

if __name__ == "__main__":
  test()
  convert()
