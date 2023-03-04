import os
import pyrogram
from pyrogram import Client, filters
from pyrogram.types import Message

# Create a Pyrogram client instance
app = Client("my_bot")


# Filter for video messages
video_filter = filters.video & ~filters.edited


# Function to set watermark on video
def set_watermark(video_path):
    # Get the filename and extension
    filename, extension = os.path.splitext(video_path)

    # Set the path for the output file
    output_path = f"{filename}_watermarked{extension}"

    # Set the command to add the watermark
    command = f"ffmpeg -i {video_path} -i watermark.png -filter_complex 'overlay=10:10' {output_path}"

    # Run the command
    os.system(command)

    # Remove the original file
    os.remove(video_path)

    # Rename the watermarked file to the original filename
    os.rename(output_path, video_path)


# Handler function for video messages
@app.on_message(video_filter)
async def watermark_video(client: Client, message: Message):
    # Download the video
    video_path = await message.download(file_name="temp_video.mp4")

    # Set the watermark on the video
    set_watermark(video_path)

    # Send the watermarked video
    await message.reply_video(video_path)

    # Remove the video file from the server
    os.remove(video_path)


# Run the client
app.run()
