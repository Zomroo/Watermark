import os
import pyrogram
from pyrogram import Client, filters
from pyrogram.types import Message
from moviepy.editor import *

# Replace YOUR_API_ID and YOUR_API_HASH with your Telegram API ID and API hash
api_id = 15849735
api_hash = 'b8105dc4c17419dfd4165ecf1d0bc100'

# Replace YOUR_BOT_TOKEN with your Telegram bot token
bot_token = '6145559264:AAEkUH_znhpaTdkbnndwP1Vy2ppv-C9Zf4o'

# Create a Pyrogram client instance
app = Client('my_bot', api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Handle the /start command
@app.on_message(filters.command('start'))
def start_command(client, message):
    text = "Hello! I'm a bot that can add text to the top right corner of a video. To use me, reply to a video with /set command and then I will add the text @OnlyFanstash to the top right corner of the video."
    client.send_message(message.chat.id, text)

# Handle the /set command
@app.on_message(filters.video & filters.reply)
def set_command(client, message):
    video_file = message.reply_to_message.video.file_id
    video_path = client.download_media(message.reply_to_message)
    video = VideoFileClip(video_path)

    # Add text to the video
    txt_clip = TextClip("@OnlyFanstash", fontsize=70, color='white', stroke_width=2).set_position(('right','top')).set_duration(video.duration)
    result = CompositeVideoClip([video, txt_clip])

    # Save the video file
    result_path = 'output.mp4'
    result.write_videofile(result_path)

    # Send the video file to the user
    client.send_video(message.chat.id, result_path)

    # Delete the temporary files
    os.remove(video_path)
    os.remove(result_path)

# Start the bot
app.run()
