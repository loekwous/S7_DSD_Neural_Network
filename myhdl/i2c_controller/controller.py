import os
from myhdl import *

if "TRACE_LOCATION" not in globals():
  TRACE_LOCATION = "traces/"

@block
def controller_i2c(clk, nrst, i2c_clk, i2c_en, start, reg_en, reg_clr, sel_reg, cnt_en, cnt_rdy, data_ready, data_success, tri_write, scl_out, read_shift_clr, read_shift_en, sel_drain, ack, clr_ack):

  t_states = enum("IDLE", "WF_START", "START1", "START2", "SEND_ADDR", "CHECK_ACK_S0", "CHECK_ACK_S1", "CHECK_ACK_S2"
  , "SEND_DATA_ADDRESS", "CHECK_ACK_S3", "CHECK_ACK_S4", "CHECK_ACK_S5", "SEND_DATA", "CHECK_ACK_S6", "CHECK_ACK_S7", "CHECK_ACK_S8"
  , "STOP_S0", "STOP_S1")

  p_s, n_s = [Signal(t_states.IDLE) for _ in range(2)]


  @always_comb
  def input_decoder():
    if (p_s == t_states.IDLE) and start == True:
      n_s.next = t_states.WF_START

    elif p_s == t_states.WF_START and start == False:
      n_s.next = t_states.START1

    elif p_s == t_states.START1 and i2c_clk == True:
      n_s.next = t_states.START2

    elif p_s == t_states.START2 and i2c_clk == False:
      n_s.next = t_states.SEND_ADDR

    elif p_s == t_states.SEND_ADDR and not i2c_clk and cnt_rdy:
      n_s.next = t_states.CHECK_ACK_S0

    elif p_s == t_states.CHECK_ACK_S0 and i2c_clk and cnt_rdy:
      n_s.next = t_states.CHECK_ACK_S1

    elif p_s == t_states.CHECK_ACK_S1 and not i2c_clk:
      if ack == True:
        n_s.next = t_states.CHECK_ACK_S2
      else:
        n_s.next = t_states.IDLE

    elif p_s == t_states.CHECK_ACK_S2 and i2c_clk:
      n_s.next = t_states.SEND_DATA_ADDRESS

    elif p_s == t_states.SEND_DATA_ADDRESS and not i2c_clk and cnt_rdy:
      n_s.next = t_states.CHECK_ACK_S3

    elif p_s == t_states.CHECK_ACK_S3 and i2c_clk and cnt_rdy:
      n_s.next = t_states.CHECK_ACK_S4

    elif p_s == t_states.CHECK_ACK_S4 and not i2c_clk:
      if ack == True:
        n_s.next = t_states.CHECK_ACK_S5
      else:
        n_s.next = t_states.IDLE

    elif p_s == t_states.CHECK_ACK_S5 and i2c_clk:
      n_s.next = t_states.SEND_DATA

    elif p_s == t_states.SEND_DATA and not i2c_clk and cnt_rdy:
      n_s.next = t_states.CHECK_ACK_S6

    elif p_s == t_states.CHECK_ACK_S6 and i2c_clk and cnt_rdy:
      n_s.next = t_states.CHECK_ACK_S7

    elif p_s == t_states.CHECK_ACK_S7 and not i2c_clk:
      if ack == True:
        n_s.next = t_states.CHECK_ACK_S8
      else:
        n_s.next = t_states.IDLE

    elif p_s == t_states.CHECK_ACK_S8 and i2c_clk:
      n_s.next = t_states.STOP_S0

    elif p_s == t_states.STOP_S0 and not i2c_clk:
      n_s.next = t_states.STOP_S1

    elif p_s == t_states.STOP_S1 and i2c_clk:
      n_s.next = t_states.IDLE

    # IDLE state
    else:
      n_s.next = p_s

  @always(clk.posedge, nrst.negedge)
  def memory():
    if nrst == False:
      p_s.next = t_states.IDLE
    else:
      p_s.next = n_s


  @always_comb
  def ready_control():
    cond_ack_0 = p_s != t_states.CHECK_ACK_S0 and p_s != t_states.CHECK_ACK_S1 and p_s != t_states.CHECK_ACK_S2
    cond_ack_1 = p_s != t_states.CHECK_ACK_S3 and p_s != t_states.CHECK_ACK_S4 and p_s != t_states.CHECK_ACK_S5
    cond_ack_2 = p_s != t_states.CHECK_ACK_S6 and p_s != t_states.CHECK_ACK_S7 and p_s != t_states.CHECK_ACK_S8
    clr_ack.next = True if cond_ack_0 and cond_ack_1 and cond_ack_2 else False
    if p_s == t_states.IDLE:
      data_ready.next = True
    else:
      data_ready.next = False

  @always_comb
  def clear_control():
    if p_s == t_states.IDLE:
      reg_clr.next = True
      read_shift_clr.next = True
    else:
      reg_clr.next = False
      read_shift_clr.next = False

  @always_comb
  def count_control():
    if p_s == t_states.IDLE:
      cnt_en.next = False
    elif p_s == t_states.SEND_ADDR or p_s == t_states.SEND_DATA_ADDRESS or p_s == t_states.SEND_DATA:
      cnt_en.next = True
    else:
      cnt_en.next = False

  @always_comb
  def reg_en_control():
    if p_s == t_states.WF_START:
      reg_en.next = True
    else:
      reg_en.next = False

  @always_comb
  def i2c_control():
    if p_s == t_states.IDLE:
      tri_write.next = True
      scl_out.next = True
      sel_drain.next = False
    elif p_s == t_states.START1:
      tri_write.next = False
      scl_out.next = True
      sel_drain.next = False
    elif p_s == t_states.START2:
      tri_write.next = False
      scl_out.next = True
      sel_drain.next = False
    elif p_s == t_states.SEND_ADDR:
      tri_write.next = True
      scl_out.next = True
      sel_drain.next = True
    elif p_s == t_states.CHECK_ACK_S0:
      tri_write.next = True
      scl_out.next = False
      sel_drain.next = False
    elif p_s == t_states.CHECK_ACK_S1:
      tri_write.next = True
      scl_out.next = True
      sel_drain.next = False
    elif p_s == t_states.CHECK_ACK_S2:
      tri_write.next = False
      scl_out.next = False
      sel_drain.next = False
    elif p_s == t_states.SEND_DATA_ADDRESS:
      tri_write.next = True
      scl_out.next = True
      sel_drain.next = True
    elif p_s == t_states.CHECK_ACK_S3:
      tri_write.next = True
      scl_out.next = False
      sel_drain.next = False
    elif p_s == t_states.CHECK_ACK_S4:
      tri_write.next = True
      scl_out.next = True
      sel_drain.next = False
    elif p_s == t_states.CHECK_ACK_S5:
      tri_write.next = False
      scl_out.next = False
      sel_drain.next = False
    elif p_s == t_states.SEND_DATA:
      tri_write.next = True
      scl_out.next = True
      sel_drain.next = True
    elif p_s == t_states.CHECK_ACK_S6:
      tri_write.next = True
      scl_out.next = False
      sel_drain.next = False
    elif p_s == t_states.CHECK_ACK_S7:
      tri_write.next = True
      scl_out.next = True
      sel_drain.next = False
    elif p_s == t_states.CHECK_ACK_S8:
      tri_write.next = True
      scl_out.next = False
      sel_drain.next = False
    elif p_s == t_states.STOP_S0:
      tri_write.next = False
      scl_out.next = False
      sel_drain.next = False
    elif p_s == t_states.STOP_S1:
      tri_write.next = False
      scl_out.next = True
      sel_drain.next = False
    else:
      tri_write.next = True
      scl_out.next = True
      sel_drain.next = False

  @always_comb
  def output_decoder():
    if p_s == t_states.START1:
      sel_reg.next = 0
      data_success.next = False
      read_shift_en.next = False
      i2c_en.next = True
    elif p_s == t_states.START2:
      sel_reg.next = 0
      data_success.next = False
      read_shift_en.next = False
      i2c_en.next = True
    elif p_s == t_states.SEND_DATA_ADDRESS:
      sel_reg.next = 1
      data_success.next = False
      read_shift_en.next = False
      i2c_en.next = True
    elif p_s == t_states.SEND_DATA:
      sel_reg.next = 2
      data_success.next = False
      read_shift_en.next = False
      i2c_en.next = True
    elif p_s == t_states.CHECK_ACK_S8:
      sel_reg.next = 2
      data_success.next = True
      read_shift_en.next = False
      i2c_en.next = True
    else: # IDLE and others
      sel_reg.next = 0
      data_success.next = False
      read_shift_en.next = False
      i2c_en.next = True

  return instances()


