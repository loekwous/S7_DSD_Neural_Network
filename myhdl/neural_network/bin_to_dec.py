from myhdl import *

@block
def selection(en, sel, outp, value = 0):
  @always_comb
  def logic():
    """ MUX implementation """
    if en == True:
      outp.next = True if (value == sel) else False
    else:
      outp.next = False
  return logic


@block
def bin_to_dec(en, bin, dec: list):
  """ Binary to Decimal conversion """
  if 2**len(bin) < len(dec):
    raise ValueError("not all decimal outputs can be driven with binary input")

  sel_insts = []
  for i in range(len(dec)):
    sel_insts.append(selection(en=en, sel=bin, outp=dec[i], value=i))

  return sel_insts

@block
def bin_to_dec_wrapper(en, bin, out0, out1, out2, out3):
  lst = [out0, out1, out2, out3]
  return bin_to_dec(en, bin, lst)

if __name__ == "__main__":
  bin_val = Signal(intbv(0,0,4))
  o0, o1, o2, o3, en = [Signal(False) for _ in range(5)]

  inst = bin_to_dec_wrapper(en=en, bin=bin_val, out0=o0, out1=o1, out2=o2, out3=o3)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)
