import ffmpeg
import whisper
import moviepy.editor as mp

from external_api.apis.youtube_api import YouTubeController
from video_editor.controllers.generic_video_editor import GenericVideoEditor
from moviepy.editor import VideoFileClip, CompositeVideoClip


class GamePlusPodcastVideoEditor(GenericVideoEditor):

    def __init__(self, main_video_link, second_video_link, video_quality=None, audio_quality=None):
        self.audio_quality = audio_quality
        self.video_quality = video_quality
        self.second_video_link = second_video_link
        self.main_video_link = main_video_link
        self.save_path = "D:\youtubeVideosForTest"

    def generateVideo(self):
        yt = YouTubeController(video_quality=self.video_quality, audio_quality=self.audio_quality)

        main_video_mp4 = yt.download_video(self.main_video_link, save_path=self.save_path)
        second_video_mp4 = yt.download_video(self.second_video_link, save_path=self.save_path)

        main_video_mp3 = yt.download_audio(self.main_video_link, save_path=self.save_path)
        second_video_mp3 = yt.download_audio(self.second_video_link, save_path=self.save_path)

        self.__generateSubtitles(main_video_mp3)

        # self.__concatenate_videos(main_video_mp4, second_video_mp4, self.save_path)
        self.__stack_videos(main_video_mp4, second_video_mp4, main_video_mp3, self.save_path)

    def __stack_videos(self, overlay_video_path, background_video_path, audio_path, output_path):
        target_height = 1920
        target_width = 1080
        # Get the height and width of the first video
        overlay_video_probe = ffmpeg.probe(overlay_video_path)
        background_video_probe = ffmpeg.probe(background_video_path)
        bg_video_X = background_video_probe['streams'][0]['width'] / 2 - target_height / 2
        overlay_target_width = ((target_height / 2) * overlay_video_probe['streams'][0]['width']
                                / overlay_video_probe['streams'][0]['height'])
        # Create a new video with both stacked

        overlay_video = (ffmpeg.input(overlay_video_path, t=5)
                         .filter('scale', overlay_target_width, -1)
                         .filter('crop', target_width, target_height / 2, overlay_target_width / 2 - target_width / 2, 0))
        (
            ffmpeg.concat(ffmpeg.input(background_video_path, t=5),
                          ffmpeg.input(audio_path, t=5), v=1, a=1)
            .overlay(overlay_video)
            .output(output_path + '\\OUT_VIDE.MP4', framerate=24)
            .run()
        )

    def __concatenate_videos(self, main_video_mp4, second_video_mp4, save_path):
        # Define the duration for each video (in seconds)
        duration = 5

        # Prepare the input video streams
        input1 = ffmpeg.input(main_video_mp4, ss=0, t=duration)
        input2 = ffmpeg.input(second_video_mp4, ss=0, t=duration)

        # Get video properties for resizing
        probe1 = ffmpeg.probe(main_video_mp4)
        probe2 = ffmpeg.probe(second_video_mp4)

        video1_width = probe1['streams'][0]['width']
        video1_height = probe1['streams'][0]['height']
        video2_width = probe2['streams'][0]['width']
        video2_height = probe2['streams'][0]['height']

        # Determine the final width and height for the output
        final_width = max(video1_width, video2_width)
        final_height = max(video1_height, video2_height)

        # Resize each video to occupy half of the final height and the final width
        input1_resized = input1.filter('scale', final_width, final_height / 2)
        input2_resized = input2.filter('scale', final_width, final_height / 2)

        # Combine the two videos vertically
        output = (
            ffmpeg
            .filter([input1_resized, input2_resized], 'vstack')
            .output(
                save_path + "/output_video_fast.mp4",
                vcodec='libx264',
                acodec='aac',
                threads=4,
                preset='fast',
                video_bitrate='500k',
                format='mp4'
            )
        )

        # Run the ffmpeg command
        ffmpeg.run(output)

    def __generateSubtitles(self, link):

        # Load the Whisper model (you can use different models like 'tiny', 'base', 'small', 'medium', 'large')
        model = whisper.load_model("tiny.en")

        # Transcribe the audio file
        result = model.transcribe(link)

        # Print the transcription with timestamps
        for segment in result['segments']:
            start_time = segment['start']
            end_time = segment['end']
            text = segment['text']
            print(f"[{start_time:.2f} - {end_time:.2f}]: {text}")




gppve = GamePlusPodcastVideoEditor('https://www.youtube.com/watch?v=HOhMSacJFFY', 'https://www.youtube.com/watch?v=iYipwtIa1Po', video_quality=1080)

gppve.generateVideo()