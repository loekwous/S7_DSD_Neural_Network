import os
from myhdl import *
from colorama import Fore, init

init()

if "TRACE_LOCATION" not in globals():
  TRACE_LOCATION = "traces/"

@block
def reg_data(clk, clr, en, data_in, data_out):
  if len(data_in) != len(data_out):
    raise ValueError("Length of data_in and data_out should be equal")
  reg = Signal(intbv(0, data_in.min, data_in.max))

  @always_comb
  def output_logic():
    data_out.next = reg

  @always(clk.posedge)
  def logic():
    if clr == True:
      reg.next = 0
    elif en == True:
      reg.next = data_in

  return output_logic, logic

@block
def tb_reg_data():
  clk, clr, en = [Signal(False) for _ in range(3)]
  data_in, data_out = [Signal(intbv(0, 0, 256)) for _ in range(2)]

  inst = reg_data(clk=clk, clr=clr, en=en, data_in=data_in, data_out=data_out)

  max_val = data_in.max
  min_val = data_in.min

  @instance
  def stimuli():

    data_in.next = max_val -2
    clr.next = False
    en.next = True
    yield delay(10)
    clk.next = True
    yield delay(10)
    clk.next = False
    clr.next = True
    if data_out != max_val -2:
      print(Fore.RED + "something went wrong, data is not set to {} before clearing".format(max_val-2) + Fore.RESET)
      yield StopSimulation()
    yield delay(10)
    clk.next = True
    yield delay(10)
    clk.next = False
    clr.next = False
    if data_out != 0:
      print(Fore.RED + "something went wrong, clear not working" + Fore.RESET)
      yield StopSimulation()


    for i in range(min_val, max_val):
      data_in.next = i
      clk.next = False
      yield delay(10)
      clk.next = True
      yield delay(10)
      if data_out != i:
        print(Fore.RED + "something went wrong, value not updated" + Fore.RESET)
        yield StopSimulation()


    last_data = data_out
    clk.next = False
    en.next = False
    yield delay(10)
    clk.next = True
    yield delay(10)
    clk.next = False
    if data_out != last_data:
      print(Fore.RED + "something went wrong, enable is not working" + Fore.RESET)
      yield StopSimulation()

    print(Fore.GREEN + "Passed test" + Fore.RESET)
    yield StopSimulation()

  return instances()

def test():
  vcd_path = os.path.join(os.getcwd(), TRACE_LOCATION, tb_reg_data.__name__ + ".vcd")
  if os.path.exists(vcd_path):
    #print("Removed old vcd file")
    os.remove(vcd_path)

  inst = tb_reg_data()

  inst.config_sim(trace=True, directory=TRACE_LOCATION)
  inst.run_sim()

def convert():
  clk, clr, en = [Signal(False) for _ in range(3)]
  data_in, data_out = [Signal(intbv(0, 0, 256)) for _ in range(2)]

  inst = reg_data(clk=clk, clr=clr, en=en, data_in=data_in, data_out=data_out)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)
  print(Fore.GREEN + "Converted file" + Fore.RESET)


if __name__ == "__main__":

  test()

  convert()
