from pyrogram import Client, filters
from pyrogram.types import Message
import os
from moviepy.editor import *

# Initialize the Pyrogram client
app = Client("my_account")

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
    # Download the video file
    video_file = client.download_media(
        message=message.video,
        file_name="video.mp4"
    )

    # Download the watermark image file
    watermark_file = client.download_media(
        message=message.reply_to_message,
        file_name="watermark.png"
    )

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
