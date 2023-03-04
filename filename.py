from pyrogram import Client, filters
from pyrogram.types import Message
import os

# Create a Pyrogram client instance
api_id = 15849735
api_hash = '15849735'
bot_token = '6145559264:AAEkUH_znhpaTdkbnndwP1Vy2ppv-C9Zf4o'
app = Client('my_bot', api_id, api_hash, bot_token=bot_token)

# Define a command handler for the /start command
@app.on_message(filters.command('start'))
def start_command_handler(client, message):
    # Send a welcome message
    client.send_message(message.chat.id, 'Hi! I am a bot that can add text to the top right corner of a video. '
                                         'Send me a video file and reply to it with the /set command to add text.')

# Define a command handler for the /set command
@app.on_message(filters.command('set') & filters.reply)
def set_command_handler(client, message):
    # Check if the replied message is a video
    if message.reply_to_message.video:
        # Download the video file
        video = client.download_media(message.reply_to_message.video)
        # Add the text to the top right corner of the video using ffmpeg
        os.system(f'ffmpeg -i "{video}" -vf "drawtext=text=@OnlyFanstash:x=w-tw-10:y=10:fontsize=20:fontcolor=white:box=1:boxcolor=black@0.5" -c:a copy output.mp4')
        # Upload the modified video
        client.send_video(message.chat.id, 'output.mp4', supports_streaming=True)
        # Delete the downloaded and modified video files
        os.remove(video)
        os.remove('output.mp4')
    else:
        # Send an error message if the replied message is not a video
        client.send_message(message.chat.id, 'Please reply to a video with the /set command.')

# Start the Pyrogram client
app.run()
