import subprocess 
from getFirefoxURL import findCurrentOpenedFirefoxURL

def getCurrentWindow():
    output = subprocess.run(["/usr/sbin/hyprctl", "activewindow"], capture_output=True, text=True)
    data = output.stdout
    for line in data.splitlines():
        if line[1:6] == "class":
            return line[8:]
        


if __name__ == "__main__":
    win = getCurrentWindow()
    print(win)
    if win == "firefox":
        print(findCurrentOpenedFirefoxURL())

