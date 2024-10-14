from pytubefix import YouTube


class YouTubeController:
    def __init__(self, video_quality=None, audio_quality=None):
        self.video_quality = video_quality
        self.audio_quality = audio_quality

    @staticmethod
    def get_youtube_video(link):
        try:
            yt = YouTube(link)
            return yt
        except:
            # to handle exception
            print("Connection Error")
            return

    def download_video(self, link, save_path):
        self.__download_video_piece(link, save_path, 'video', 'p', 'resolution')

    def download_audio(self, link, save_path):
        self.__download_video_piece(link, save_path, 'audio', 'kbps', 'abr', True)

    def __download_video_piece(self, link, save_path, piece_type, replace_part, attr, mp3=False):
        try:
            yt = YouTube(link)
        except:
            # to handle exception
            print("Connection Error")
            return

        mp4_streams = yt.streams.filter(file_extension='mp4', type=piece_type)

        if self.video_quality is None:
            d_piece = max(
                mp4_streams,
                key=lambda stream: int(getattr(stream, attr, '0').replace(replace_part, '')),
                default=None
            )
        else:
            d_piece = next(
                (stream for stream in mp4_streams if
                 int(getattr(stream, attr, '0').replace(replace_part, '')) == self.video_quality),
                None
            )

            # If not found, find the nearest higher resolution
            if d_piece is None:
                # Sort streams by resolution and get the first one with a resolution greater than 144p
                d_piece = min(
                    (stream for stream in mp4_streams if
                     int(getattr(stream, attr, '0').replace(replace_part, '')) > self.video_quality),
                    key=lambda stream: int(getattr(stream, attr, '0').replace(replace_part, '')),
                    default=None
                )

            if d_piece is None:
                d_piece = max(
                    (stream for stream in mp4_streams if
                     int(getattr(stream, attr, '0').replace(replace_part, '')) < self.video_quality),
                    key=lambda stream: int(getattr(stream, attr, '0').replace(replace_part, '')),
                    default=None
                )

        if d_piece is not None:
            d_piece.download(output_path=save_path, mp3=mp3)
