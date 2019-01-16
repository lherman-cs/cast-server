from youtube_dl import YoutubeDL
from vlc import Instance


class Video:
    __ydl_format = "best"
    has_audio = True
    title = ""
    video_url = ""
    audio_url = ""
    thumbnail_url = ""

    def __init__(self, vlc: Instance, url: str):
        with YoutubeDL({"format": self.__ydl_format}) as ydl:
            info = ydl.extract_info(url, download=False)

            self.title = info["title"]

            # This means there's the video got splitted up to
            # video-only and audio-only
            if "requested_formats" in info:
                formats = info["requested_formats"]

                # TODO! maybe the order of formats matters
                self.video_url = formats[0]["url"]
                self.audio_url = formats[1]["url"]
                self.has_audio = False
            else:
                self.video_url = info["url"]

            self.thumbnail_url = info["thumbnail"]

            self.media = vlc.media_new(self.video_url)
            if not self.has_audio:
                self.media.slaves_add(1, 4, self.audio_url)
