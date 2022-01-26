VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH = [1,0,0]

class AIInfo:
  def __init__(self):
    self.number_of_neurons_per_layer = 10
    self.physical_number_of_neurons_per_layer = self.number_of_neurons_per_layer
    self.number_of_inputs = 10
    self.number_of_outputs = 3
    self.number_of_layers = 10
    self.physicial_layers = self.number_of_layers
    self.activation_type = "ramp" # future: relu (sigmoid comparable option)
    self.fixed_point_division = 2**10
    self.signed_bus_width = 32
    # step -> y(u) = (0 if u < 0) or (1 if u >= 0)
    # ramp -> y(u) = max(0, min(u, fixed_point_division))
    # relu -> y(u) = max(0, u)
    # sig -> y(u) = (u)/(1+|u|)
    self.error_checking_function = "rms"

ai_info = AIInfo()

def print_project_info():
  print("+--------------------------------------------------+")
  print("|Neural network project                            |")
  print("|© Loek Lankhorst & Michael Ladru                  |")
  print("+--------------------------------------------------+")
  print("|Version: {}.{}.{}                                    |".format(VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH))
  print("|Date: 7 January 2022                              |")
  print("|Executed in the name of Fontys                    |")
  print("|All the intellectual information belongs to Fontys|")
  print("+--------------------------------------------------+")
  print("| The purpose of this project is to find three     |")
  print("| type waves in an audio signal.                   |")
  print("| - Square wave                                    |")
  print("| - Triangle wave                                  |")
  print("| - Sine wave                                      |")

def print_ai_info():
  print("+--------------------------------------------------+")
  print("Neural network information")
  for key in ai_info.__dict__:
    print("  - " +  key.replace("_", " ") + ":",ai_info.__dict__[key])

if __name__ == "__main__":
  pass
  print_project_info()
  print_ai_info()
