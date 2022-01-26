import os
import time
from myhdl import *

if "TRACE_LOCATION" not in globals():
  TRACE_LOCATION = "traces/"

if __name__ == '__main__':
  from neural_network_info import ai_info
else:
  from .neural_network_info import ai_info

ONE_LINE = False

@block
def threshold_detector(in0, in1, in2, out0, out1, out2):

  @always_comb
  def logic():
    exact_half = (ai_info.fixed_point_division // 2)
    out0.next = True if in0 > exact_half else False
    out1.next = True if in1 > exact_half else False
    out2.next = True if in2 > exact_half else False

  return logic

@block
def tb_threshold_detector():
  in0, in1, in2 = [Signal(intbv(val=0, min=-(2**(ai_info.signed_bus_width)), max=2**(ai_info.signed_bus_width)-1)) for _ in range(3)]
  out0, out1, out2 = [Signal(False) for _ in range(3)]

  inst = threshold_detector(in0=in0, in1=in1, in2=in2, out0=out0, out1=out1, out2=out2)

  @instance
  def stimuli():
    exact_half = (ai_info.fixed_point_division //2)
    test_values = (-10, 0, exact_half-1, exact_half, exact_half+1)
    for test_value in test_values:
      yield delay(10)
      in0.next = intbv(test_value)
      in1.next = intbv(test_value)
      in2.next = intbv(test_value)
      yield delay(10)
      if __debug__ and __name__ == '__main__':
        print(now(), "test value = %d > %d -> %d" % (int(test_value), int(exact_half), int(out0)))
        yield delay(10)
      assert_expression_0 = (out0 == True and test_value > (exact_half)) or (out0 == False and test_value <= (exact_half))
      assert_expression_1 = (out1 == True and test_value > (exact_half)) or (out1 == False and test_value <= (exact_half))
      assert_expression_2 = (out2 == True and test_value > (exact_half)) or (out2 == False and test_value <= (exact_half))
      if __debug__:
        assert assert_expression_0 and assert_expression_1 and assert_expression_2, "Output value is not correct"
    if __debug__:
      yield StopSimulation()
  return instances()

def convert():
  in0, in1, in2 = [Signal(intbv(val=0, min=-(2**(ai_info.signed_bus_width)), max=2**(ai_info.signed_bus_width)-1)) for _ in range(3)]
  out0, out1, out2 = [Signal(False, delay=5) for _ in range(3)]

  inst = threshold_detector(in0=in0, in1=in1, in2=in2, out0=out0, out1=out1, out2=out2)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)
  toVHDL.std_logic_ports = True
  toVHDL.directory = "../vhdl/neural_network"
  toVHDL(inst, initial_value=True)

def test():
  #remove old trace if exists
  vcd_path = os.path.join(os.getcwd(), TRACE_LOCATION, tb_threshold_detector.__name__ + ".vcd")
  if os.path.exists(vcd_path):
    print("Removed old vcd file")
    os.remove(vcd_path)

  try:
    tb = tb_threshold_detector()
    tb.config_sim(trace=True, directory=TRACE_LOCATION)
    tb.run_sim()
    return True
  except:
    return False

if __name__ == '__main__':

  test()
  convert()
