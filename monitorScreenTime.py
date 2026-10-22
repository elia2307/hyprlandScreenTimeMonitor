from getCurrentUsedWindow import get_current_window_data
from time import sleep
import os

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
def is_hyprland_idle():
    f = open(IDLE_FILE_LOCATION, "r")
    text = f.read()
    return text == "true"
    

SLEEP_DURATION= 60
def monitor_screen_time():
    f = open("screenTime.log", "a")
    while True:
        if not is_hyprland_idle():
            data = get_current_window_data()
            f.write(str(data)+"\n")
            f.flush()
            print("active")
        else:
            print("idle")
        sleep(SLEEP_DURATION)



        
if __name__ == "__main__":
    monitor_screen_time()
