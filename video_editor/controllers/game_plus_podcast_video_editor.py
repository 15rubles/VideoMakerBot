import ffmpeg
import whisper
import os, glob, shutil

from external_api.apis.youtube_api import YouTubeController
from video_editor.controllers.generic_video_editor import GenericVideoEditor
from PIL import Image, ImageDraw, ImageFont


class GamePlusPodcastVideoEditor(GenericVideoEditor):

    def __init__(self, main_video_link, second_video_link, video_quality=None, audio_quality=None, fps=24,
                 video_width=1080, video_height=1920):
        self.audio_quality = audio_quality
        self.video_quality = video_quality
        self.second_video_link = second_video_link
        self.main_video_link = main_video_link
        self.save_path = "D:\youtubeVideosForTest"
        self.yt = YouTubeController(video_quality=self.video_quality, audio_quality=self.audio_quality)
        self.fps = fps
        self.video_width = video_width
        self.video_height = video_height

    def generateVideo(self, start_time, end_time):
        main_video_mp4 = self.yt.download_video(self.main_video_link, save_path=self.save_path)
        second_video_mp4 = self.yt.download_video(self.second_video_link, save_path=self.save_path)

        main_video_mp3 = self.yt.download_audio(self.main_video_link, save_path=self.save_path)

        subtitles_text = self.__generateSubtitles(main_video_mp3, start_time, end_time)

        subtitle_video = self.__generateSubtitlesOwerlayVideo(subtitles_text, end_time - start_time)

        self.__stack_videos(main_video_mp4, second_video_mp4, subtitle_video, main_video_mp3)

    def __stack_videos(self, overlay_video_path, background_video_path, subtitle_video_path, audio_path):
        target_height = self.video_height
        target_width = self.video_width
        video_len = 5

        # Get the height and width of the first video
        overlay_video_probe = ffmpeg.probe(overlay_video_path)
        background_video_probe = ffmpeg.probe(background_video_path)
        bg_video_X = background_video_probe['streams'][0]['width'] / 2 - target_height / 2
        overlay_target_width = ((target_height / 2) * overlay_video_probe['streams'][0]['width']
                                / overlay_video_probe['streams'][0]['height'])
        bg_target_width = (target_height * background_video_probe['streams'][0]['width']
                                / background_video_probe['streams'][0]['height'])

        # Create a new video with both stacked
        overlay_video = (ffmpeg.input(overlay_video_path, t=video_len)
                         .filter('scale', overlay_target_width, -1)
                         .filter('crop', target_width, target_height / 2,
                                 overlay_target_width / 2 - target_width / 2, 0))

        background_video = (ffmpeg.input(background_video_path, t=video_len)
                            .filter('scale', bg_target_width, -1)
                            .filter('crop', target_width, target_height,
                                    bg_target_width / 2 - target_width / 2, 0))
        (
            ffmpeg.concat(background_video,
                          ffmpeg.input(audio_path, t=video_len), v=1, a=1)
            .overlay(overlay_video)
            .overlay(ffmpeg.input(subtitle_video_path, t=video_len).filter('format', 'yuva420p'))
            .output(self.save_path + '\\OUT_VIDE.MP4', framerate=self.fps)
            .run(overwrite_output=True)
        )

    def __generateSubtitles(self, link, start_time, end_time):
        # Load the Whisper model (you can use different models like 'tiny', 'base', 'small', 'medium', 'large')
        model = whisper.load_model("tiny.en")

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

    def __generateSubtitlesOwerlayVideo(self, subtitles_text, duration):
        # Directory to store generated subtitle images
        subtitles_dir = self.save_path + "\\subtitles"

        # create empty video for subtitles
        width = self.video_width
        height = self.video_height
        color = "0x00000000"  # transparent
        subtitles_video = self.save_path + '\\subtitles_video.mov'

        # Create an empty video with a specific size and length
        ffmpeg.input(
            'color=c={}:s={}x{}:d={}'.format(color, width, height, duration),
            f='lavfi'
        ).output(
            subtitles_video,
            pix_fmt='yuva420p',
            vcodec='prores_ks',
            r=self.fps  # Frames per second
        ).run(overwrite_output=True)

        # Create images for each subtitle and add them to video
        subtitles_video_final = self.save_path + '\\subtitles_video_final.mp4'
        index = 0
        start_segment_index = 0
        segment = ''
        for i, word in enumerate(subtitles_text):
            segment += ' ' + word['word']
            if segment.endswith(('.', '!', '?')):
                image = self.__create_subtitle_image(segment)
                image_path = f"{subtitles_dir}\\subtitle_{index}.png"
                image.save(image_path)
                start = subtitles_text[start_segment_index]['start']
                end = subtitles_text[i]['end']
                try:
                    (
                        ffmpeg.input(subtitles_video)
                        .overlay(ffmpeg.input(image_path, loop=1, t=end - start),
                                 x=0,
                                 y=self.video_height / 2,
                                 enable=f'between(t,{start},{end})'
                                 )
                        .output(subtitles_video_final, r=self.fps)
                        .run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
                    )
                except ffmpeg.Error as e:
                    print('stderr:', e.stderr.decode('utf8'))
                    print('stdout:', e.stdout.decode('utf8'))
                self.__delete_and_copy_file(subtitles_video_final, subtitles_video)
                segment = ' '
                start_segment_index = i + 1
                index += 1

        # Delete all files in folder
        files = glob.glob(subtitles_dir + "\\*")
        for f in files:
            os.remove(f)

        return subtitles_video

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

    def __create_subtitle_image(self, text, width=920, height=150):
        # Create a transparent image
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Load a font (change the path if needed)
        font = ImageFont.load_default()

        # Get the size of the text and position it in the center
        text_size = draw.textsize(text, font=font)
        text_x = (width - text_size[0]) // 2
        text_y = (height - text_size[1]) // 2

        # Draw the text with white color (or change as needed)
        draw.text((text_x, text_y), text, fill=(255, 255, 255, 255), font=font)

        return image


gppve = GamePlusPodcastVideoEditor('https://www.youtube.com/watch?v=HOhMSacJFFY', 'https://www.youtube.com/watch?v=iYipwtIa1Po', video_quality=1080)

gppve.generateVideo(0, 5)