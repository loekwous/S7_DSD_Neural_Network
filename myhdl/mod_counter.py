from myhdl import *

@block
def mod_counter(clk, en, clr, dout, top, max_value=None):

  if max_value is not None:
    counter = Signal(intbv(0, 0, max_value+1))
  else:
    counter = Signal(intbv(0)[len(dout):])

  @always_comb
  def update_dout():
    dout.next = counter

  @always_comb
  def update_top():
    if counter == counter.max -2:
      top.next = True
    else:
      top.next = False

  @always(clk.posedge)
  def update_counter():
    if clr == True:
      counter.next = 0
    elif en == True:
      if counter < counter.max - 2:
        counter.next = counter + 1
      else:
        counter.next = 0
  return instances()

@block
def tb_mod_counter():
  dout = Signal(intbv(0,0, 81))
  clk, clr, en, top = [Signal(bool(0)) for _ in range(4)]

  cnt = mod_counter(clk=clk, clr=clr, en=en, top=top, dout=dout, max_value=80)

  @instance
  def stimuli():
    step_one_counting = False
    step_two_clearing = False
    step_three_top = False
    step_four_overflow = False
    en.next = True
    yield delay(10)
    clk.next = True
    yield delay(10)
    clk.next = False
    if dout == 1:
      step_one_counting = True
    clr.next = True
    yield delay(10)
    clk.next = True
    yield delay(10)
    clr.next = False
    clk.next = False
    if dout == 0:
      step_two_clearing = True
    yield delay(10)

    for i in range(1,81):
      yield delay(10)
      clk.next = True
      yield delay(10)
      clk.next = False
      if i == 79 and top == True:
        step_three_top = True
      if i == 79 and dout != 79:
        step_one_counting = False
      if i == 80 and dout == 0:
        step_four_overflow = True


    print("<=== Results ===>")
    print("cnt:", step_one_counting)
    print("clr:", step_two_clearing)
    print("top:", step_three_top)
    print("ovf:", step_four_overflow)

  return instances()

def Main():
  dout = Signal(intbv(0,0, 81))
  clk, clr, en, top = [Signal(bool(0)) for _ in range(4)]

  cnt = mod_counter(clk=clk, clr=clr, en=en, top=top, dout=dout, max_value=80)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "../vhdl/video_controller/"
  toVHDL(cnt, initial_value=True)
  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(cnt, initial_value=True)

if __name__ == "__main__":
  tb = tb_mod_counter()
  tb.config_sim(trace=True)
  tb.run_sim(20*100)
  Main()
