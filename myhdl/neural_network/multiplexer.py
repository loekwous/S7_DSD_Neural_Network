import os
from myhdl import *

if "TRACE_LOCATION" not in globals():
  TRACE_LOCATION = "traces/"

# @block
# def selector(sel, inp, outp, value=0):

#   @always_comb
#   def logic():
#     if sel == value:
#       outp.next = inp
#     else:
#       outp.next = 0
#   return logic

# @block
# def or_gate(a, b , c):
#   if len(a) != len(b) and len(b) != len(c):
#     raise ValueError("length of all ports should be the same")
#   @always_comb
#   def logic():
#     for i in range:
#       c.next[i] = a[i] or b[i]
#   return logic



# @block
# def single_multiplexer(in0, in1, sel, output):
#   @always_comb
#   def logic():
#     output.next = in1 if sel == True else in0
#   return logic

# @block
# def selector(sel, outputs):
#   if 2**len(sel) < len(outputs):
#     raise ValueError("Sel should be able to locate every output")

#   mem = tuple([2**i for i in range(0, len(outputs))])

#   @always_comb
#   def logic():
#     """ Input logic selector MUX """
#     if sel > 1:
#       index = (sel - 1)
#       outputs.next = mem[index]
#     else:
#       outputs.next = sel

#   return instances()

# @block
# def multiplexer(inputs, sel, output):
#   if 2**len(sel) < len(inputs):
#     raise ValueError("the sel input should be able to reach all the inputs")

#   n_inputs = len(inputs)
#   n_multiplexers = n_inputs - 1
#   n_signals = n_multiplexers - 1

#   selector_outputs = Signal(intbv(0)[n_multiplexers:])
#   selector_inst = selector(sel=sel, outputs=n_multiplexers)

#   sigs = [Signal(intbv(0, inputs[0].min, inputs[0].max)) for _ in range(n_inputs)]

#   multiplexers = []
#   if n_inputs == 2:
#     multiplexers.append(single_multiplexer(inputs[0], inputs[1], sel, output))
#   else:
#     multiplexers.append(single_multiplexer(inputs[0], inputs[1], selector_outputs[0], sigs[0]))
#     for i in range(n_multiplexers - 2):
#       multiplexers.append(single_multiplexer(inputs[i+2], sigs[i], selector_outputs[i+1], sigs[i+1]))
#     multiplexers.append(single_multiplexer(inputs[n_inputs - 1], sigs[n_signals-1], selector_outputs[n_multiplexers-1], output))
#   return instances()

# @block
# def multiplexer_wrapper(in0, in1, in2, in3, sel, output):
#   inputs = [in0, in1, in2, in3]
#   inst = multiplexer(inputs, sel, output)
#   return inst


# @block
# def tb_selector():
#   outp = Signal(intbv(0)[7:])
#   sel = Signal(intbv(0,0,len(outp) + 1))

#   inst = selector(sel, outp)

#   iterations = sel.max

#   @instance
#   def stimuli():
#     for i in range(iterations):
#       sel.next = i
#       yield delay(10)
#       if sel < 2 and outp != sel:
#         print("outp is not equal to sel below 2")
#       elif sel >= 2 and outp != 2**(sel-1):
#         print("outp is not equal to 2 times sel above or equal to 2")
#     yield StopSimulation()
#   return instances()

# def convert():
#   in0, in1, in2, in3, output = [Signal(intbv(0, -1024, 1023)) for _ in range(5)]
#   sel = Signal(intbv(0,0,4))

#   inst = multiplexer_wrapper(in0, in1, in2, in3, sel, output)

#   toVHDL.std_logic_ports = True
#   toVHDL.directory = "vhdl_out/"
#   toVHDL(inst, initial_value=True)

# def test_selector():
#   vcd_path = os.path.join(os.getcwd(), TRACE_LOCATION, tb_selector.__name__ + ".vcd")
#   if os.path.exists(vcd_path):
#     print("Removed old vcd file")
#     os.remove(vcd_path)

#   tb = tb_selector()
#   tb.config_sim(trace=True, directory=TRACE_LOCATION)
#   tb.run_sim()

@block
def multiplexer(inputs, sel, outp):
  for i in range(len(inputs)):
    if len(inputs[i]) != len(outp):
      raise ValueError("Length should be equal")

  sigs = [Signal(intbv(0, inputs[i].min, inputs[i].max)) for i in range(len(inputs))]

  n_inputs = len(inputs)

  @always_comb
  def input_forwarding():
    for i in range(n_inputs):
      # if __debug__:
      #   print("updating %d to %d" % (i, inputs[i]))
      sigs[i].next = inputs[i]

  @always_comb
  def output_logic():
    outp.next = sigs[sel]
    # if __debug__:
    #   print("sigs[sel]= %d" % sigs[sel])
  return input_forwarding, output_logic

@block
def multiplexer_wrapper(in0, in1, in2, in3, sel, output):
  sigs = [in0, in1, in2, in3]
  inst = multiplexer(sigs, sel, output)
  return inst


@block
def tb_multiplexer():

  vcd_path = os.path.join(os.getcwd(), TRACE_LOCATION, tb_multiplexer.__name__ + ".vcd")
  if os.path.exists(vcd_path):
    print("Removed old vcd file")
    os.remove(vcd_path)

  in0, in1, in2, in3, output = [Signal(intbv(0,0,1024)) for _ in range(5)]
  sel = Signal(intbv(0,0,4))

  inst = multiplexer_wrapper(in0, in1, in2, in3, sel, output)

  iterations = sel.max

  @instance
  def stimuli():
    yield delay(10)
    sel.next = 0
    in0.next = 1
    in1.next = 2
    in2.next = 3
    in3.next = 4
    yield delay(20)
    for i in range(iterations):
      sel.next = i
      yield delay(10)
    sel.next = 0
    yield delay(10)
    yield StopSimulation()
  
  return instances()

if __name__ == "__main__":

  inst = tb_multiplexer()
  inst.config_sim(trace=True, directory=TRACE_LOCATION)
  inst.run_sim()

  in0, in1, in2, in3, output = [Signal(intbv(0,0,1024)) for _ in range(5)]
  sel = Signal(intbv(0,0,4))

  inst = multiplexer_wrapper(in0, in1, in2, in3, sel, output)

  # test_selector()

  # outp = Signal(intbv(0)[8:])
  # sel = Signal(intbv(0,0,len(outp)))

  # inst = selector(sel, outp)

  # toVHDL.std_logic_ports = True
  # toVHDL.directory = "vhdl_out/"
  # toVHDL(inst, initial_value=True)


  # convert()
