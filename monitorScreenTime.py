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
    f = open(IDLE_FILE_LOCATION, "w")
    f.write("false")
    f.close()


def is_hyprland_idle():
    f = open(IDLE_FILE_LOCATION, "r")
    text = f.read()
    return text == "true"
    

SLEEP_DURATION= 60
def monitor_screen_time(output_path):
    init_idle_file()
    f = open(output_path, "a")
    while True:
        if not is_hyprland_idle():
            data = get_current_window_data()
            print("active")
        else:
            data = [ time.time(), "IDLE"]
            print("idle")
        f.write(str(data)+"\n")
        f.flush()
        time.sleep(SLEEP_DURATION)



 
if __name__ == "__main__":
    output_path = os.getenv("output_location", os.getenv("HOME")+"/.local/state/screenTime.log")
    print(output_path)
    if sys.argv ==2:
        output_path = sys.argv[2]

    monitor_screen_time(output_path)
