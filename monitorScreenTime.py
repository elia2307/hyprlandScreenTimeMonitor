from getCurrentUsedWindow import get_current_window_data
import sys
import os
import time
from dotenv import load_dotenv, find_dotenv 
load_dotenv(find_dotenv())


IDLE_FILE_LOCATION= os.getenv("HOME") + "/.cache/idleState"
"""uses hypridle
 when idle sets file to true 
 when resume set file to false
 config to achieve this:
listener {
    timeout = 150
    ignore_inhibit = true
    on-timeout = echo "true" > ~/.cache/idleState
    on-resume = echo "false" > ~/.cache/idleState
}
"""

def init_idle_file():
    try:
        f = open(IDLE_FILE_LOCATION, "w")
        f.write("false")
        f.close()
    except Exception as  e: 
        print("Exception raised initialising init file:",e) 


def is_hyprland_idle():
    try : 
        f = open(IDLE_FILE_LOCATION, "r")
        text = f.read().strip()
        return text == "true"
    except Exception as e:
        print("Exception raised checking if hyprland is idle:",e)
        return False
    

SLEEP_DURATION= 60
def monitor_screen_time(output_path):
    init_idle_file()
    f = open(output_path, "a")
    while True:
        try:
            if not is_hyprland_idle():
                data = get_current_window_data()
                print("active")
            else:
                data = [ time.time(), "IDLE"]
                print("idle")
            f.write(str(data)+"\n")
            f.flush()
            time.sleep(SLEEP_DURATION)
        except Exception as e:
            print("Exception raised in monitor screen time loop:",e)

def get_output_location():
    if sys.argv ==2:
        return sys.argv[2]
    home_path = os.getenv("HOME","")
    output_path = os.getenv("output_location", "")
    if output_path == "" :
        if home_path == "":
            print ("warning output_location env is not set and home environemtn variable is also not set")
            return "screenTime.log"
        else:
            return  home_path + "/.local/state/screenTime.log"
    return output_path 


 
if __name__ == "__main__":
    output_path = get_output_location()
    monitor_screen_time(output_path)
