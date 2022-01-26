import os
import sys
import warnings
from colorama import Fore, init
from neural_network import neural_network_info

from video_controller import *
import video_controller as vico

from neural_network import *
import neural_network as nene

import numpy as np

DEBUG = False

VIDEO_CONTROLLER_PATH = os.getcwd() + "/video_controller/"
NEURAL_NETWORK_PATH = os.getcwd() + "/neural_network/"

# Suppress warnings, because they are already checked
warnings.filterwarnings("ignore")

if __name__ == "__main__":

    if "3.7.3" not in sys.version:
        print("Your python version is not compatible, press enter to exit")
        input()
        exit(0)

    init()

    neural_network_info.print_project_info()
    neural_network_info.print_ai_info()

    modules = [
        nene.threshold_detector,
        vico.source_selector,
        vico.character_writer,
        vico.drawn_memory,
        vico.mod_counter,
        vico.video_mux,
        vico.square_generator,
        vico.vga,
        vico.video_state_machine,
        vico.triangle_generator,
        vico.sine_generator,
        vico.position_validator,
        vico.gen_offset
    ]

    i = 0
    progress = np.linspace(0, 100, len(modules)+1)

    print(Fore.CYAN + "<=== Testing modules ===>" + Fore.RESET)
    # Print progress on testing modules
    for i in range(len(modules)):
        module_name = modules[i].__name__.replace(modules[i].__package__ + ".", "")
        try:
            result = modules[i].test()
            if result:
                print("[{}{}{:.2f}%{}{}] - Tested for: {}".format(Fore.GREEN,(" " if (i < len(modules)-1)
                else ""), progress[i+1], (" " if (progress[i+1] < 10.0) else ""), Fore.RESET, module_name))
            else:
                print("[{}{}{:.2f}%{}{}] - Failed test for: {}".format(Fore.RED,(" " if (i < len(modules)-1)
                else ""), progress[i+1], (" " if (progress[i+1] < 10.0) else ""), Fore.RESET, module_name))
        except:
            print("[{}{}{:.2f}%{}{}] - No tests found for: {}".format(Fore.BLUE,(" " if (i < len(modules)-1)
              else ""), progress[i+1], (" " if (progress[i+1] < 10.0) else ""), Fore.RESET, module_name))

    print(Fore.CYAN + "<=== Generating VHDL ===>" + Fore.RESET)
    # print progress and corresponding file to screen
    for i in range(len(modules)):
        module_name = modules[i].__name__.replace(modules[i].__package__ + ".", "")
        print("[{}{}{:.2f}%{}{}] - Generating VHDL for: {}".format(Fore.GREEN, (" " if (i < len(modules)-1)
              else ""), progress[i+1], (" " if (progress[i+1] < 10.0) else ""), Fore.RESET, module_name))
        modules[i].convert()

    print(Fore.GREEN + "Finished!" + Fore.RESET)
