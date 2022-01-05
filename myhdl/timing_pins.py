from myhdl import *

class TimingPins:
  def __init__(self, clk = Signal(bool(0)), nrst = Signal(bool(0))):
    self.clk = clk
    self.nrst = nrst
