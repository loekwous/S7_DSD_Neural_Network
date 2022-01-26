import os
from myhdl import *
from colorama import Fore, init

init()

if "TRACE_LOCATION" not in globals():
  TRACE_LOCATION = "traces/"


@block
def combiner(rw, address, data_out):
  if len(address) != 7:
    raise ValueError("Address should be 7 bit")

  @always_comb
  def logic():
    data_out.next = concat(address, rw)

  return logic

@block
def tb_combiner():
  rw = Signal(False)
  address = Signal(intbv(0)[7:])
  data_out = Signal(intbv(0)[8:])

  inst = combiner(rw=rw, address=address, data_out=data_out)

  @instance
  def stimuli():
    rw.next = False
    address.next = 1
    yield delay(10)
    if data_out != 2:
      print(Fore.RED + "data is not updating" + Fore.RESET)
      yield StopSimulation()
    yield delay(10)
    rw.next = True
    address.next = 127
    yield delay(10)
    if data_out != 255:
      print(Fore.RED + "data is not updating" + Fore.RESET)
      yield StopSimulation()
    print(Fore.GREEN + "Passed test" + Fore.RESET)
    yield StopSimulation()


  return inst, stimuli

def test():
  vcd_path = os.path.join(os.getcwd(), TRACE_LOCATION, tb_combiner.__name__ + ".vcd")
  if os.path.exists(vcd_path):
    #print("Removed old vcd file")
    os.remove(vcd_path)
  inst = tb_combiner()

  inst.config_sim(trace=True, directory=TRACE_LOCATION)
  inst.run_sim()

def convert():
  rw = Signal(False)
  address = Signal(intbv(0)[7:])
  data_out = Signal(intbv(0)[8:])

  inst = combiner(rw=rw, address=address, data_out=data_out)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)
  print(Fore.GREEN + "Converted file" + Fore.RESET)

if __name__ == "__main__":
  test()
  convert()
