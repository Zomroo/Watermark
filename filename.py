from pyrogram import Client, filters
from pyrogram.types import Message
import os
import logging
import logging
logging.basicConfig(filename='myapp.log', level=logging.DEBUG)

# Set up the logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a Pyrogram client instance
api_id = 15849735
api_hash = 'b8105dc4c17419dfd4165ecf1d0bc100'
bot_token = '6145559264:AAEkUH_znhpaTdkbnndwP1Vy2ppv-C9Zf4o'
port = int(os.environ.get('PORT', 5000))
app = Client('my_bot', api_id, api_hash, bot_token=bot_token)

# Log the "I am alive" message
logging.info('I am alive')
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
        # Upload the modified video and save the sent message
        sent_msg = client.send_video(message.chat.id, 'output.mp4', supports_streaming=True)
        # Delete the downloaded and modified video files
        os.remove(video)
        os.remove('output.mp4')
    else:
        # Send an error message if the replied message is not a video
        client.send_message(message.chat.id, 'Please reply to a video with the /set command.')

# Define a command handler for the /status command
@app.on_message(filters.command('status'))
def status_command_handler(client, message):
    # Check if the replied message is the modified video sent by the bot
    if message.reply_to_message.video and message.reply_to_message.video.file_name == 'output.mp4':
        # Get the size of the modified video file
        output_size = os.path.getsize('output.mp4')
        # Get the size of the video file sent by the bot
        sent_size = message.reply_to_message.video.file_size
        # Calculate the upload progress
        progress = round(sent_size / output_size * 100)
        # Send the status message
        status_message = f"Video upload status: {sent_size} bytes ({progress}% done)"
        client.send_message(message.chat.id, status_message)
    else:
        # Send an error message if the replied message is not the modified video sent by the bot
        client.send_message(message.chat.id, 'Please reply to the modified video sent by the bot with the /status command.')
        pass  # add this line to indicate that there is no code to be executed in this block
        
# Start
if __name__ == '__main__':
    app.run()  # Run the Pyrogram client
