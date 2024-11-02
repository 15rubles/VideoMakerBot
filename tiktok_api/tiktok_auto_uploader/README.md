# TiktokAutoUploader v2.0

# Quickstart

You must have Node installed on your computer, in order to run this, 
Please follow instructions in the provided URL, 

`https://nodejs.org/en/download`

Please make sure `node` is in your environment path before running, as it is required in the upload stage. 


--------------------------------------
### Installation

Install requirements for package.

```bash
pip install -r requirements.txt
```
Install node packages.
```bash
cd tiktok_uploader/tiktok-signature/
npm i
```

### Using program in CLI:

-----------------------------------

### Login to Account 🔒:

System handles multiple user accounts logging in, and will save this to system. This will prompt you to login into your tiktok account and store these cookies locally.

> ```bash
> # Login
> 
> python cli.py login -n my_saved_username
> ```

### Upload Videos 🖼️:

Users can select user, and upload a video from path or directly from a youtube shorts link.

```bash
# Upload from videos path
python cli.py upload --user my_saved_username -v "video.mp4" -t "My video title" 
```

```bash
# Upload from youtube link
python cli.py upload --user my_saved_username -yt "https://www.youtube.com/shorts/#####" -t "My video title" 
```

--------------------------------

### Show Current Users and Videos ⚙️:

All local videos must be saved under folder `VideosDirPath` if this doesn't exist please create one.

```bash
# Show all current videos found on system.
python cli.py show -v 
```

All cookies must be saved under folder `CookiesDir`, if this doesn't exist please create one.

```bash
# Show all current cookies found on system.
python cli.py show -c 
```

-----

### Help Command ℹ️:

If you are unsure with command, use the flag `-h`

```bash
# Show all current videos found on system.
python cli.py -h
python cli.py show -h
python cli.py login -h
python cli.py upload -h
```

 ----
