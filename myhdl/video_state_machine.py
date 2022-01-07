from myhdl import *

from drawn_memory import DrawnInputs, DrawnOutputs
from timing_pins import TimingPins
from position_validator import Canvas


class ExternalInputs:
    def __init__(self):
        self.triangle, self.sine, self.square = [
            Signal(bool(0)) for _ in range(3)]


class InternalInputs():
    def __init__(self, drawn_outputs: DrawnOutputs = DrawnOutputs()):
        self.drawn_outputs = drawn_outputs
        self.ch_max, self.val_sq, self.val_tri, self.val_sin = [
            Signal(bool(0)) for _ in range(4)]
        self.x_count_top = Signal(bool(0))


class ExternalOutputs:
    def __init__(self):
        self.pixel = Signal(bool(0))
        self.we = Signal(bool(0))


class InternalOutputs:
    def __init__(self, drawn_inputs: DrawnInputs = DrawnInputs()):
        self.drawn_inputs = drawn_inputs
        self.sel_output = Signal(intbv(0, 0, 3))
        self.clr_x = Signal(bool(0))
        self.clr_sin, self.clr_tri, self.clr_sq, self.ch_en = [
            Signal(bool(0)) for _ in range(4)]


@block
def video_state_machine(timing_pins: TimingPins, int_inputs: InternalInputs, ext_inputs: ExternalInputs, int_outputs: InternalOutputs, ext_outputs: ExternalOutputs):
    t_states = enum("SINIT", "IDLE", "SET_SINE", "RES_SINE",
                    "SET_TRIANGLE", "RES_TRIANGLE", "SET_SQUARE", "RES_SQUARE", "NAME")
    t_functs = enum("FNONE", "FSINE", "FTRIANGLE", "FSQUARE")

    func = Signal(t_functs.FNONE)

    p_s = Signal(t_states.SINIT)
    n_s = Signal(t_states.SINIT)

    @always_comb
    def sel_function():
        if func == t_functs.FNONE:
            int_outputs.clr_sin.next = True
            int_outputs.clr_sq.next = True
            int_outputs.clr_tri.next = True
            int_outputs.sel_output.next = 0
            ext_outputs.we.next = False
        elif func == t_functs.FSINE:
            int_outputs.clr_sin.next = False
            int_outputs.clr_sq.next = True
            int_outputs.clr_tri.next = True
            int_outputs.sel_output.next = 0 # SEL = SINE
            ext_outputs.we.next = True
        elif func == t_functs.FTRIANGLE:
            int_outputs.clr_sin.next = True
            int_outputs.clr_sq.next = True
            int_outputs.clr_tri.next = False
            int_outputs.sel_output.next = 1 # SEL = TRIANGLE
            ext_outputs.we.next = True
        else:
            int_outputs.clr_sin.next = True
            int_outputs.clr_sq.next = False
            int_outputs.clr_tri.next = True
            int_outputs.sel_output.next = 2 # SEL = SQUARE
            ext_outputs.we.next = True

    @always_comb
    def input_decoder():
        if p_s == t_states.SINIT:
            n_s.next = t_states.NAME
        elif p_s == t_states.NAME and int_inputs.ch_max == True:
            n_s.next = t_states.IDLE
        elif p_s == t_states.IDLE:
            if ext_inputs.sine == True and int_inputs.drawn_outputs.sin_o == False:
                n_s.next = t_states.SET_SINE
            elif ext_inputs.sine == False and int_inputs.drawn_outputs.sin_o == True:
                n_s.next = t_states.RES_SINE
            elif ext_inputs.square == True and int_inputs.drawn_outputs.sq_o == False:
                n_s.next = t_states.SET_SQUARE
            elif ext_inputs.square == False and int_inputs.drawn_outputs.sq_o == True:
                n_s.next = t_states.RES_SQUARE
            elif ext_inputs.triangle == True and int_inputs.drawn_outputs.tri_o == False:
                n_s.next = t_states.SET_TRIANGLE
            elif ext_inputs.triangle == False and int_inputs.drawn_outputs.tri_o == True:
                n_s.next = t_states.RES_TRIANGLE
            else:
                n_s.next = t_states.IDLE
        elif (p_s == t_states.SET_SINE or p_s == t_states.RES_SINE or p_s == t_states.SET_SQUARE or p_s == t_states.RES_SQUARE or p_s == t_states.SET_TRIANGLE or p_s == t_states.RES_TRIANGLE) and int_inputs.x_count_top == True:
            n_s.next = t_states.IDLE
        else:
            n_s.next = p_s

    @always(timing_pins.clk.posedge, timing_pins.nrst.negedge)
    def mem():
        if timing_pins.nrst == False:
            p_s.next = t_states.SINIT
        else:
            p_s.next = n_s

    @always_comb
    def output_decoder_char():
        if p_s == t_states.NAME:
            int_outputs.ch_en.next = True
        else:
            int_outputs.ch_en.next = False

    @always_comb
    def output_decoder_pixel():
      if (p_s == t_states.SET_SINE and int_inputs.val_sin == True) or (p_s == t_states.SET_SQUARE and int_inputs.val_sq == True) or (p_s == t_states.SET_TRIANGLE and int_inputs.val_tri == True):
        ext_outputs.pixel.next = True
      else:
        ext_outputs.pixel.next = False

    @always_comb
    def output_decoder_func():
        if (p_s == t_states.SET_SINE or p_s == t_states.RES_SINE):
            int_outputs.clr_x.next = False
            if int_inputs.val_sin == True:
                func.next = t_functs.FSINE
            else:
                func.next = t_functs.FNONE
        elif (p_s == t_states.SET_SQUARE or p_s == t_states.RES_SQUARE):
            int_outputs.clr_x.next = False
            if int_inputs.val_sq == True:
                func.next = t_functs.FSQUARE
            else:
                func.next = t_functs.FNONE
        elif (p_s == t_states.SET_TRIANGLE or p_s == t_states.RES_TRIANGLE):
            int_outputs.clr_x.next = False
            if int_inputs.val_tri == True:
                func.next = t_functs.FTRIANGLE
            else:
                func.next = t_functs.FNONE
        else:
            int_outputs.clr_x.next = True
            func.next = t_functs.FNONE

    @always_comb
    def output_decoder_mem():
        if p_s == t_states.SINIT:
            int_outputs.drawn_inputs.clr.next = True
            int_outputs.drawn_inputs.sin_t.next = False
            int_outputs.drawn_inputs.sq_t.next = False
            int_outputs.drawn_inputs.tri_t.next = False
        elif p_s == t_states.IDLE:
            int_outputs.drawn_inputs.clr.next = False

            if int_inputs.drawn_outputs.sin_o != ext_inputs.sine:
                int_outputs.drawn_inputs.sin_t.next = True
            else:
                int_outputs.drawn_inputs.sin_t.next = False

            if int_inputs.drawn_outputs.sq_o != ext_inputs.square:
                int_outputs.drawn_inputs.sq_t.next = True
            else:
                int_outputs.drawn_inputs.sq_t.next = False

            if int_inputs.drawn_outputs.tri_o != ext_inputs.triangle:
                int_outputs.drawn_inputs.tri_t.next = True
            else:
                int_outputs.drawn_inputs.tri_t.next = False
        else:
            int_outputs.drawn_inputs.clr.next = False
            int_outputs.drawn_inputs.sin_t.next = False
            int_outputs.drawn_inputs.sq_t.next = False
            int_outputs.drawn_inputs.tri_t.next = False
    return instances()

def Main():
    timing_pins = TimingPins()
    int_inputs = InternalInputs()
    ext_inputs = ExternalInputs()
    int_outputs = InternalOutputs()
    ext_outputs = ExternalOutputs()

    sm = video_state_machine(timing_pins=timing_pins, int_inputs=int_inputs,
                             ext_inputs=ext_inputs, int_outputs=int_outputs, ext_outputs=ext_outputs)
    toVHDL.std_logic_ports = True
    toVHDL.directory = "vhdl_out/"
    toVHDL(sm, initial_value=True)
    toVHDL.std_logic_ports = True
    toVHDL.directory = "../vhdl/video_controller/"
    toVHDL(sm, initial_value=True)

if __name__ == "__main__":
    Main()
