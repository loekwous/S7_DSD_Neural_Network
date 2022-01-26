from myhdl import *
import math

@block
def ram_module_conc(clk, din, addrw, addrr, we, dout, nrst, storage_locations = 2**32):

  MAX_ADDRESS_WIDTH = max(len(addrw),len(addrr))
  MAX_ADDRESS_VAL = 2**MAX_ADDRESS_WIDTH
  mem_size = min(MAX_ADDRESS_VAL, int(storage_locations))
  mem = [Signal(bool(0)) for _ in range(mem_size)]


  @always(clk.posedge)
  def write_handle():
    """ Write to RAM on positive edge of the clock.
    This function is secured to not write to unexisting locations"""
    if we == True:
      if addrw < int(mem_size):
        mem[addrw].next = din
        # if __debug__:
        #   print(now(), "RAM", " write mem[", int(addrw), "] =", int(din), "clk:", int(clk), "we", int(we))
      else:
        mem[intbv(int(storage_locations)) - 1].next = din

  @always_comb
  def read_handle():
    dout.next = mem[addrr]
    # if __debug__:
    #   print(now(),"RAM", "read mem[", int(addrr), "] =", int(mem[addrr]))

  return write_handle, read_handle

@block
def ram_testbench(clk, din, addrw, addrr, we, dout, nrst, storage_locations = 2**32):
  memory = ram_module_conc(din=din, addrr=addrr, addrw=addrw, we=we, clk=clk, dout=dout, nrst=nrst, storage_locations=STORAGE_LOCATIONS)
  counter = Signal(intbv(0,0,STORAGE_LOCATIONS))

  @instance
  def stimuli():
    addrr.next = 0
    addrw.next = 0
    yield delay(10)
    nrst.next = False
    yield delay(10)
    nrst.next = True
    yield delay(10)

    # Writing to location 0 with value 1
    we.next = True
    din.next = True
    yield delay(5)
    clk.next = True
    yield delay(5)
    clk.next = False
    din.next = False
    if dout != True:
      print("memory is not writing...")
      assert ("memory is not writing")

    yield delay(5)
    nrst.next = False
    yield delay(5)
    if dout == True:
      print("nrst is not working")
      assert ("nrst is not working")
    nrst.next = True
    yield delay(5)

    din.next = True
    we.next = True
    print("Testing memory locations")
    for i in range(STORAGE_LOCATIONS - 1):
      yield delay(5)
      clk.next = True
      yield delay(5)
      if dout != True:
        print("memory location", int(addrr), "is not working")
        assert ( "memory location is not working")
      yield delay(5)
      clk.next = False
      addrr.next = addrr + 1
      addrw.next = addrw + 1


  return instances()

if __name__ == "__main__":
  SCR_WIDTH = 640 / 8
  SCR_HEIGHT = 480 / 8
  STORAGE_LOCATIONS = int(SCR_HEIGHT * SCR_WIDTH)
  ADDR_BITS = math.ceil(math.log(SCR_WIDTH*SCR_HEIGHT,2))
  din = Signal(bool(0))
  dout = Signal(bool(0))
  addrw = Signal(intbv(0)[ADDR_BITS:])
  addrr = Signal(intbv(0)[ADDR_BITS:])
  we = Signal(bool(0))
  nrst = Signal(bool(1))
  clk = Signal(bool(0))

  tb = ram_testbench(din=din, addrr=addrr, addrw=addrw, we=we, clk=clk, dout=dout, nrst=nrst, storage_locations=STORAGE_LOCATIONS)

  tb.run_sim(500)

  system = ram_module_conc(din=din, addrr=addrr, addrw=addrw, we=we, clk=clk, dout=dout, nrst=nrst, storage_locations=STORAGE_LOCATIONS)
  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out"
  toVHDL(system)
  toVHDL.std_logic_ports = True
  toVHDL.directory = "../vhdl/video_controller"
  toVHDL(system)
