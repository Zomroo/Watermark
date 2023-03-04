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

# Dictionary to store messages with video files
message_dict = {}

# Define the message handler function
@app.on_message(filters.video & ~filters.forwarded)
def handle_message(client: Client, message: Message):
    # Store the message in the dictionary with the video file ID as the key
    message_dict[message.video.file_id] = message

# Define the /set command handler function
@app.on_command("set")
def handle_set(client: Client, message: Message):
    # Retrieve the original message from the dictionary using the video file ID
    original_message = message_dict.get(message.reply_to_message.video.file_id)
    if original_message is None:
        # If the original message is not found, send an error message
        message.reply_text("Please reply to a video message that you want to add a watermark to with /set.")
    else:
        # Download the video file
        video_file = client.download_media(
            message=original_message.video,
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

        # Send the watermarked video as a reply to the original message
        original_message.reply_video(
            video=output_file,
            quote=True
        )

# Start the Pyrogram client
app.run()
