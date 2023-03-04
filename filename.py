from pyrogram import Client, filters
from pyrogram.types import Message

import os
import requests
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

app = Client("my_bot_token", api_id=12345, api_hash="my_api_hash")

# Define a function to add watermark to the video
def add_watermark(video_path, watermark_text):
    # Load the video clip
    video_clip = VideoFileClip(video_path)

    # Create a TextClip for the watermark
    watermark = TextClip(watermark_text, fontsize=20, color='white', font='Arial-Bold')

    # Add the watermark to the top right corner of the video clip
    watermark_clip = watermark.set_position(('right', 'top')).set_duration(video_clip.duration)

    # Composite the watermark with the video clip
    final_clip = CompositeVideoClip([video_clip, watermark_clip])

    # Export the composite video as a streamable file
    output_file = os.path.splitext(video_path)[0] + '_watermarked.mp4'
    final_clip.write_videofile(output_file, codec='libx264', preset='medium', bitrate='5000k', audio_codec='aac', fps=video_clip.fps, threads=4)

    return output_file

# Define a handler function for the /start command
@app.on_message(filters.command('start'))
def start_handler(client: Client, message: Message):
    response = "Hi! I'm a bot that can add a watermark to your video files. Just send me a video file and use the /set command to add a watermark."
    message.reply_text(response)

# Define a handler function for the /set command
@app.on_message(filters.command('set'))
def set_handler(client: Client, message: Message):
    # Check if the message has a video
    if message.video is None:
        message.reply_text("Please send a video file.")
        return

    # Download the video file
    video_path = client.download_media(message.video)

    # Add the watermark to the video
    watermark_text = '@OnlyFanstash'
    output_file = add_watermark(video_path, watermark_text)

    # Upload the watermarked video as a streamable file
    response = requests.post('https://api.streamable.com/upload', files={'file': open(output_file, 'rb')}, auth=('my_streamable_username', 'my_streamable_password'))
    video_url = 'https://streamable.com/' + response.json()['shortcode']

    # Reply to the message with the watermarked video URL
    message.reply_text(video_url)

if __name__ == '__main__':
    app.run()
