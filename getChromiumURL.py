from chromagnon.SNSSParse import parse as parse_SNSS
import chromagnon.sessionParse
from chromagnon.sessionParse import parse as parse_session
import os

def find_last_tab(session_commands):
    url = ""
    for command in session_commands:
        if type(command) == chromagnon.sessionParse.CommandUpdateTabNavigation:
            url = command.url
    return url

def find_most_recent_session(path):
    last_modified = 0
    session_path = ""
    for file in os.listdir(path):
        if not file.startswith("Session_"):
            continue
        file_path = path + "/" + file 
        if os.path.exists(file_path):
            mod = os.path.getmtime(file_path)
            if mod > last_modified:
                last_modified = mod
                session_path = file_path
    return session_path

def get_last_tab(path):
    snss = parse_SNSS(path)
    session_command = parse_session(snss)
    return find_last_tab(session_command)
    

def find_chromium_session_file():
    folder = os.getenv("HOME") + "/.config/chromium/Profile 8/Sessions/" 
    return find_most_recent_session(folder)

def find_google_chrome_session_file():
    folder = os.getenv("HOME") + "/.config/google-chrome/Default/Sessions/"
    return find_most_recent_session(folder)

def find_chromium_url():
    path = find_chromium_session_file()
    return get_last_tab(path)

def find_google_chrome_url():
    path = find_google_chrome_session_file()
    return get_last_tab(path)
    





if __name__ == "__main__":
    path = os.getenv("HOME")+ "/.config/chromium/Profile 8/Sessions/" 
    path = find_most_recent_session(path)
    snss = parse_SNSS(path)
    sessionCommand = parse_session(snss)
    #for command in sessionCommand:
    #    print(command)
    print(get_last_tab(sessionCommand))

