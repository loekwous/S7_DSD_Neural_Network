from myhdl import *

@block
def selection(inp, sel, outp, value = 0):
  """ Selector to check if this output should be enabled within the DEMUX """
  @always_comb
  def logic():
    if value == sel:
      outp.next = inp
    else:
      outp.next = False
  return logic

@block
def demux_block(en, sel, outp: list):
  """ DEMUX implementation """
  if 2**len(sel) < len(outp):
    raise ValueError("not all outputs can be driven with sel input")

  sel_insts = []
  for i in range(len(outp)):
    sel_insts.append(selection(inp=en, sel=sel, outp=outp[i], value=i))

  return sel_insts

@block
def demux_wrapper(en, sel, out0, out1, out2, out3):
  lst = [out0, out1, out2, out3]
  return demux_block(en=en, sel=sel, outp=lst)


if __name__ == "__main__":
  sel = Signal(intbv(0,0,4))
  o0, o1, o2, o3, en = [Signal(False) for _ in range(5)]

  inst = demux_wrapper(en=en, sel=sel, out0=o0, out1=o1, out2=o2, out3=o3)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)
