import json
import os

import requests
from dotenv import load_dotenv

load_dotenv("./.env")

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = os.getenv("CHANNEL_HANDLE")
maxResults = 50

def get_playlist_id():
    try:

        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        # print(json.dumps(data, indent=4))
        channel_items = data["items"][0]
        channel_playlist_id = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]
        return channel_playlist_id
    except requests.exceptions.RequestException as e:
        raise e

playylist_id = get_playlist_id()


def get_video_ids(playlist_id):
    video_ids = []
    page_tokens = None
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&playlistId={playlist_id}&key={API_KEY}&maxResults={maxResults}"
    try:
        while True:
            url = base_url
            if page_tokens:
                url += f"&pageToken={page_tokens}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            for item in data.get("items", []):
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)
            page_tokens = data.get('nextPageToken')
            if not page_tokens:
                break
        return video_ids
    except requests.exceptions.RequestException as e:
        raise e

if __name__ == "__main__":
    playlist_id = get_playlist_id()
    video_ids = get_video_ids(playlist_id)