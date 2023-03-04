import os
from pyrogram import Client, filters
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.VideoClip import TextClip

# API credentials
API_ID = os.environ.get("15849735")
API_HASH = os.environ.get("b8105dc4c17419dfd4165ecf1d0bc100")
BOT_TOKEN = os.environ.get("6145559264:AAEkUH_znhpaTdkbnndwP1Vy2ppv-C9Zf4o")

# Create the Pyrogram client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


def add_watermark(video_file, output_file, watermark_text):
    """Adds a watermark to a video file."""
    video = VideoFileClip(video_file)

    # Add watermark text to the video
    txt_clip = TextClip(watermark_text, fontsize=30, color='white').set_position("bottom")
    result = CompositeVideoClip([video, txt_clip])

    # Save the watermarked video
    result.write_videofile(output_file)


@app.on_message(filters.video & filters.reply)
def set_watermark(client, message):
    """Sets the watermark for the bot."""
    video_file = client.download_media(message.reply_to_message)
    watermark_text = "@OnlyFanstash"
    output_file = "watermarked_" + os.path.basename(video_file)
    add_watermark(video_file, output_file, watermark_text)
    message.reply_video(output_file)


if __name__ == "__main__":
    app.run()
