import os, json, lz4.block

def writeJSONData(data):
    w = open("log.txt", "w")
    w.write(str(data))
def readFirefoxData(path):
    f = open(path, "rb")
    magic = f.read(8)
    if magic != b'mozLz40\x00':
        raise ValueError("Header of firefox file is wrong for path:" + path) 
    jdata = json.loads(lz4.block.decompress(f.read()).decode("utf-8"))

    #writeJSONData(jdata)

    return jdata
def getMainEntry(tab):
    if len(tab["entries"])==0:
        raise ValueError("No readable tab data")
    i = int(tab["index"])-1
    return tab["entries"][i]
def getCurrentOpenedURL(path):
    firefox_json = readFirefoxData(path)

    last_accessed_time = 0
    last_accessed_tab = 0
    for win in firefox_json["windows"]:
        for tab in win["tabs"]:
            if tab["lastAccessed"] > last_accessed_time:
                last_accessed_tab = tab
                last_accessed_time = tab["lastAccessed"]
    return getMainEntry(last_accessed_tab)["url"]


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


def findCurrentOpenedFirefoxURL():
    mozillaFolder = os.getenv("HOME") + "/.mozilla/firefox/"
    path=find_firefox_session_file(mozillaFolder)
    return getCurrentOpenedURL(path)

if __name__ == "__main__":
    print(findCurrentOpenedFirefoxURL())

