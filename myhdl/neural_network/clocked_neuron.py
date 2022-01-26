from myhdl import *

if __name__ == '__main__':
  from neural_network_info import *
  from neuron import *
  from register_block import register_block
  from reg_selector import reg_selector
  from multiplexer import multiplexer
else:
  try:
    from neural_network_info import *
    from neuron import *
    from register_block import register_block
    from reg_selector import reg_selector
    from multiplexer import multiplexer
  except:
    from .neural_network_info import *
    from .neuron import *
    from .register_block import register_block
    from .reg_selector import reg_selector
    from .multiplexer import multiplexer

# function = 00 input, 01 weight, 10 bias
@block
def neuron_clocked(clk, en, clr, data, outp, sel=None, funct=None, n_inputs=1):
  if n_inputs < 1:
    raise ValueError("number of inputs is not correct")

  if len(funct) != 2:
    raise ValueError("funct should be 2")

  if 2**len(sel) < n_inputs:
    raise ValueError("sel should be able to locate every input")

  class DemuxOut:
    BIN_DEC_INP = 0
    BIN_DEC_WEIGHT = 1
    BIAS = 2

  # selection lines from reg_selector
  inp_reg_sel = [Signal(False) for _ in range(n_inputs)]
  weight_reg_sel = [Signal(False) for _ in range(n_inputs)]
  bias_sel = Signal(False)

  reg_sel = reg_selector(sel=sel, funct=funct, en=en, inp_out=inp_reg_sel, weight_out=weight_reg_sel, bias_out=bias_sel)

  weight_reg_sig = [Signal(intbv(0, data.min, data.max)) for i in range(n_inputs)]
  input_reg_sig = [Signal(intbv(0, data.min, data.max)) for i in range(n_inputs)]
  bias_reg_sig = Signal(intbv(0, data.min, data.max))

  bias_reg = register_block(clk=clk, en=bias_sel, clr=clr, input=data, output=bias_reg_sig)

  weight_regs = []
  for i in range(n_inputs):
    weight_regs.append(register_block(clk=clk, en=weight_reg_sel[i], clr=clr, input=data, output=weight_reg_sig[i]))

  inp_regs = []
  for i in range(n_inputs):
    inp_regs.append(register_block(clk=clk, en=inp_reg_sel[i], clr=clr, input=data, output=input_reg_sig[i]))

  neuron_inst = neuron(output=outp, inputs=input_reg_sig, weights=weight_reg_sig, bias=bias_reg_sig)

  return instances()

@block
def tb_neuron_clocked():
  clk, en, clr = [Signal(False) for _ in range(3)]
  data, outp = [Signal(intbv(0, -(2**31), 2**31-1)) for _ in range(2)]
  n_inputs = 2
  sel = Signal(intbv(0,0, n_inputs))
  funct = Signal(intbv(0)[2:])
  inst = neuron_clocked(clk=clk, en=en, clr=clr, data=data, outp=outp, sel=sel, funct=funct, n_inputs=n_inputs)

  @instance
  def stimuli():
    clr.next = False
    clk.next = False
    sel.next = 0
    funct.next = 0
    data.next = 0
    en.next = False

    #clear device
    yield delay(10)
    clr.next = True
    yield delay(10)
    clk.next = True
    yield delay(10)
    clk.next = False
    clr.next = False


    yield delay(10)
    # set first input to 128
    data.next = 128
    funct.next = 0
    sel.next = 0
    en.next = True
    yield delay(10)
    clk.next = True
    yield delay(10)
    clk.next = False
    #set second input to 128
    data.next = 128
    sel.next = 1
    yield delay(10)
    clk.next = True
    yield delay(10)
    clk.next = False
    #set first weight to -1024
    data.next = -1024
    sel.next = 0
    funct.next = 1
    yield delay(10)
    clk.next = True
    yield delay(10)
    clk.next = False
    #set second weight to 2048
    data.next = 2048
    sel.next = 1
    yield delay(10)
    clk.next = True
    yield delay(10)
    clk.next = False
    yield delay(100)
    if __debug__:
      yield StopSimulation()

  return instances()

def test():
  vcd_path = os.path.join(os.getcwd(), TRACE_LOCATION, tb_neuron_clocked.__name__ + ".vcd")
  if os.path.exists(vcd_path):
    #print("Removed old vcd file")
    os.remove(vcd_path)

  inst = tb_neuron_clocked()

  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)


  inst.config_sim(trace=True, directory=TRACE_LOCATION)
  inst.run_sim()



def convert():
  clk, en, clr = [Signal(False) for _ in range(3)]
  data, outp = [Signal(intbv(0, -(2**31), 2**31-1)) for _ in range(2)]
  n_inputs = 2
  sel = Signal(intbv(0,0, n_inputs))
  funct = Signal(intbv(0)[2:])
  inst = neuron_clocked(clk=clk, en=en, clr=clr, data=data, outp=outp, sel=sel, funct=funct, n_inputs=n_inputs)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)

if __name__ == "__main__":
  test()
  convert()
