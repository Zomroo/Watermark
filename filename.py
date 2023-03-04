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
    # Download the video file
    video_file = client.download_media(
        message=message.video,
        file_name="video.mp4"
    )

    # Store the message ID to reference it later
    watermark_message_id = message.message_id

    # Ask the user to send the watermark image file
    message.reply_text("Please reply to this message with the watermark image file.")

    # Listen for the reply containing the watermark image file
    @app.on_message(filters.reply & filters.photo)
    def handle_watermark_message(client: Client, message: Message):
        # Remove the listener so that it doesn't keep running unnecessarily
        app.remove_handler(handle_watermark_message)

        # Download the watermark image file
        watermark_file = client.download_media(
            message=message.photo[-1],
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
        message.reply_video(
            video=output_file,
            quote=True
        )

    # Store the watermark message ID to reference it later
    client.set_relay_data(watermark_message_id, "watermark_message_id")

# Listen for the /set command
@app.on_message(filters.command("set"))
def handle_set_command(client: Client, message: Message):
    # Get the watermark message ID from the original message
    watermark_message_id = client.get_relay_data(message.reply_to_message.message_id, "watermark_message_id")

    # If the watermark message ID exists, delete the watermark message
    if watermark_message_id:
        client.delete_messages(message.chat.id, watermark_message_id)
        message.reply_text("Watermark image message deleted.")
    else:
        message.reply_text("No watermark image message found.")

# Start the Pyrogram client
app.run()
