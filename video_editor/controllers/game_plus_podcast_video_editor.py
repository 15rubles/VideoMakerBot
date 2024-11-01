import glob
import os
import shutil

import ffmpeg
import whisper
from PIL import Image, ImageDraw, ImageFont

from external_api.apis.youtube_api import YouTubeController
from video_editor.controllers.generic_video_editor import GenericVideoEditor


class GamePlusPodcastVideoEditor(GenericVideoEditor):

    def __init__(self, main_video_link, second_video_link, video_quality=None, audio_quality=None, fps=24,
                 video_width=1080, video_height=1920, font='Kanit-Bold.ttf'):
        self.audio_quality = audio_quality
        self.video_quality = video_quality
        self.second_video_link = second_video_link
        self.main_video_link = main_video_link
        self.save_path = "D:\\youtubeVideosForTest"
        self.yt = YouTubeController(video_quality=self.video_quality, audio_quality=self.audio_quality)
        self.fps = fps
        self.video_width = video_width
        self.video_height = video_height
        self.font = self.save_path + '\\' + font

    def generateVideo(self, start_time, end_time, output_video_name):
        main_video_mp4 = self.yt.download_video(self.main_video_link, save_path=self.save_path)
        second_video_mp4 = self.yt.download_video(self.second_video_link, save_path=self.save_path)

        main_video_mp3 = self.yt.download_audio(self.main_video_link, save_path=self.save_path)

        subtitles_text = self.__generate_subtitles(main_video_mp3, start_time, end_time)

        self.__stack_videos(main_video_mp4, second_video_mp4, subtitles_text, main_video_mp3, output_video_name,
                            start_time, end_time)

    def __stack_videos(self, overlay_video_path, background_video_path, subtitles_text, audio_path,
                       output_video_name, start_time, end_time):
        target_height = self.video_height
        target_width = self.video_width

        # Get the height and width of the first video
        overlay_video_probe = ffmpeg.probe(overlay_video_path)
        background_video_probe = ffmpeg.probe(background_video_path)
        overlay_target_width = ((target_height / 2) * overlay_video_probe['streams'][0]['width']
                                / overlay_video_probe['streams'][0]['height'])
        bg_target_width = (target_height * background_video_probe['streams'][0]['width']
                           / background_video_probe['streams'][0]['height'])

        # Create a new video with both stacked
        overlay_video = (ffmpeg.input(overlay_video_path, ss=start_time)
                         .filter('scale', overlay_target_width, -1)
                         .filter('crop', target_width, target_height / 2,
                                 overlay_target_width / 2 - target_width / 2, 0))

        background_video = (ffmpeg.input(background_video_path, t=end_time - start_time)
                            .filter('scale', bg_target_width, -1)
                            .filter('crop', target_width, target_height,
                                    bg_target_width / 2 - target_width / 2, 0))

        base_video = (ffmpeg.concat(background_video, ffmpeg.input(audio_path, ss=start_time), v=1, a=1)
                      .overlay(overlay_video))
        base_video = self.__generate_subtitles_overlay_video(subtitles_text, end_time - start_time, base_video)
        (
            base_video
            .output(self.save_path + '\\output_videos\\' + output_video_name + '.mp4', framerate=self.fps,
                    t=end_time - start_time)
            .run(overwrite_output=True)
        )

        self.__delete_subtitles_images()

    def __generate_subtitles(self, link, start_time, end_time):
        # Load the Whisper model (you can use different models like 'tiny', 'base', 'small', 'medium', 'large')
        model = whisper.load_model("base.en")

        fileout = self.__crop_audio(link, start_time, end_time)
        # Transcribe the audio file
        result = model.transcribe(fileout, word_timestamps=True)

        words = []
        # Print the transcription with timestamps
        for segment in result['segments']:
            for word in segment['words']:
                words.append(word)
                start_time = word['start']
                end_time = word['end']
                text = word['word']
                print(f"[{start_time:.2f} - {end_time:.2f}]: {text}")

        return words

    def __crop_audio(self, file_audio, start_seconds, end_seconds):
        output = "tmp.mp3"

        (
            ffmpeg.input(file_audio)
            .filter('atrim', start_seconds, end_seconds)
            .output(output)
            .run(overwrite_output=True)
        )

        return output

    def __generate_subtitles_overlay_video(self, subtitles_text, duration, ffmpeg_command, max_segment_len=35):
        # Directory to store generated subtitle images
        subtitles_dir = self.save_path + "\\subtitles"

        # Create images for each subtitle and add them to video
        index = 0
        segment = ''
        subtitles_height = 150
        start_time = 0
        for i, word in enumerate(subtitles_text):
            if len(segment + ' ' + word['word']) > max_segment_len or segment.endswith(('.', '!', '?')):
                image_path = f"{subtitles_dir}\\subtitle_{index}.png"
                ffmpeg_command = self.__add_segment_to_subtitles(segment, image_path, start_time,
                                                                 subtitles_text[i-1]['end'],
                                                                 self.video_height / 2 - subtitles_height / 2,
                                                                 ffmpeg_command)
                segment = ''
                index += 1
                start_time = subtitles_text[i]['start']
            segment += ' ' + word['word']

        if segment != '':
            image_path = f"{subtitles_dir}\\subtitle_{index}.png"
            ffmpeg_command = self.__add_segment_to_subtitles(segment, image_path, start_time, duration,
                                                             self.video_height / 2 - subtitles_height / 2,
                                                             ffmpeg_command)

        return ffmpeg_command

    def __delete_subtitles_images(self):
        subtitles_dir = self.save_path + "\\subtitles"
        files = glob.glob(subtitles_dir + "\\*")
        for f in files:
            os.remove(f)

    def __add_segment_to_subtitles(self, segment, image_path, start, end, subtitle_y, ffmpeg_command):
        image = self.__create_subtitle_image(segment)
        image.save(image_path)
        return ffmpeg_command.overlay(ffmpeg.input(image_path, loop=1, t=end - start),
                                      x=0,
                                      y=subtitle_y,
                                      enable=f'between(t,{start},{end})'
                                      )

    def __delete_and_copy_file(self, original_file_path, new_file_name):
        # Check if the original file exists
        if os.path.exists(original_file_path):
            # Create a new file path for the copy
            new_file_path = os.path.join(os.path.dirname(original_file_path), new_file_name)
            if os.path.exists(new_file_path):
                os.remove(new_file_path)

            # Copy the original file to the new file path
            shutil.copy2(original_file_path, new_file_path)
            print(f"Copied to: {new_file_path}")

            # Delete the original MP3 file
            os.remove(original_file_path)
            print(f"Deleted: {original_file_path}")
        else:
            print(f"File does not exist: {original_file_path}")

    def __create_subtitle_image(self, text, width=1080, height=150, font_size=65):
        # Create a transparent image
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        try:
            font = ImageFont.truetype(self.font, font_size)
        except IOError:
            font = ImageFont.load_default()

        # Get the size of the text and position it in the center
        text_size = draw.textsize(text, font=font)
        text_x = (width - text_size[0]) // 2
        text_y = (height - text_size[1]) // 2

        # Draw the text with white color (or change as needed)
        draw.text((text_x, text_y), text, fill=(255, 255, 0, 255), font=font)

        return image


# gppve = GamePlusPodcastVideoEditor('https://www.youtube.com/watch?v=HOhMSacJFFY',
#                                    'https://www.youtube.com/watch?v=iYipwtIa1Po', video_quality=1080)
#
# gppve.generateVideo(0, 5, 'output_video')
