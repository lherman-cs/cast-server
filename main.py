from pprint import pprint
from json import dumps

from youtube_dl import YoutubeDL

import vlc
from vlc import MediaSlaveType
import sys

import tkinter


# import standard libraries
import os
import pathlib
from threading import Thread, Event
import time
import platform


def get_stream_url(url):
    info = {}
    with YoutubeDL({"format": "bestvideo+bestaudio/best"}) as ydl:
        info = ydl.extract_info(url, download=False)
    return info


class VideoPlayer:
    def __init__(self, url, title=None):
        formats = get_stream_url(url)["requested_formats"]
        video_url = formats[0]["url"]
        audio_url = formats[1]["url"]

        self.Instance = vlc.Instance()

        self.player = self.Instance.media_player_new()
        media = self.Instance.media_new(video_url)
        self.player.set_media(media)
        self.player.add_slave(1, audio_url, True)
        self.player.set_fullscreen(True)

        self.player.play()

        while 1:
            pass


VideoPlayer("https://www.youtube.com/watch?v=oPpzJAzdpTU")
