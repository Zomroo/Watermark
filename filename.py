import os
import datetime
from pyrogram import Client, filters
from pyrogram.types import Message
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

# Create a Pyrogram client
app = Client("my_bot")


# Define a function to add a watermark to the video
def set_watermark(video_path: str, watermark_text: str) -> str:
    video = VideoFileClip(video_path)
    text_clip = (TextClip(watermark_text, fontsize=24, color='white', font='Arial-Bold')
                 .set_position(('center', 30))
                 .set_duration(video.duration))
    result = CompositeVideoClip([video, text_clip])
    output_path = os.path.join("downloads", f"watermarked_{os.path.basename(video_path)}")
    result.write_videofile(output_path)
    video.close()
    result.close()
    os.remove(video_path)
    return output_path


# Handle incoming messages
@app.on_message(filters.command("start"))
async def start_handler(_: Client, message: Message):
    await message.reply_text("Hello! Send me a video and I'll add a watermark to it.")


# Handle incoming messages with videos
@app.on_message(filters.video & ~filters.edited_channel)
async def video_handler(_: Client, message: Message):
    # Download the video
    video_path = await message.download()

    # Add watermark to the video
    watermark_text = f"Added by @{(await app.get_me()).username} on {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
    watermarked_video_path = set_watermark(video_path, watermark_text)

    # Send the watermarked video
    await message.reply_video(video=watermarked_video_path)

# Run the client until Ctrl+C is pressed
app.run()
