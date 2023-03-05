from pyrogram import Client, filters
from pyrogram.types import Message
import os
import logging

# Set up the logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a Pyrogram client instance
api_id = int(os.environ.get('API_ID'))
api_hash = os.environ.get('API_HASH')
bot_token = os.environ.get('BOT_TOKEN')
port = int(os.environ.get('PORT', 5000))
app = Client('my_bot', api_id, api_hash, bot_token=bot_token)

# Define an error handler for all exceptions
@app.on_error()
async def handle_error(client, exception):
    logging.exception(exception)
    await client.send_message(chat_id='your_chat_id', text='An error occurred. Please try again later.')

# Log the "I am alive" message
logging.info('I am alive')

# Define a command handler for the /start command
@app.on_message(filters.command('start'))
async def start_command_handler(client, message):
    # Send a welcome message
    await client.send_message(message.chat.id, 'Hi! I am a bot that can add text to the top right corner of a video. '
                                         'Send me a video file and reply to it with the /set command to add text.')

# Define a command handler for the /set command
@app.on_message(filters.command('set') & filters.reply)
async def set_command_handler(client, message):
    # Check if the replied message is a video
    if message.reply_to_message.video:
        # Download the video file
        video = await client.download_media(message.reply_to_message.video)
        # Add the text to the top right corner of the video using ffmpeg
        os.system(f'ffmpeg -i "{video}" -vf "drawtext=text=@OnlyFanstash:x=w-tw-10:y=10:fontsize=20:fontcolor=white:box=1:boxcolor=black@0.5" -c:a copy output.mp4')
        # Upload the modified video and save the sent message
        sent_msg = await client.send_video(message.chat.id, 'output.mp4', supports_streaming=True)
        # Delete the downloaded and modified video files
        os.remove(video)
        os.remove('output.mp4')
    else:
        # Send an error message if the replied message is not a video
        await client.send_message(message.chat.id, 'Please reply to a video with the /set command.')

# Define a command handler for the /status command
@app.on_message(filters.command('status'))
async def status_command_handler(client, message):
    # Check if the bot is running
    await client.send_message(message.chat.id, 'I am alive and ready to watermark your videos! Send me a video file and '
                                               'reply to it with the /set command to add text.')

# Define a command handler for the second /start command
@app.on_message(filters.command('start'))
async def start_command_handler(client, message):
    # Send a welcome message
    await client.send_message(message.chat.id, 'Hi! I am a bot that can add text to the top right corner of a video. '
                                         'Send me a video file and reply to it with the /set command to add text.')

# Start the Pyrogram client
app.run()
