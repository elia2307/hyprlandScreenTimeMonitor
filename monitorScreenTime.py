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
    
BANNED_SYMBOLS = ",[]\n\\()"
def encode_uri(string):
    out = ""
    prev_encode = False
    for c in string:
        if c in BANNED_SYMBOLS or (c.isnumeric() and prev_encode):
            out+="%"+str(ord(c))
            prev_encode=True
        elif c.isnumeric():
            #numbers only need to get encoded if previous sequence is %num since that creates ambiougity 
            out+=c
        else: 
            out+=c
            prev_encode = False

    return out 

def decode_uri(string):
    out = ""
    while string.find("%") != -1:
        out+=string[:string.find("%")]
        string=string[string.find("%")+1:]
        num = ""
        while len(string) > 0 and string[0].isnumeric():
            num+=string[0]
            string = string[1:]
        out+=chr(int(num))
    return out+string


def encode_arr(arr):
    #data in format [time, proc, proc_info]
    #convert all characters not letters to %num encoding (numbers also since that could change %num if previous sequence is encoded)
    #overly caustious approach however means that junk data can't try and break screentime.log (e.g , or \n)
    out = ""
    for part in arr:
        if type(part) is list:
            #can have arrays in data so recursively combine and add brackets 
            out+= "[" +encode_arr(part) + "]"+","
        else:
            out+=encode_uri(str(part)) + ","
    if out[-1] == ",":
        out=out[:-1]
    return out




SLEEP_DURATION= 60
def monitor_screen_time(output_path):
    init_idle_file()
    f = open(output_path, "a")
    while True:
        start=time.time()
        try:
            if not is_hyprland_idle():
                data = get_current_window_data()
                print("active")
            else:
                data = [ int(time.time()), "IDLE"]
                print("idle")
            f.write(encode_arr(data)+"\n")
            #f.write(str(data)+"\n")
            f.flush()
        except Exception as e:
            print("Exception raised in monitor screen time loop:",e)
        sleep_time = SLEEP_DURATION - (time.time() - start)
        if sleep_time > 0:
            time.sleep(sleep_time)

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
