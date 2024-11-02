from tiktok_api.tiktok_auto_uploader.tiktok_uploader import tiktok


# Namespace(subcommand='upload', users='shortvideos799',
# video='D:\\Github_repositories\\DoomScrolingBot\\video_editor\\downloaded_files\\output_videos\\output_video_name_0.mp4',
# youtube=None, title='My video title', schedule=0, comment=1, duet=0, stitch=0, visibility=0,
# brandorganic=0, brandcontent=0, ailabel=0, proxy='')


def upload_video(username, video_path, title, allow_comments=1, schedule_time=0, allow_duet=0,
                 allow_stitch=0, visibility_type=0, brand_organic_type=0,
                 branded_content_type=0, ai_label=0, proxy=None):
    tiktok.upload_video(username, video_path, title, schedule_time, allow_comments, allow_duet, allow_stitch,
                        visibility_type, brand_organic_type, branded_content_type, ai_label, proxy)

def login_to_tiktok_account(username):
    tiktok.login(username)