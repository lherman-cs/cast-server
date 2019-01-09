from collections import deque
from queue import Queue

import vlc
from vlc import MediaSlaveType, Media, MediaPlayer, \
    EventManager, EventType, callbackmethod, State

from .extractor import Extractor


def operation(func):
    def wrapper(self, *args, **kwargs):
        def op_wrapper():
            func(self, *args, **kwargs)

        self._VideoPlayer__ops.put(op_wrapper)

    return wrapper


class VideoPlayer:
    __vlc_args = ('--input-repeat=-1', '--fullscreen',
                  '--mouse-hide-timeout=0', '--input-fast-seek')

    def __init__(self):
        self.__vlc = vlc.Instance(*self.__vlc_args)
        self.__player: MediaPlayer = self.__vlc.media_player_new()
        self.__player.set_fullscreen(True)
        self.__event_manager: EventManager = self.__player.event_manager()
        self.__event_manager.event_attach(
            EventType.MediaPlayerEndReached, self.on_end_reached)
        self.__playlist = deque()
        self.__ops = Queue()

    def main(self):
        while 1:
            self.__ops.get()()

    @operation
    def add(self, url: str):
        ext = Extractor(url)

        media: Media = self.__vlc.media_new(ext.video_url)
        if not ext.has_audio:
            media.slaves_add(1, 4, ext.audio_url)

        self.__playlist.append(media)

    @operation
    def next(self):
        if len(self.__playlist) == 0:
            self.__player.stop()
            return

        next_video: Media = self.__playlist.popleft()
        self.__player.set_media(next_video)
        self.__player.play()

    @operation
    def play(self):
        state = self.__player.get_state()
        if state == State.Stopped or state == State.NothingSpecial:
            self.next()
        else:
            self.__player.play()

    @operation
    def pause(self):
        self.__player.pause()

    @operation
    def seek(self, pos: float):
        self.__player.set_position(pos)

    @callbackmethod
    def on_end_reached(self, *args):
        self.next()
