import subprocess 
import time
from getFirefoxURL import find_current_opened_firefox_URL
from get_youtube_info import get_youtube_info, is_url_youtube
EXCLUDE_LIST = ["","kitty","kitten","bash"]
SHELL_PROCESS="bash"
TERMINAL="kitty"
def get_terminal_processes(pid):
    output = subprocess.run("./findProcessTreeNames.sh " +  str(pid), capture_output=True, text=True, shell=True)
    std = output.stdout
    filtered_output=""
    for line in std.splitlines():
        line=line.strip()
        if line.lower() not in EXCLUDE_LIST:
            filtered_output+=line+","
    if filtered_output == "":
        #if all other excludes are filtered then shell process is open and was filtered 
        return SHELL_PROCESS
    return filtered_output[:-1]
    

def get_current_window():
    output = subprocess.run(["/usr/sbin/hyprctl", "activewindow"], capture_output=True, text=True)
    data = output.stdout
    ## if no window is open then Invalid is returned 
    if data.strip() == "Invalid":
        return { "class": "desktop"}
    out = {}
    for line in data.splitlines():
        if line[1:6] == "class":
            out["class"] = line[8:]
        elif line[1:4] == "pid":
            out["pid"] = line[6:]
    return out 

def get_current_window_data():
    win = get_current_window()
    data = [ time.time(),win["class"]]
    print(win)
    if win["class"] == "firefox":
        url = find_current_opened_firefox_URL()
        data.append(url)
        if is_url_youtube(url):
            data.append(get_youtube_info(url))
    elif win["class"] == TERMINAL:
        data.append(get_terminal_processes(win["pid"]))
    return data

if __name__ == "__main__":
    print(get_current_window_data())

