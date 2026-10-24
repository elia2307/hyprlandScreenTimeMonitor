import subprocess 
import time
from getFirefoxURL import find_current_opened_firefox_URL
from getBrowserURL import Browsers, get_browser_data
EXCLUDE_LIST = ["","kitty","kitten","bash", "node-MainThread"]
SHELL_PROCESS="bash"
TERMINAL="kitty"

def get_tmux_server_pid(tmux_client_pid):
    command = "tmux list-clients -f '#{==:#{client_pid},"+str(tmux_client_pid)+"}' -F '#{pid}'"   
    output = subprocess.run(command, capture_output=True, text=True, shell=True)
    std = output.stdout
    return std.strip()

def get_tmux_processes(pid):
    tmux_pid = get_tmux_server_pid(pid)
    return get_terminal_processes(tmux_pid)

def get_terminal_processes(pid):
    output = subprocess.run("./findProcessTreeNames.sh " +  str(pid), capture_output=True, text=True, shell=True)
    std = output.stdout
    filtered_output=[]
    for line in std.splitlines():
        line=line.strip()
        parts = line.split(" ",1) #pid,comm (comm can have spaces so second while pid always an int)
        if len(parts) < 2:
            continue
        elif parts[1] in EXCLUDE_LIST:
            continue
        elif parts[1] == "tmux: client":
            #filtered_output += parts[1] + "," + get_tmux_processes(parts[0]) + ","
            filtered_output.append(parts[1])
            filtered_output.append(get_tmux_processes(parts[0]))
        else:
            #filtered_output+=parts[1]+","
            filtered_output.append(parts[1])

    if filtered_output == "":
        #if all other excludes are filtered then shell process is open and was filtered 
        return SHELL_PROCESS
    return filtered_output
    

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
    data = [ int(time.time()),win["class"]]
    if win["class"] == "firefox":
        data.append(get_browser_data(Browsers.FIREFOX))
    elif win["class"] == "chromium":
        data.append(get_browser_data(Browsers.CHROMIUM))
    elif win["class"] == "google-chrome":
        data.append(get_browser_data(Browsers.CHROME))
    elif win["class"] == TERMINAL:
        data.append(get_terminal_processes(win["pid"]))
    print(data)
    return data

if __name__ == "__main__":
    print(get_current_window_data())

