from myhdl import *
import sys

if __name__ == '__main__':
    from ram_concurrent import ram_module_conc
else:
    from .ram_concurrent import ram_module_conc


# Real screen constants
class vga_vars:
    TOTAL_SCREEN_X = 640
    TOTAL_SCREEN_Y = 480
    FRONT_PORCH_X = 16
    FRONT_PORCH_Y = 11
    SYNC_PULSE_X = 96
    SYNC_PULSE_Y = 2
    BACK_PORCH_X = 48
    BACK_PORCH_Y = 31


class VgaInputs:
  def __init__(self):
    self.x_pos = Signal(intbv(0, 0, vga_vars.TOTAL_SCREEN_X/8))
    self.y_pos = Signal(intbv(0, 0, vga_vars.TOTAL_SCREEN_Y/8))
    self.pixel = Signal(bool(0))
    self.clk = Signal(bool(0))
    self.we = Signal(bool(0))
    self.nrst = Signal(bool(1))

class VgaOutputs:
  def __init__(self):
    self.vga_r, self.vga_g, self.vga_b = [Signal(intbv(0)[8:]) for _ in range(3)]
    self.vga_clk, self.vga_sync_n, self.vga_blank_n, self.vga_vs, self.vga_hs = [Signal(bool(0)) for _ in range(5)]



