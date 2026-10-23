from getFirefoxURL import find_current_opened_firefox_URL
from getChromiumURL import  find_chromium_url , find_google_chrome_url 
from get_youtube_info import get_youtube_info, is_url_youtube
from enum import Enum


class Browsers(Enum):
    FIREFOX = 1
    CHROME = 2 
    CHROMIUM =3 


def get_most_recent_url(browser):
    match browser:
        case Browsers.FIREFOX:
            return find_current_opened_firefox_URL()
        case Browsers.CHROME:
            return find_google_chrome_url()
        case Browsers.CHROMIUM:
            return find_chromium_url()

def get_browser_data(browser):
    url = get_most_recent_url(browser)
    data = []
    data.append(url)
    if is_url_youtube(url):
        info = get_youtube_info(url)
        if info is not  None:
            data.append(info)
    return data

