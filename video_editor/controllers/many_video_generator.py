from tiktok_api.controllers.tiktok_api_handler import upload_video, login_to_tiktok_account
from video_editor.controllers.game_plus_podcast_video_editor import GamePlusPodcastVideoEditor
from video_editor.controllers.generic_video_editor import GenericVideoEditor


class ManyVideoGenerator:
    @staticmethod
    def generate(timestamps, base_video_name, video_editor: GenericVideoEditor) -> list[str]:
        videos_paths = []
        for index, (start, end) in enumerate(timestamps):
            print(str(index) + " " + str(start) + " " + str(end))
            video_path = video_editor.generateVideo(start, end, base_video_name + "_" + str(index))
            videos_paths.append(video_path)
        return videos_paths


gppve = GamePlusPodcastVideoEditor('https://www.youtube.com/watch?v=MyAWr7qImdQ',
                                   'https://www.youtube.com/watch?v=iYipwtIa1Po', video_quality=1080)

timestamps = [(3, 72)]

paths = ManyVideoGenerator.generate(timestamps, 'output_video_name', gppve)

username = 'shortvideos799'

login_to_tiktok_account(username)

for path in paths:
    upload_video(username, path, "How guys with Cybertrucks think we react #tesla #cybertruck #elonmask")

