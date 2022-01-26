import os
from myhdl import *

if "TRACE_LOCATION" not in globals():
  TRACE_LOCATION = "traces/"

from audio_rectifier import audio_rectifier

@block
def i2s_counter(clk, cnt_clr, cnt_up, cnt_top):
  count_top = 24

  counter = Signal(intbv(0,0,count_top+1))

  @always_comb
  def output_logic():
    if counter == count_top:
      cnt_top.next = True
    else:
      cnt_top.next = False

  @always(clk.posedge)
  def count_logic():
    if cnt_clr == True:
      counter.next = 0
    else:
      if cnt_up == True:
        if counter < count_top:
          counter.next = counter + 1
  return instances()

@block
def i2s_sipo(clk, nrst, en, din, dout):
  sr = Signal(intbv(0, dout.min, dout.max))
  bits = len(sr)

  @always_comb
  def output_logic():
    dout.next = sr

  @always(clk.posedge, nrst.negedge)
  def shift_logic():
    if nrst == False:
        sr.next = 0
    else:
       if en == True:
         sr.next = concat(sr[bits-2:0],din)
  return instances()

@block
def i2s_controller(clk, nrst, i2s_clk, i2s_frame, sipo_en, cnt_top, cnt_clr, cnt_up, rdy):

  t_states = enum("IDLE", "DELAY", "DELAY2", "CAPTURE", "WF_LOW", "WF_HIGH", "WF_END")

  p_s, n_s = [Signal(t_states.IDLE) for _ in range(2)]

  @always_comb
  def input_decoder():
    if p_s == t_states.IDLE and i2s_frame == True and i2s_clk == True:
      n_s.next = t_states.DELAY
    elif p_s == t_states.DELAY and i2s_frame == True and i2s_clk == False:
      n_s.next = t_states.DELAY2
    elif p_s == t_states.DELAY2 and i2s_frame == True and i2s_clk == True:
      n_s.next = t_states.CAPTURE
    elif p_s == t_states.CAPTURE:
      n_s.next = t_states.WF_LOW
    elif p_s == t_states.WF_LOW and i2s_frame == True and i2s_clk == False:
      n_s.next = t_states.WF_HIGH
    elif p_s == t_states.WF_HIGH and i2s_frame == True and i2s_clk == True:
      if cnt_top == True:
        n_s.next = t_states.WF_END
      else:
        n_s.next = t_states.CAPTURE
    elif p_s == t_states.WF_END and i2s_frame == False:
      n_s.next = t_states.IDLE
    else:
      n_s.next = p_s

  @always(clk.posedge, nrst.negedge)
  def memory():
    if nrst == False:
      p_s.next = t_states.IDLE
    else:
      p_s.next = n_s

  @always_comb
  def output_decoder():
    if p_s == t_states.IDLE:
      sipo_en.next = False
      cnt_clr.next = True
      cnt_up.next = False
      rdy.next = True
    elif p_s == t_states.DELAY:
      sipo_en.next = False
      cnt_clr.next = False
      cnt_up.next = False
      rdy.next = False
    elif p_s == t_states.DELAY2:
      sipo_en.next = False
      cnt_clr.next = False
      cnt_up.next = False
      rdy.next = False
    elif p_s == t_states.CAPTURE:
      sipo_en.next = True
      cnt_clr.next = False
      cnt_up.next = True
      rdy.next = False
    else:
      sipo_en.next = False
      cnt_clr.next = False
      cnt_up.next = False
      rdy.next = False
  return instances()

@block
def top_level_i2s(clk, nrst, i2s_clk, i2s_data, i2s_frame, dout, rdy):

  cnt_up, cnt_clr, cnt_top = [Signal(False) for _ in range(3)]
  sipo_en = Signal(False)

  inst_counter = i2s_counter(clk, cnt_clr, cnt_up, cnt_top)
  inst_sipo = i2s_sipo(clk, nrst, sipo_en, i2s_data, dout)
  inst_controller = i2s_controller(clk, nrst, i2s_clk, i2s_frame, sipo_en, cnt_top, cnt_clr, cnt_up, rdy)

  return instances()

@block
def tb_top_level_i2s():
  dout = Signal(intbv(0)[24:])
  audio_out = Signal(intbv(0)[10:])
  clk, nrst, i2s_clk, i2s_frame, i2s_data, rdy = [Signal(False) for _ in range(6)]
  inst = top_level_i2s(clk, nrst, i2s_clk, i2s_data, i2s_frame, dout, rdy)
  inst_rect = audio_rectifier(clk, rdy, dout, audio_out)

  @always(delay(1000))
  def clock_control():
    i2s_clk.next = not i2s_clk

  @always(delay(2*27000))
  def frame_control():
    i2s_frame.next = not i2s_frame

  @always(delay(10))
  def main_clock_control():
    clk.next = not clk

  @instance
  def stimuli():
    i2s_data.next = False
    nrst.next = False
    yield delay(30)
    nrst.next = True
    yield delay(70000)
    i2s_data.next = True
    yield delay(10000)
    i2s_data.next = False
    yield delay(10000)
    i2s_data.next = True
    yield delay(10000)
    i2s_data.next = False

  return instances()

def test():
  vcd_path = os.path.join(os.getcwd(), TRACE_LOCATION, tb_top_level_i2s.__name__ + ".vcd")
  if os.path.exists(vcd_path):
    os.remove(vcd_path)
  inst = tb_top_level_i2s()

  inst.config_sim(trace=True, directory=TRACE_LOCATION)
  inst.run_sim(400000)

def convert():
  dout = Signal(intbv(0)[24:])
  clk, nrst, i2s_clk, i2s_frame, i2s_data, rdy = [Signal(False) for _ in range(6)]
  inst = top_level_i2s(clk, nrst, i2s_clk, i2s_data, i2s_frame, dout, rdy)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)

if __name__ == "__main__":
  test()
  convert()
