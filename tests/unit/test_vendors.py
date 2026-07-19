# tests/unit/test_vendors.py

from pathlib import Path
import sys
import time
from datetime import datetime

# Ensure repo root is on sys.path so we can import bootstrap
repo_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo_root))

import bootstrap  # noqa: E402

import openpyxl
from gameboy_automation.utils.custom_string import CustomString
from gameboy_automation.utils.custom_string.palettes import TABLEAU_20
from gameboy_automation.utils.benchmark import Benchmark

def main() -> None:
    # Setup colored strings
    color_purple = CustomString("this will be replaced")
    color_gray = CustomString("this will be replaced")
    color_blue = CustomString("this will be replaced")
    color_light_gray = CustomString("this will be replaced")
    color_light_orange = CustomString("this will be replaced")
    color_light_gray = CustomString("this will be replaced")
    color_light_yellow = CustomString("this will be replaced")
    color_light_green = CustomString("this will be replaced")
    color_cyan = CustomString("this will be replaced")
    color_light_pink = CustomString("this will be replaced")
    color_red = CustomString("this will be replaced")
    color_blue.set_color(TABLEAU_20["blue"])
    color_gray.set_color(TABLEAU_20["gray"])
    color_light_gray.set_color(TABLEAU_20["light_gray"])
    color_light_orange.set_color(TABLEAU_20["light_orange"])
    color_purple.set_color(TABLEAU_20["purple"])
    color_light_gray.set_color(TABLEAU_20["light_gray"])
    color_light_yellow.set_color(TABLEAU_20["light_olive"])
    color_light_green.set_color(TABLEAU_20["light_green"])
    color_cyan.set_color(TABLEAU_20["cyan"])
    color_light_pink.set_color(TABLEAU_20["light_pink"])
    color_red.set_color(TABLEAU_20["red"])

    with Benchmark("test_benchmark_and_custom_colors.py") as timer:
        #placeholder start
        print(" Vendors tested!")
	#placeholder end
	
    # main code goes here
    output_string = color_gray.replace_text(" Gray ")
    output_string += color_blue.replace_text(" Blue ")
    output_string += color_light_green.replace_text(" Blue ")
    print(output_string)
    print(" "+color_gray.replace_text("Elapsed: ")+color_gray.replace_text((timer.human_readable_string_without_microseconds())))

if __name__ == "__main__":
    main()
