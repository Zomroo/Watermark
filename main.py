import os
import asyncio
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message
from moviepy.editor import *
from aiohttp import web

# Replace YOUR_API_ID and YOUR_API_HASH with your Telegram API ID and API hash
api_id = 15849735
api_hash = 'b8105dc4c17419dfd4165ecf1d0bc100'

# Replace YOUR_BOT_TOKEN with your Telegram bot token
bot_token = '6145559264:AAEkUH_znhpaTdkbnndwP1Vy2ppv-C9Zf4o'

# Set the Heroku port number
PORT = int(os.environ.get('PORT', 5000))

# Create a Pyrogram client instance
app = Client('my_bot', api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Define a web server endpoint
async def web_server():
    async def handler(_):
        return web.Response(text='Hello, world')
    app = web.Application()
    app.add_routes([web.get('/', handler)])
    return app

# Define a web response endpoint
async def web_response():
    runner = web.AppRunner(await web_server())
    await runner.setup()
    bind_address = "0.0.0.0"
    site = web.TCPSite(runner, bind_address, PORT)
    await site.start()

# Start the web server
loop = asyncio.get_event_loop()
loop.create_task(web_response())

# Handle the /start command
@app.on_message(filters.command('start'))
async def start_command(client, message):
    text = "Hello! I'm a bot that can add text to the top right corner of a video. To use me, reply to a video with /set command and then I will add the text @OnlyFanstash to the top right corner of the video."
    await client.send_message(message.chat.id, text)

# Handle the /set command
@app.on_message(filters.video & filters.reply)
async def set_command(client, message):
    video_file = message.reply_to_message.video.file_id
    video_path = await client.download_media(message.reply_to_message)
    video = VideoFileClip(video_path)

    # Add text to the video
    txt_clip = TextClip("@OnlyFanstash", fontsize=70, color='white', stroke_width=2).set_position(('right','top')).set_duration(video.duration)
    result = CompositeVideoClip([video, txt_clip])

    # Save the video file
    result_path = 'output.mp4'
    result.write_videofile(result_path)

    # Send the video file to the user
    await client.send_video(message.chat.id, result_path)

    # Delete the temporary files
    os.remove(video_path)
    os.remove(result_path)

# Start the bot
async def main():
    await app.start()
    await app.idle()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
