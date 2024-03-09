#! /bin/bash
path_to_this_script="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
path_to_venv="$(cd "$path_to_this_script/../../venv" && pwd)"

#Activate venv and run python script for clearing the screen
source $path_to_venv/bin/activate && $path_to_venv/bin/python $path_to_this_script/clear_screen_on_shutdown.py
