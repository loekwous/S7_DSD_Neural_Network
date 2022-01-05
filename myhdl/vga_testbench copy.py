from myhdl import *

import vga
from vga import *

class test_stats:
  hsync_active = False
  hsync_nonactive = False
  vsync_active = False
  vsync_nonactive = False
  pixel_matches = 0
  pixel_total = 0

@block
def test_vga(period, reset_offset, reset_time, run_time):
    vga_i = vga.VgaInputs()
    vga_o = vga.VgaOutputs()

    # stimulus signals
    divided_clk = Signal(bool(0))
    nrst_is_passed = Signal(bool(0))

    last_pixel = Signal(bool(0))

    # Video counters
    MAX_X = int(vga_vars.TOTAL_SCREEN_X+vga_vars.FRONT_PORCH_X +
                vga_vars.SYNC_PULSE_X+vga_vars.BACK_PORCH_X)
    MAX_Y = int(vga_vars.TOTAL_SCREEN_Y+vga_vars.FRONT_PORCH_Y +
                vga_vars.SYNC_PULSE_Y+vga_vars.BACK_PORCH_Y)
    x_counter = Signal(intbv(0, min=0, max=MAX_X + 1))
    y_counter = Signal(intbv(0, min=0, max=MAX_Y + 1))

    vga_driver = vga.vga_top_level(vga_i, vga_o)


    @instance
    def print_results():
        yield delay(run_time)
        print("<=== Results ===>")
        print("HSYNC active   :", test_stats.hsync_active)
        print("HSYNC nonactive:", test_stats.hsync_nonactive)
        print("VSYNC active   :", test_stats.vsync_active)
        print("VSYNC nonactive:", test_stats.vsync_nonactive)
        print("pixel counter:  ", test_stats.pixel_total)
        print("returned pixels ", test_stats.pixel_matches)

    @always(divided_clk.negedge)
    def update_pixel():
        last_pixel.next = not last_pixel

    @instance
    def video_stimuli():
        yield delay(reset_offset + reset_time)
        for i in range(1,vga_vars.TOTAL_SCREEN_X//8):
            test_stats.pixel_total += 1
            vga_i.pixel.next = bool((i - 1)%2)
            vga_i.we.next = True
            vga_i.x_pos.next = i
            vga_i.y_pos.next = 0
            yield delay(period)
            vga_i.we.next = False
            #print(now(), "TB", "iteration:", i, "=", "r", int(vga_o.vga_r), "g", int(vga_o.vga_g), "b", int(vga_o.vga_b), "i%2 =", i%2)
            test_stats.pixel_matches += int((bool(vga_o.vga_r) and bool(vga_o.vga_g) and bool(vga_o.vga_b)) ==  bool(i%2))
            yield delay(2 * 8 * period - period)



    @always(divided_clk.negedge)
    def check_hs():
        if (x_counter >= (vga_vars.TOTAL_SCREEN_X + vga_vars.FRONT_PORCH_X)) and (x_counter < (vga_vars.TOTAL_SCREEN_X + vga_vars.FRONT_PORCH_X + vga_vars.SYNC_PULSE_X )):
            if vga_o.vga_hs == True:
                test_stats.hsync_active = False
            else:
                test_stats.hsync_active = True
        else:
            if vga_o.vga_hs == False:
                test_stats.hsync_nonactive = False
            else:
                test_stats.hsync_nonactive = True

    @always(divided_clk.negedge)
    def check_vs():
        if (y_counter >= (vga_vars.TOTAL_SCREEN_Y + vga_vars.FRONT_PORCH_Y)) and (y_counter < (vga_vars.TOTAL_SCREEN_Y + vga_vars.FRONT_PORCH_Y + vga_vars.SYNC_PULSE_Y )):
            if vga_o.vga_vs == True:
                test_stats.vsync_active = False
            else:
                test_stats.vsync_active = True
        else:
            if vga_o.vga_vs == False:
                test_stats.vsync_nonactive = False
            else:
                test_stats.vsync_nonactive = True

    @always(divided_clk.posedge, vga_i.nrst)
    def pos_counter():
        """ The counter increments the x and y counter. These are free running around the through screen """
        if vga_i.nrst == False:
            x_counter.next = 0
            y_counter.next = 0
        else:
            if x_counter < intbv(MAX_X - 1):
                x_counter.next = x_counter + 1
            else:
                x_counter.next = 0
                if y_counter < intbv(MAX_Y - 1):
                    y_counter.next = y_counter + 1
                else:
                    y_counter.next = 0


    @instance
    def update_reset():
        yield delay(reset_offset)
        vga_i.nrst.next = False
        vga_i.we.next = True
        print(now(), "nrst = 0")
        yield delay(reset_time)
        vga_i.nrst.next = True
        print(now(), "nrst = 1")
        nrst_is_passed.next = True

    @instance
    def update_clock():
        while True:
            yield delay(period//2)
            vga_i.clk.next = not vga_i.clk


    @always(vga_i.clk.posedge)
    def update_slow_clock():
        divided_clk.next = not divided_clk

    return instances()

if __name__ == "__main__":

    PERIOD = int(20)
    RESET_OFFSET = 2*PERIOD + PERIOD//4
    RESET_TIME = 1*PERIOD

    X_TIME = (vga_vars.TOTAL_SCREEN_X + vga_vars.FRONT_PORCH_X + vga_vars.SYNC_PULSE_X + vga_vars.BACK_PORCH_X) * 2 * PERIOD
    Y_FRACTION = (vga_vars.TOTAL_SCREEN_Y + vga_vars.FRONT_PORCH_Y + vga_vars.SYNC_PULSE_Y + vga_vars.BACK_PORCH_Y)

    #RUN_TIME = RESET_OFFSET + RESET_TIME + X_TIME * Y_FRACTION
    RUN_TIME = RESET_OFFSET + RESET_TIME + X_TIME * 10
    #RUN_TIME = 5000

    print("<=== VGA testbench info ===>")
    print("period time:    ", PERIOD, "ns")
    print("horizontal time:", X_TIME, "ns")
    print("reset offset:   ", RESET_OFFSET, "ns")
    print("reset time:     ", RESET_TIME, "ns")
    print("total time:     ", RUN_TIME, "ns")
    print("<===--------------------===>")

    tb = test_vga(period=PERIOD, reset_offset=RESET_OFFSET, reset_time=RESET_TIME, run_time=RUN_TIME)
    tb.config_sim(trace=True)
    tb.run_sim(RUN_TIME)
