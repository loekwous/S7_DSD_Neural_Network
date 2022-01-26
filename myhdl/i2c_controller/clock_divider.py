import os
from myhdl import *
import math

if "TRACE_LOCATION" not in globals():
  TRACE_LOCATION = "traces/"

@block
def clock_divider(clk, en, clk_out, incoming_frequency=50E6 ,target_frequency = 1E5):
  div = incoming_frequency / target_frequency
  div = int(div) // 2

  clk_out_sig = Signal(False)
  counter = Signal(intbv(0, 0, div+1))

  counter_max = counter.max -1

  @always_comb
  def output_logic():
    clk_out.next = clk_out_sig

  @always(clk.posedge)
  def update_output():
    if counter == counter_max:
      if en == True:
       clk_out_sig.next = not clk_out_sig
      else:
        clk_out_sig.next = False

  @always(clk.posedge)
  def cnt_update():
    if en == True:
      if counter < counter_max:
        counter.next = counter + 1
      else:
        counter.next = 0
    else:
      counter.next = 0
  return instances()


@block
def tb_clock_divider():
  clk, en, clk_out = [Signal(False) for _ in range(3)]
  incoming_frequency = 50E6
  target_frequency = 12.5E6
  inst = clock_divider(clk, en, clk_out, incoming_frequency=incoming_frequency ,target_frequency = incoming_frequency)

  div = incoming_frequency / target_frequency
  div = int(div)

  @instance
  def stimuli():
    en.next = False
    for i in range(div * 2):
      clk.next = False
      yield delay(10)
      clk.next = True
      yield delay(10)
    en.next = True
    for i in range(div * 2):
      clk.next = False
      yield delay(10)
      clk.next = True
      yield delay(10)
    en.next = False
    for i in range(div * 2):
      clk.next = False
      yield delay(10)
      clk.next = True
      yield delay(10)
    yield StopSimulation()
  return instances()

def test():
  vcd_path = os.path.join(os.getcwd(), TRACE_LOCATION, tb_clock_divider.__name__ + ".vcd")
  if os.path.exists(vcd_path):
    #print("Removed old vcd file")
    os.remove(vcd_path)
  inst = tb_clock_divider()

  inst.config_sim(trace=True, directory=TRACE_LOCATION)
  inst.run_sim()

def convert():
  clk, en, clk_out = [Signal(False) for _ in range(3)]
  inst = clock_divider(clk, en, clk_out, incoming_frequency=50E6 ,target_frequency = 10E4)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)

if __name__ == "__main__":
  test()
  convert()
