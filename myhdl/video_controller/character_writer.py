import os
from myhdl import *
import sys

if "TRACE_LOCATION" not in globals():
  TRACE_LOCATION = "traces/"

if __name__ == '__main__':
  from character_set import *
  from position_validator import Canvas
else:
  from  .character_set import *
  from .position_validator import Canvas


def number_to_bit_array(number):
  output_list = []
  temp_number = number
  bit_list = [2**(7-i) for i in range(7)]
  for i in range(len(bit_list)):
    if temp_number >= bit_list[i]:
      temp_number -= bit_list[i]
      output_list.append(True)
    else:
      output_list.append(False)
  return output_list

def bit_array_to_number(bit_array):
  output_number = 0
  bit_list = [2**(7-i) for i in range(8)]
  for i in range(len(bit_array)):
    output_number += bit_list[i] * int(bit_array[i])
  return output_number

def translate(lst):
  # create one bit list from x-min to x-max
  output_list = []
  output_bit_list = []
  converted_bit_list = []
  rotated_bit_list = []
  # convert to bit list
  for char in lst:
    temp_converted_bit_list = []
    for item in char:
      bit_array = number_to_bit_array(item)
      bit_array.append(False)
      temp_converted_bit_list.append(bit_array)
    converted_bit_list.append(temp_converted_bit_list)

  for char in range(len(converted_bit_list)):
    rotated_bit_list.append([])
    for y in range(len(converted_bit_list[0])):
      rotated_bit_list[char].append([])
      for x in range(len(converted_bit_list[0][0])):
        rotated_bit_list[char][y].append(False)

  for i in range(len(converted_bit_list)):
    for old_x in range(len(converted_bit_list[0][0])):
      for old_y in range(len(converted_bit_list[0])):
        rotated_bit_list[i][old_x][7-old_y] = converted_bit_list[i][old_y][old_x]

  for char in rotated_bit_list:
    for x in char:
      output_list.append(bit_array_to_number(x))

  return output_list

def get_char_list(text: str):
  output_list = []
  number_list = []

  for char in text.upper():
    if char is not " ":
      number_list.append(ord(char)-65)
    else:
      number_list.append(len(character_set))

  for num in number_list:
    if num is not len(character_set):
      output_list.append(character_set[num])
    else:
      output_list.append([0,0,0,0,0,0,0,0])

  return tuple(translate(output_list))


@block
def character_writer(clk, en, max, x,y,pixel, text):
  if len(text)*8 >= Canvas.width:
    raise "This is not possible to print on the screen"

  data = get_char_list(text)

  y_out = Signal(intbv(0,0,256))
  x_counter = Signal(intbv(0, 0, len(data)))
  y_counter = Signal(intbv(0, 0, 8))

  @always_comb
  def update_outputs():
    x.next = x_counter
    y.next = y_counter
    pixel.next = y_out[y_counter]

  @always_comb
  def update_sig_y():
    y_out.next = data[x_counter]

  @always_comb
  def update_max():
    if x_counter == x_counter.max -1:
      max.next = True
    else:
      max.next = False

  @always(clk.posedge)
  def update_output():
    if en == True:
      if y_counter < y_counter.max - 1:
        y_counter.next = y_counter + 1
      else:
        y_counter.next = 0
        if x_counter < x_counter.max - 1:
          x_counter.next = x_counter + 1
        else:
          x_counter.next = 0

    else:
      x_counter.next = 0
      y_counter.next = 0

  return instances()

@block
def tb_text_writer():
  clk, en, pixel, max = [Signal(False) for _ in range(4)]
  x = Signal(intbv(0,0, Canvas.width))
  y = Signal(intbv(0,0, Canvas.height))
  text = "M and L"

  inst = character_writer(clk=clk, en=en, pixel=pixel, max=max, x=x, y=y, text=text)

  @instance
  def stimuli():
    en.next = True
    for i in range(len(text)*8*8 + 1):

      if __name__ == "__main__":
        if i%8 == 0 and i <= len(text)*8*8:
          print("")
        if pixel == True:
          print("#", end="")
        else:
          print(" ", end="")

      yield delay(10)
      clk.next = True
      yield delay(10)
      clk.next = False
    yield StopSimulation()

  return instances()

def convert():
  clk, en, pixel, max = [Signal(False) for _ in range(4)]
  x = Signal(intbv(0,0, Canvas.width))
  y = Signal(intbv(0,0, Canvas.height))
  text = "M and L"

  inst = character_writer(clk=clk, en=en, max=max, x=x, y=y, pixel=pixel, text=text)

  toVHDL.std_logic_ports = True
  toVHDL.directory = "vhdl_out/"
  toVHDL(inst, initial_value=True)
  toVHDL.std_logic_ports = True
  toVHDL.directory = "../vhdl/video_controller/"
  toVHDL(inst, initial_value=True)

def test():
  #remove old trace if exists
  vcd_path = os.path.join(os.getcwd(), TRACE_LOCATION, tb_text_writer.__name__ + ".vcd")
  if os.path.exists(vcd_path):
    print("Removed old vcd file")
    os.remove(vcd_path)

  try:
    tb = tb_text_writer()
    tb.config_sim(trace=True, directory=TRACE_LOCATION)
    tb.run_sim()
    return True
  except:
    return False


if __name__ == "__main__":

  test()
  convert()
