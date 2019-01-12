from youtube_dl import YoutubeDL


class Extractor:
    __ydl_format = "bestvideo+bestaudio/best"
    has_audio = True
    video_url = ""
    audio_url = ""

    def __init__(self, url: str):
        with YoutubeDL({"format": self.__ydl_format}) as ydl:
            info = ydl.extract_info(url, download=False)

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
