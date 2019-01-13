from collections import deque
from queue import Queue
from functools import wraps

import vlc
from vlc import MediaSlaveType, Media, MediaPlayer, \
    EventManager, EventType, callbackmethod, State

from .extractor import Extractor


def operation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        def op_wrapper():
            func(*args, **kwargs)

        args[0]._VideoPlayer__ops.put(op_wrapper)

    return wrapper


class VideoPlayer:
    __vlc_args = ('--input-repeat=-1', '--fullscreen',
                  '--mouse-hide-timeout=0', '--input-fast-seek')

    def __init__(self):
        self.__vlc = vlc.Instance(*self.__vlc_args)
        self.__player = self.__vlc.media_player_new()
        self.__player.set_fullscreen(True)
        self.__event_manager = self.__player.event_manager()
        self.__event_manager.event_attach(
            EventType.MediaPlayerEndReached, self.on_end_reached)
        self.__playlist = deque()
        self.__ops = Queue()

    def main(self):
        while 1:
            op = self.__ops.get()
            op()

    @operation
    def add(self, url: str):
        ext = Extractor(url)

        media = self.__vlc.media_new(ext.video_url)
        if not ext.has_audio:
            media.slaves_add(1, 4, ext.audio_url)

        self.__playlist.append(media)
        state = self.__player.get_state()
        if state == State.Stopped or state == State.NothingSpecial:
            self.__next()

    def __next(self):
        if len(self.__playlist) == 0:
            self.__player.stop()
            return

        next_video = self.__playlist.popleft()
        self.__player.set_media(next_video)
        self.__player.play()

    @operation
    def next(self):
        self.__next()

    @operation
    def play(self):
        state = self.__player.get_state()
        if state == State.Stopped or state == State.NothingSpecial:
            self.__next()
        else:
            self.__player.play()

    @operation
    def pause(self):
        self.__player.pause()

    @operation
    def stop(self):
        self.__player.stop()

    @operation
    def seek(self, pos: float):
        self.__player.set_position(pos)

    @callbackmethod
    def on_end_reached(self, *args):
        self.next()
