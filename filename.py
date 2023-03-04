from pyrogram import Client, filters
from pyrogram.types import Message
import os
from moviepy.editor import *

# Add your API ID, API hash, and bot token here
api_id = 12345
api_hash = "0123456789abcdef0123456789abcdef"
bot_token = "1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


# Define the watermark function
def add_watermark(video_path, watermark_path, output_path):
    video = VideoFileClip(video_path)
    watermark = (ImageClip(watermark_path)
                 .resize(height=video.h / 6) # You can adjust the size of the watermark here
                 .margin(right=8, top=8, opacity=0) # You can adjust the position of the watermark here
                 .set_pos(("right", "top")))
    result = CompositeVideoClip([video, watermark])
    result.write_videofile(output_path)

# Define the message handler function
@app.on_message(filters.video & ~filters.forwarded)
def handle_message(client: Client, message: Message):
    if message.text and message.text.startswith("/set"):
        watermark_file = client.download_media(
            message=message.reply_to_message,
            file_name="watermark.png"
        )
        message.reply_text("Watermark set successfully!")
    else:
        # Download the video file
        video_file = client.download_media(
            message=message.video,
            file_name="video.mp4"
        )

        # Check if a watermark has been set
        if os.path.exists("watermark.png"):
            watermark_file = "watermark.png"
        else:
            # If no watermark has been set, use a default watermark
            watermark_file = "default_watermark.png"

        # Generate the output file path
        output_file = os.path.join(
            "downloads",
            f"{os.path.splitext(os.path.basename(video_file))[0]}_watermarked.mp4"
        )

        # Add the watermark to the video
        add_watermark(video_file, watermark_file, output_file)

        # Send the watermarked video as a reply
        message.reply_video(
            video=output_file,
            quote=True
        )

# Start the Pyrogram client
app.run()
