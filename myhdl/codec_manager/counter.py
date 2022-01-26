from myhdl import *

@block
def counter(clk, clear, count_up, count_out, top, max_val=3):
  count_sig = Signal(intbv(0,0, max_val+1))

  @always_comb
  def top_logic():
    if count_sig == max_val:
      top.next = True
    else:
      top.next = False

  @always_comb
  def output_logic():
    count_out.next = count_sig

  @always(clk.posedge)
  def count_logic():
    if clear == True:
      count_sig.next = 0
    else:
      if count_up == True and count_sig < max_val:
        count_sig.next = count_sig.next + 1

  return instances()

def convert():
  clk, clear, count_up, top = [Signal(False) for _ in range(4)]
  count_out = Signal(intbv(0, 0,4))
  inst = counter(clk, clear, count_up, count_out, top, max_val=count_out.max-1)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)

if __name__ == "__main__":
  convert()
