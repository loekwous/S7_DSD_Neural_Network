from myhdl import *

import position_validator


@block
def gen_offset(sin_in, tri_in, sq_in, sin_o, tri_o, sq_o):
    @always_comb
    def update_output():
        sin_o.next = position_validator.Canvas.height - \
            1 - sin_in - (position_validator.Sine.top)
        tri_o.next = position_validator.Canvas.height - \
            1 - tri_in - (position_validator.Triangle.top)
        sq_o.next = position_validator.Canvas.height - \
            1 - sq_in - (position_validator.Square.top)

    return update_output


def Main():
    sin_in, tri_in, sq_in, sin_o, tri_o, sq_o = [
        Signal(intbv(0, 0, position_validator.Canvas.height)) for _ in range(6)]
    inst = gen_offset(sin_in, tri_in, sq_in, sin_o, tri_o, sq_o)
    toVHDL.std_logic_ports = True
    toVHDL.directory = "../vhdl/video_controller"
    toVHDL(inst, initial_value=True)
    toVHDL.std_logic_ports = True
    toVHDL.directory = "vhdl_out/"
    toVHDL(inst, initial_value=True)


if __name__ == "__main__":
    Main()