@block
def tb_controller():
  clk, nrst, i2c_clk, i2c_clk_en, start, en_reg, clr_reg, current_bit, count_en, count_rdy, ready, success, tri_r, tri_w, scl_internal, sh_clr, sh_en, sh_in, tri_rw = [Signal(False) for _ in range(19)]
  sel_sig = Signal(intbv(0,0, 3))

  inst_controller = controller_i2c(clk, nrst, i2c_clk, i2c_clk_en, start, en_reg, clr_reg, sel_sig, current_bit, count_en, count_rdy, ready, success, tri_rw, tri_r, tri_w, scl_internal, sh_clr, sh_en, sh_in)

  @instance
  def stimuli():
    nrst.next = True
    yield delay(10)
    nrst.next = False
    yield delay(10)
    nrst.next = True
    yield delay(10)
    for i in range(50):
      clk.next = True
      yield delay(10)
      clk.next = False
      yield delay(10)
    start.next = True
    for i in range(50):
      clk.next = True
      yield delay(10)
      clk.next = False
      yield delay(10)
    yield StopSimulation()
  return instances()

def test():
  vcd_path = os.path.join(os.getcwd(), TRACE_LOCATION, tb_controller.__name__ + ".vcd")
  if os.path.exists(vcd_path):
    os.remove(vcd_path)
  inst = tb_controller()
  inst.config_sim(trace=True, directory=TRACE_LOCATION)
  inst.run_sim()

if __name__ == "__main__":
  test()
