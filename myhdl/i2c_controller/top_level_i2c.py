import os
from myhdl import *

from bit_selector import bit_selector
from clock_divider import clock_divider
from combiner import combiner
from controller import controller_i2c
from counter import counter
from mux_3input import mux_3input
from register_data import reg_data
from shift_register import shift_reg_data
from tri_state_controller import tri_state_controller
from controller import controller_i2c
from open_drain_output import open_drain_output

if "TRACE_LOCATION" not in globals():
  TRACE_LOCATION = "traces/"

@block
def get_rw(din, rw_out):
  @always_comb
  def logic():
    rw_out.next = din[0]
  return logic

@block
def data_acquisition(i2c_address, rw_in, regi_address, regi_data, clk, clr, en, sel, d_out, rw_out=None):
  combiner_out = Signal(intbv(0)[8:])
  i2c_addr_reg_out, reg_addr_out, reg_data_out = [Signal(intbv(0)[8:]) for _ in range(3)]

  #inst_rw = get_rw(i2c_addr_reg_out, rw_out)
  inst_combiner = combiner(rw_in, i2c_address, combiner_out)
  inst_i2c_addr_reg = reg_data(clk, clr, en, combiner_out, i2c_addr_reg_out)
  inst_reg_addr_reg = reg_data(clk, clr, en, regi_address, reg_addr_out)
  inst_reg_data_reg = reg_data(clk, clr, en, regi_data, reg_data_out)
  inst_mux = mux_3input(i2c_addr_reg_out, reg_addr_out, reg_data_out, sel, d_out)

  return instances()

@block
def mux_2input(in0, in1, sel, outp):
  @always_comb
  def logic():
    outp.next = in0 if sel == 0 else in1
  return logic

@block
def check_ack(i2c_clk, clr, din, dout):
  @always(i2c_clk.posedge)
  def logic():
    if clr == True:
      dout.next = False
    else:
      if din == False:
        dout.next = True
      else:
        dout.next = False
  return instances()

@block
def success_reg(clk, set, res, success):
  @always(clk.posedge)
  def logic():
    if res == True:
      success.next = False
    else:
      if set == True:
        success.next = True
  return logic

@block
def output_control(fsm_sel, fsm_write, fsm_clk, i2c_clk, current_bit, sh_clr, sh_en, read_data, SCL, SDA, ack, ack_clr):
  read_bit, mux_scl_out, mux_sda_out = [Signal(False) for _ in range(3)]

  inst_chk_ack = check_ack(i2c_clk, ack_clr, read_bit, ack)
  inst_mux_scl = mux_2input(fsm_clk, i2c_clk, fsm_sel, mux_scl_out)
  inst_mux_sda = mux_2input(fsm_write, current_bit, fsm_sel, mux_sda_out)
  inst_tri_state = tri_state_controller(mux_sda_out, read_bit, SDA)
  inst_open_drain = open_drain_output(mux_scl_out, SCL)
  inst_shift_register = shift_reg_data(i2c_clk, sh_clr, sh_en, read_bit, read_data)
  return instances()

