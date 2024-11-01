from video_editor.controllers.game_plus_podcast_video_editor import GamePlusPodcastVideoEditor
from video_editor.controllers.generic_video_editor import GenericVideoEditor


class ManyVideoGenerator:
    @staticmethod
    def generate(timestamps, base_video_name, video_editor : GenericVideoEditor):
        for index, (start, end) in enumerate(timestamps):
            print(str(index) + " " + str(start) + " " + str(end))
            video_editor.generateVideo(start, end, base_video_name + "_" + str(index))


gppve = GamePlusPodcastVideoEditor('https://www.youtube.com/watch?v=HOhMSacJFFY',
                                   'https://www.youtube.com/watch?v=iYipwtIa1Po', video_quality=1080)

timestamps = [(0, 20)]

ManyVideoGenerator.generate(timestamps, 'output_video_name', gppve)

