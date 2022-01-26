from myhdl import *

@block
def codec_controller(clk, nrst, start, ready, i2c_start, i2c_ready, i2c_success, cnt_clr, cnt_up, cnt_top):

  t_states = enum("IDLE", "WF_START", "START_SENDING"
    , "WAIT_FOR_TRANS", "COUNT_UP")

  p_s, n_s = Signal(t_states.IDLE), Signal(t_states.IDLE)

  @always_comb
  def input_decoder():
    if p_s == t_states.IDLE and start == True:
      n_s.next = t_states.WF_START
    elif p_s == t_states.WF_START and start == False:
      n_s.next = t_states.START_SENDING
    elif p_s == t_states.START_SENDING and i2c_ready == False:
      n_s.next = t_states.WAIT_FOR_TRANS
    elif p_s == t_states.WAIT_FOR_TRANS:
      if i2c_ready == True:
        if i2c_success == True:
          if cnt_top == True:
            n_s.next = t_states.IDLE
          else:
            n_s.next = t_states.COUNT_UP
        else:
          n_s.next = t_states.IDLE
      else:
        n_s.next = t_states.WAIT_FOR_TRANS
    elif p_s == t_states.COUNT_UP:
      n_s.next = t_states.START_SENDING
    else:
      n_s.next = p_s

  @always(clk.posedge, nrst.negedge)
  def memory():
    if nrst == False:
      p_s.next = t_states.IDLE
    else:
      p_s.next = n_s

  @always_comb
  def start_control():
    i2c_start.next = True if p_s == t_states.START_SENDING else False

  @always_comb
  def clear_control():
    clear_condition = p_s == t_states.IDLE or p_s == t_states.WF_START
    cnt_clr.next = True if clear_condition else False

  @always_comb
  def count_control():
    cnt_up.next = True if p_s == t_states.COUNT_UP else False

  @always_comb
  def ready_control():
    ready.next = True if p_s == t_states.IDLE else False
  
  return instances()

def convert():
  clk, nrst, start, ready, i2c_start, i2c_ready, i2c_success, cnt_clr, cnt_up, cnt_top = [Signal(False) for _ in range(10)]
  inst = codec_controller(clk, nrst, start, ready, i2c_start, i2c_ready, i2c_success, cnt_clr, cnt_up, cnt_top)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)

if __name__ == "__main__":
  convert()
