import os, json, lz4.block

def write_JSON_data(data):
    w = open("log.txt", "w")
    w.write(str(data))
def read_firefox_data(path):
    f = open(path, "rb")
    magic = f.read(8)
    if magic != b'mozLz40\x00':
        raise ValueError("Header of firefox file is wrong for path:" + path) 
    jdata = json.loads(lz4.block.decompress(f.read()).decode("utf-8"))


    return jdata
def get_main_entry(tab):
    if len(tab["entries"])==0:
        raise ValueError("No readable tab data")
    i = int(tab["index"])-1
    return tab["entries"][i]
def get_current_opened_URL(path):
    firefox_json =read_firefox_data(path)

    last_accessed_time = 0
    last_accessed_tab = 0
    for win in firefox_json["windows"]:
        for tab in win["tabs"]:
            if tab["lastAccessed"] > last_accessed_time:
                last_accessed_tab = tab
                last_accessed_time = tab["lastAccessed"]
    return get_main_entry(last_accessed_tab)["url"]


def find_firefox_session_file(firefox_folder):
    """ 
    WARNING if 2 profiles open at same time then each sessionstore-backups will get updated around same time 
    so will randomly pick between 2, since modification times will be slightly different but both get saved at same time ish
    """
    relative_path="/sessionstore-backups/recovery.jsonlz4"
    firefox_path = ""
    last_modified = 0
    for dir in os.listdir(firefox_folder):
        path = firefox_folder + dir + relative_path
        if os.path.exists(path):
            mod = os.path.getmtime(path)
            #print(mod)
            if mod > last_modified:
                last_modified = mod
                firefox_path = path
    return firefox_path


def find_current_opened_firefox_URL():
    mozillaFolder = os.getenv("HOME") + "/.mozilla/firefox/"
    path=find_firefox_session_file(mozillaFolder)
    return get_current_opened_URL(path)

if __name__ == "__main__":
    print(find_current_opened_firefox_URL())

