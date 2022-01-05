from myhdl import *
import math


@block
def clock_divider(clk_in, clk_out, clock_div):
  div_val_check = math.log(clock_div, 2)
  div_val_check_int = int(div_val_check)
  if abs(div_val_check - div_val_check_int) > 1e-6:
    raise ValueError("Clock div {} is not in power of 2".format(clock_div))

  num_bits = int(math.log(clock_div,2))

  counter = Signal(intbv(0)[num_bits:])

  @always_comb
  def update_output():
    clk_out.next = counter[num_bits-1]

  @always(clk_in.posedge)
  def update_counter():
    if counter < counter.max - 1:
      counter.next = counter.next + 1
    else:
      counter.next = 0

  return instances()

@block
def test():
  clk_in, clk_out = [Signal(False) for _ in range(2)]
  inst = clock_divider(clk_in=clk_in, clk_out=clk_out, clock_div=2)

  @instance
  def stimuli():
    yield delay(10)
    clk_in.next = True
    yield delay(10)
    clk_in.next = False
    if clk_out == False:
      print("Clock is False but should be True")
    yield delay(10)
    clk_in.next = True
    yield delay(10)
    clk_in.next = False
    if clk_out == True:
      print("Clock is True but should be False")
    yield StopSimulation()

  return instances()


def Main():
  CLK_IN_FREQ = 50E6
  CLK_OUT_FREQ = 1

  nearest_div = int(2**math.floor(math.log( (CLK_IN_FREQ / CLK_OUT_FREQ) ,2) ))
  print("Nearest div = ", nearest_div)
  print("CLK_OUT_FREQ =", CLK_IN_FREQ/nearest_div)

  clk_in, clk_out = [Signal(False) for _ in range(2)]
  inst = clock_divider(clk_in=clk_in, clk_out=clk_out, clock_div=nearest_div)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "../vhdl/video_controller/"
  toVHDL(inst, initial_value=True)
  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)

if __name__ == "__main__":
  tb = test()
  tb.config_sim(trace=True)
  tb.run_sim()
  Main()
