import os
from myhdl import *
from colorama import Fore, init

init()

if "TRACE_LOCATION" not in globals():
  TRACE_LOCATION = "traces/"

@block
def shift_reg_data(clk, clr, en, data_in, data_out):
  if len(data_in) != 1:
    raise ValueError("Data in should be one bit")
  reg = Signal(intbv(0, data_out.min, data_out.max))

  reg_len = len(reg)

  @always_comb
  def output_logic():
    data_out.next = reg

  @always(clk.posedge)
  def logic():
    if clr == True:
      reg.next = 0
    elif en == True:
      val = reg[reg_len:0]
      reg.next = concat(val, data_in)

  return output_logic, logic

@block
def tb_shift_reg_data():
  clk, clr, en, data_in = [Signal(False) for _ in range(4)]
  data_out = Signal(intbv(0, 0, 256))

  inst = shift_reg_data(clk=clk, clr=clr, en=en, data_in=data_in, data_out=data_out)

  check_list = [1]
  for i in range(1, len(data_out)):
    check_list.append(check_list[i-1] * 2 + 1)
  check_list = tuple(check_list)

  n_shifts = len(data_out)

  @instance
  def stimuli():

    data_in.next = True
    clr.next = False
    en.next = True
    yield delay(10)
    clk.next = True
    yield delay(10)
    clk.next = False
    clr.next = True
    if data_out != 1:
      print(Fore.RED + "something went wrong, data is not set to 1 before clearing" + Fore.RESET)
      yield StopSimulation()
    yield delay(10)
    clk.next = True
    yield delay(10)
    clk.next = False
    clr.next = False
    if data_out != 0:
      print(Fore.RED + "something went wrong, clear not working" + Fore.RESET)
      yield StopSimulation()

    data_in.next = True
    clr.next = False
    en.next = True

    yield delay(10)
    for i in range(n_shifts):
      clk.next = True
      yield delay(10)
      clk.next = False
      yield delay(10)
      if data_out != check_list[i]:
        print(1<<i)
        print(int(data_out))
        print(Fore.RED + "something went wrong, value not updated" + Fore.RESET)
        yield StopSimulation()
    print(Fore.GREEN + "Passed test" + Fore.RESET)
    yield StopSimulation()

  return instances()

def test():
  vcd_path = os.path.join(os.getcwd(), TRACE_LOCATION, tb_shift_reg_data.__name__ + ".vcd")
  if os.path.exists(vcd_path):
    #print("Removed old vcd file")
    os.remove(vcd_path)

  inst = tb_shift_reg_data()

  inst.config_sim(trace=True, directory=TRACE_LOCATION)
  inst.run_sim()

def convert():
  clk, clr, en, data_in = [Signal(False) for _ in range(4)]
  data_out = Signal(intbv(0, 0, 256))

  inst = shift_reg_data(clk=clk, clr=clr, en=en, data_in=data_in, data_out=data_out)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)
  print(Fore.GREEN + "Converted file" + Fore.RESET)


if __name__ == "__main__":

  test()

  convert()
