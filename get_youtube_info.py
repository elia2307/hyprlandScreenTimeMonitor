from googleapiclient.discovery import build 
import os
from dotenv import load_dotenv, find_dotenv
#put api key in .env file in format API_KEY = '{KEY}'
load_dotenv(find_dotenv())
DEVELOPER_KEY = os.getenv("API_KEY")

youtube_cache = {}
youtube = build('youtube', 'v3', developerKey=DEVELOPER_KEY)
def get_video_details(video_id):
    if video_id in youtube_cache:
        return youtube_cache[video_id]
    
    request = youtube.videos().list(part='snippet', id=video_id)
    details = request.execute()
    title = details['items'][0]['snippet']['title']
    channel = details['items'][0]['snippet']['channelTitle']
    channelID = details['items'][0]['snippet']['channelId']
    kind = details['items'][0]['kind']
    out = [title, channel, channelID, kind]
    youtube_cache[video_id] = out
    return out 
    

def try_get_video_details(video_id, max_attempts=3):
    for i in range(max_attempts):
        try:
            data = get_video_details(video_id)
            return data
        except Exception as e:
            print("exception raised in try_get_video_details attempt:",i,":",e)
    return 

def is_url_youtube(url):
    url = url.lower()
    start_prefix1= "https://"
    start_prefix2 = "www."
    if url.startswith(start_prefix1):
        url= url[len(start_prefix1):]
    if url.startswith(start_prefix2):
        url= url[len(start_prefix2):]
    youtube = "youtube.com"
    return url.startswith(youtube) 

YOUTUBE_ID_LENGTH = 11
def get_url_id(url):
    start_prefix1= "https://"
    start_prefix2 = "www."
    start_prefix3 = "youtube.com"
    if url.startswith(start_prefix1):
        url= url[len(start_prefix1):]
    if url.startswith(start_prefix2):
        url= url[len(start_prefix2):]
    if url.startswith(start_prefix3):
        url= url[len(start_prefix3):]
    else:
        return ""
    #removes https://www.youtube.com from start of url 
    watch_prefix = "/watch?v="
    if not url.startswith(watch_prefix):
        return ""
    url= url[len(watch_prefix):]
    return url[:YOUTUBE_ID_LENGTH]
    



def get_youtube_info(url):
    #assumes url is a valid youtube url     
    id = get_url_id(url)
    if id == "":
        #not a watch id could be feed 
        return 
    return  try_get_video_details(id)
    

