import pyrogram
import os
import cv2
from pyrogram import filters


app = pyrogram.Client(
    "my_bot",
    api_id=15849735,  # Replace with your own Telegram API ID
    api_hash="b8105dc4c17419dfd4165ecf1d0bc100",  # Replace with your own Telegram API hash
    bot_token="6067171502:AAF20GwzoxblYC4yBNw8nTffRJprwgLTKi0"  # Replace with your own bot token
)

@app.on_message(filters.command(["start"]))
def start(bot, update):
    bot.send_message(chat_id=update.chat.id, text='This bot can add a watermark to your videos. Use the /set command to set the watermark.')

@app.on_message(filters.command(["set"]))
def set_watermark(bot, update):
    message = update.reply_to_message
    if message.video:
        video_path = message.download(file_name="temp_video.mp4")
        watermark_text = "@OnlyFanstash"
        video = cv2.VideoCapture(video_path)
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        while True:
            ret, frame = video.read()
            if not ret:
                break
            cv2.putText(frame, watermark_text, (width-200, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imwrite('temp_frame.jpg', frame)
            os.system(f'ffmpeg -y -i temp_frame.jpg -i "{video_path}" -map 0:0 -map 1:1 -c:v libx264 -preset ultrafast -crf 22 -c:a copy -shortest temp_output.mp4')
            os.remove('temp_frame.jpg')
            os.remove(video_path)
            if os.path.exists('temp_output.mp4'):
                os.rename('temp_output.mp4', video_path)

        video = open(video_path, 'rb')
        update.reply_video(video)
        video.close()
        os.remove(video_path)
    else:
        bot.send_message(chat_id=update.chat.id, text="Please reply to a video to add watermark.")

app.run()
