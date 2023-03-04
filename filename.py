from pyrogram import Client, filters
from pyrogram.types import Message
import os
from moviepy.editor import *

# Add your API ID, API hash, and bot token here
api_id = 15849735
api_hash = "b8105dc4c17419dfd4165ecf1d0bc100"
bot_token = "6145559264:AAEkUH_znhpaTdkbnndwP1Vy2ppv-C9Zf4o"

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Define watermark image path
watermark_file = None

# Define the watermark function
def add_watermark(video_path, output_path):
    video = VideoFileClip(video_path)
    watermark = (ImageClip(watermark_file)
                 .resize(height=video.h / 6) # You can adjust the size of the watermark here
                 .margin(right=8, top=8, opacity=0) # You can adjust the position of the watermark here
                 .set_pos(("right", "top")))
    result = CompositeVideoClip([video, watermark])
    result.write_videofile(output_path)

# Define the /start command handler
@app.on_message(filters.command("start"))
def start(client: Client, message: Message):
    message.reply_text("Hi! I can add a watermark to your videos. To get started, reply to a video with /set and upload a watermark image.")

# Define the /set command handler
@app.on_message(filters.command("set"))
def set_watermark(client: Client, message: Message):
    # Check if the message is a reply to a video
    if message.reply_to_message and message.reply_to_message.video:
        # Download the watermark image file
        global watermark_file
        watermark_file = client.download_media(
            message=message,
            file_name="watermark.png"
        )
        message.reply_text("Watermark image set successfully! You can now reply to a video with /watermark to get the watermarked video.")
    else:
        message.reply_text("Please reply to a video to set the watermark image.")

# Define the /watermark command handler
@app.on_message(filters.command("watermark"))
def watermark(client: Client, message: Message):
    # Check if the message is a reply to a video
    if message.reply_to_message and message.reply_to_message.video:
        # Download the video file
        video_file = client.download_media(
            message=message.reply_to_message,
            file_name="video.mp4"
        )

        # Generate the output file path
        output_file = os.path.join(
            "downloads",
            f"{os.path.splitext(os.path.basename(video_file))[0]}_watermarked.mp4"
        )

        # Add the watermark to the video
        add_watermark(video_file, output_file)

        # Send the watermarked video as a reply
        message.reply_video(
            video=output_file,
            quote=True
        )
    else:
        message.reply_text("Please reply to a video with /watermark to get the watermarked video.")

# Start the Pyrogram client
app.run()
