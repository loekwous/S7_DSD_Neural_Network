from myhdl import *

@block
def rom_content(sel, i2c_address, rw, reg_address, data):

  i2c_address_hard = 0x34 >> 1
  rw_HARD = False

  left_volume_address = 0 << 1
  right_volume_address = 1 << 1
  power_down_address = 6 << 1
  active_control_address = 9 << 1

  left_volume = 0x17
  right_volume = 0x17
  power_down = 0x0A
  active_control = 1
  reg_addresses = (left_volume_address, right_volume_address, power_down_address, active_control_address)
  reg_data = (left_volume, right_volume, power_down, active_control)

  @always_comb
  def logic():
    rw.next = rw_HARD
    i2c_address.next = i2c_address_hard
    reg_address.next = reg_addresses[sel]
    data.next = reg_data[sel]

  return instances()

def convert():
  sel = Signal(intbv(0, 0, 5))
  i2c_address = Signal(intbv(0)[7:])
  reg_address, data = [Signal(intbv(0)[8:]) for _ in range(2)]
  rw = Signal(False)
  inst = rom_content(sel, i2c_address, rw, reg_address, data)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)

if __name__ == "__main__":
  convert()