@block
def vga_top_level(vga_in, vga_out):
    # Constant screen values
    SCREEN_WIDTH = int(640/8)
    SCREEN_HEIGHT = int(480/8)

    # RAM pointers
    ram_address_write = Signal(
        intbv(val=0, min=0, max=SCREEN_HEIGHT*SCREEN_WIDTH))
    ram_address_read = Signal(
        intbv(val=0, min=0, max=SCREEN_HEIGHT*SCREEN_WIDTH))
    ram_output = Signal(bool(0))

    vga_output = Signal(intbv(0)[3:])

    # Video counters
    MAX_X = int(vga_vars.TOTAL_SCREEN_X+vga_vars.FRONT_PORCH_X +
                vga_vars.SYNC_PULSE_X+vga_vars.BACK_PORCH_X)
    MAX_Y = int(vga_vars.TOTAL_SCREEN_Y+vga_vars.FRONT_PORCH_Y +
                vga_vars.SYNC_PULSE_Y+vga_vars.BACK_PORCH_Y)
    x_counter = Signal(intbv(0, min=0, max=MAX_X + 1))
    y_counter = Signal(intbv(0, min=0, max=MAX_Y + 1))

    # RAM module
    ram = ram_module_conc(din=vga_in.pixel, addrw=ram_address_write, addrr=ram_address_read,
                          we=vga_in.we, clk=vga_in.clk, dout=ram_output, storage_locations=SCREEN_HEIGHT*SCREEN_WIDTH, nrst=vga_in.nrst)

    # VGA clock signal
    clk_25mhz = Signal(bool(0))

    @always_comb
    def control_ram_read():
        """ Translate x and y counter to ram address. The counter value is divided by 8 to ensure a match with the input of 80x60"""
        #ram_address_read.next = (SCREEN_WIDTH * (y_counter / 8) + (x_counter / 8))
        if x_counter < vga_vars.TOTAL_SCREEN_X and y_counter < vga_vars.TOTAL_SCREEN_Y:
            ram_address_read.next = SCREEN_WIDTH * \
                (y_counter >> 3) + (x_counter >> 3)
        else:
            ram_address_read.next = 0

    @always_comb
    def vsync_control():
        """ Control the vertical sync line """
        if y_counter >= (vga_vars.TOTAL_SCREEN_Y + vga_vars.FRONT_PORCH_Y) and y_counter < (vga_vars.TOTAL_SCREEN_Y + vga_vars.FRONT_PORCH_Y + vga_vars.SYNC_PULSE_Y):
            vga_out.vga_vs.next = False
        else:
            vga_out.vga_vs.next = True

    @always_comb
    def video_control():
        """ Control video output """
        if x_counter < vga_vars.TOTAL_SCREEN_X and y_counter < vga_vars.TOTAL_SCREEN_Y:
            # if __debug__:
            #     print(now(), "VGA", "sig vga_output:", bin(vga_output), "ram output:", ram_output)
            if ram_output == True:
                vga_output.next = 7
            else:
                vga_output.next = 0
        else:
            vga_output.next = 0

    @always_comb
    def hsync_control():
        """ Control the horizontal sync line """
        if x_counter >= (vga_vars.TOTAL_SCREEN_X + vga_vars.FRONT_PORCH_X) and x_counter < (vga_vars.TOTAL_SCREEN_X + vga_vars.FRONT_PORCH_X + vga_vars.SYNC_PULSE_X):
            vga_out.vga_hs.next = False
        else:
            vga_out.vga_hs.next = True

    @always_comb
    def color_converter():
        """ Converts 3 bits to 24 color bits """
        if vga_output[2] == True:
            vga_out.vga_r.next = 255
        else:
            vga_out.vga_r.next = 0
        if vga_output[1] == True:
            vga_out.vga_g.next = 255
        else:
            vga_out.vga_g.next = 0
        if vga_output[0] == True:
            vga_out.vga_b.next = 255
        else:
            vga_out.vga_b.next = 0
        # if __debug__:
        #     print(now(), "VGA", "sig vga_output", bin(vga_output), "r", int(vga_out.vga_r), "g", int(vga_out.vga_g), "b", int(vga_out.vga_b))

    @always_comb
    def update_vga_clk():
        """ Generate VGA clock with clock divider (DIV2) and hang blank and sync to VCC """
        vga_out.vga_blank_n.next = True
        vga_out.vga_sync_n.next = True
        vga_out.vga_clk.next = clk_25mhz

    @always(clk_25mhz.posedge, vga_in.nrst.negedge)
    def pos_counter():
        """ The counter increments the x and y counter. These are free running around the through screen """
        if vga_in.nrst == False:
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

    @always(vga_in.clk.posedge)
    def clock_divider():
        """ Clock divider (div2) to get a 25 MHz clock """
        clk_25mhz.next = not clk_25mhz

    @always_comb
    def calc_ram_address():
        """ Convert x position and y position to address """
        if (vga_in.x_pos < SCREEN_WIDTH - 1) and (vga_in.y_pos < SCREEN_HEIGHT - 1):
            ram_address_write.next = vga_in.x_pos + vga_in.y_pos * SCREEN_WIDTH
        else:
            """ Set to zero if x_pos and y_pos are not valid """
            ram_address_write.next = 0

    return calc_ram_address, clock_divider, pos_counter, ram, update_vga_clk, color_converter, control_ram_read, vsync_control, hsync_control, video_control


class test_stats:
  hsync_active = False
  hsync_nonactive = False
  vsync_active = False
  vsync_nonactive = False
  pixel_matches = 0
  pixel_total = 0

@block
def test_vga(period, reset_offset, reset_time, run_time):
    vga_i = VgaInputs()
    vga_o = VgaOutputs()

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

    vga_driver = vga_top_level(vga_i, vga_o)


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

def convert():
    vga_i = VgaInputs()
    vga_o = VgaOutputs()
    vga = vga_top_level(vga_i, vga_o)
    toVHDL.std_logic_ports = True
    toVHDL.directory = "vhdl_out/"
    toVHDL(vga, initial_values=True)
    toVHDL.std_logic_ports = True
    toVHDL.directory = "../vhdl/video_controller/"
    toVHDL(vga, initial_values=True)

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

    # tb = test_vga(period=PERIOD, reset_offset=RESET_OFFSET, reset_time=RESET_TIME, run_time=RUN_TIME)
    # tb.config_sim(trace=True)
    # tb.run_sim(RUN_TIME)
    convert()
