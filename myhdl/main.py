import drawn_memory
import mod_counter
import mux
import position_validator
import sine_generator
import square_generator
import triangle_generator
import vga
import video_state_machine
import gen_offset

if __name__ == "__main__":
  functions = [drawn_memory.Main, mod_counter.Main, mux.Main, square_generator.Main, vga.Main, video_state_machine.Main, triangle_generator.Main, sine_generator.Main, position_validator.Main, gen_offset.Main]

  for function in functions:
    print("Generating VHDL for: {}".format(function.__name__))
    function()




  print("Press enter to continue...")
  input()