@block
def top_level_i2c(start, regi_data, regi_address, rw, address, clk, nrst, ready, success, SDA, SCL, read_data, incoming_frequency=50E6 ,target_frequency = 1E5):
  sel_sig = Signal(intbv(0,0, 3))
  i2c_clk, current_bit, count_en, count_rdy, scl_internal, sh_clr, sh_en, i2c_clk_en = [Signal(False) for _ in range(8)]
  bit_select = Signal(intbv(0,0, 8))
  mux_out = Signal(intbv(0)[8:])
  clr_reg, en_reg = [Signal(False) for _ in range(2)]
  fsm_sel = Signal(False)
  fsm_write = Signal(False)
  fsm_ack = Signal(False)
  fsm_clr_ack = Signal(False)
  success_trigger = Signal(False)

  inst_success = success_reg(clk, success_trigger, en_reg, success)
  inst_data_acquisition = data_acquisition(address, rw, regi_address, regi_data, clk, clr_reg, en_reg, sel_sig, mux_out)
  inst_bit_selector = bit_selector(mux_out, bit_select, current_bit)
  inst_counter = counter(i2c_clk, count_en, count_rdy, bit_select)
  inst_output = output_control(fsm_sel, fsm_write, scl_internal, i2c_clk, current_bit, sh_clr, sh_en, read_data, SCL, SDA, fsm_ack, fsm_clr_ack)
  inst_divider = clock_divider(clk, i2c_clk_en, i2c_clk, incoming_frequency=incoming_frequency ,target_frequency=target_frequency)

  inst_controller = controller_i2c(clk=clk, nrst=nrst, i2c_clk=i2c_clk, i2c_en=i2c_clk_en, start=start, reg_en=en_reg
    , reg_clr=clr_reg, sel_reg=sel_sig, cnt_en=count_en, cnt_rdy=count_rdy, data_ready=ready, data_success=success_trigger
    , tri_write=fsm_write, scl_out=scl_internal, read_shift_clr=sh_clr, read_shift_en=sh_en, sel_drain=fsm_sel, ack=fsm_ack, clr_ack=fsm_clr_ack)

  return instances()


@block
def tb_top_level_i2c():
  start, rw, clk, nrst, ready, success = [Signal(False) for _ in range(6)]
  SDA, SCL = [TristateSignal(False) for _ in range(2)]
  regi_data, regi_address, read_data = [Signal(intbv(0)[8:]) for _ in range(3)]
  address = Signal(intbv(0)[7:])

  inst = top_level_i2c(start, regi_data, regi_address, rw, address, clk, nrst, ready, success, SDA, SCL, read_data, target_frequency=3.125E6)

  driver = SDA.driver()


  @instance
  def stimuli():
    driver.next = None
    print("reset device")
    nrst.next = True
    yield delay(10)
    nrst.next = False
    yield delay(10)
    nrst.next = True

    print("clueless clocking")
    for i in range(200):
      clk.next = True
      yield delay(10)
      clk.next = False
      yield delay(10)
    print("setting data and starting process")
    address.next = 10
    regi_data.next = 20
    regi_address.next = 5
    start.next = True
    yield delay(10)
    for i in range(286):
      clk.next = True
      yield delay(10)
      clk.next = False
      if ready == False and start == True:
        start.next = False
        print("setting start to false, because ready is also false")
      if i == 285:
        driver.next = False
      yield delay(10)

    print("address clocking")
    clock_counter =0

    while True:
      clk.next = True
      yield delay(10)
      clk.next = False

      if clock_counter > 300 and clock_counter < 320:
        driver.next = False
      elif clock_counter > 610 and clock_counter < 630:
        driver.next = False
      elif clock_counter > 800 and clock_counter < 810:
        start.next = True
      elif clock_counter > 810 and clock_counter < 820:
        start.next = False
      elif clock_counter > 8:
        driver.next = None

      if clock_counter > 1500:
        break
      clock_counter += 1

      yield delay(10)
    if __debug__:
      yield StopSimulation()
  return instances()

def convert_tb():
  inst = tb_top_level_i2c()
  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)

def convert():
  start, rw, clk, nrst, ready, success = [Signal(False) for _ in range(6)]
  SDA = TristateSignal(False)
  SCL = TristateSignal(False)
  regi_data, regi_address, read_data = [Signal(intbv(0)[8:]) for _ in range(3)]
  address = Signal(intbv(0)[7:])

  inst = top_level_i2c(start, regi_data, regi_address, rw, address, clk, nrst, ready, success, SDA, SCL, read_data)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)

def test():
  vcd_path = os.path.join(os.getcwd(), TRACE_LOCATION, tb_top_level_i2c.__name__ + ".vcd")
  if os.path.exists(vcd_path):
    #print("Removed old vcd file")
    os.remove(vcd_path)
  inst = tb_top_level_i2c()
  inst.config_sim(trace=True, directory=TRACE_LOCATION)
  inst.run_sim()

if __name__ == "__main__":
  test()
  convert()
  convert_tb()
