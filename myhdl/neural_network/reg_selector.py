from  myhdl import *

if __name__ == '__main__':
  from register_block import register_block
  from bin_to_dec import bin_to_dec
  from demux_block import demux_block
else:
  try:
    from register_block import register_block
    from bin_to_dec import bin_to_dec
    from demux_block import demux_block
  except:
    from .register_block import register_block
    from .bin_to_dec import bin_to_dec
    from .demux_block import demux_block

@block
def reg_selector(sel, funct, en, inp_out, weight_out, bias_out):

  class DemuxOut:
    BIN_DEC_INP = 0
    BIN_DEC_WEIGHT = 1
    BIAS = 2

  demux_out = [Signal(False) for _ in range(3)]
  dmx = demux_block(en=en, sel=funct, outp=demux_out)

  bd_inp = bin_to_dec(en=demux_out[DemuxOut.BIN_DEC_INP], bin=sel, dec=inp_out)
  bd_wei = bin_to_dec(en=demux_out[DemuxOut.BIN_DEC_WEIGHT], bin=sel, dec=weight_out)

  @always_comb
  def bias_logic():
    """ Register selector bias logic """
    if demux_out[DemuxOut.BIAS] == True:
      bias_out.next = True
    else:
      bias_out.next = False

  return instances()

@block
def reg_selector_wrapper(sel, funct, en, i0,i1,i2, w0,w1,w2, bias_out):
  inp = [i0, i1, i2]
  wei = [w0, w1, w2]
  inst = reg_selector(sel=sel, funct=funct, en=en, inp_out=inp, weight_out=wei, bias_out=bias_out)
  return inst


if __name__ == "__main__":

  sel = Signal(intbv(0,0, 4))
  funct = Signal(intbv(0,0,3))
  en, bias_out = [Signal(False) for _ in range(2)]
  i0, i1, i2, w0, w1, w2 = [Signal(False) for _ in range(6)]

  inst = reg_selector_wrapper(sel=sel, funct=funct, en=en, i0=i0,i1=i1,i2=i2, w0=w0,w1=w1,w2=w2, bias_out=bias_out)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)
