import telegram
import os
import cv2

bot = telegram.Bot(token='6067171502:AAF20GwzoxblYC4yBNw8nTffRJprwgLTKi0')

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='This bot can add a watermark to your videos. Use the /set command to set the watermark.')

def set_watermark(update, context):
    video_file = context.bot.getFile(update.message.video.file_id)
    video_path = 'temp_video.mp4'
    video_file.download(video_path)

    watermark_text = '@OnlyFanstash'
    video = cv2.VideoCapture(video_path)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    while True:
        ret, frame = video.read()
        if not ret:
            break
        cv2.putText(frame, watermark_text, (width-200, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imwrite('temp_frame.jpg', frame)
        os.system('ffmpeg -y -i temp_frame.jpg -i ' + video_path + ' -map 0:0 -map 1:1 -c:v libx264 -preset ultrafast -crf 22 -c:a copy -shortest temp_output.mp4')
        os.remove('temp_frame.jpg')
        os.remove(video_path)
        os.rename('temp_output.mp4', video_path)

    context.bot.send_video(chat_id=update.effective_chat.id, video=open(video_path, 'rb'))

def main():
    updater = telegram.ext.Updater(token='your_bot_token_here', use_context=True)

    updater.dispatcher.add_handler(telegram.ext.CommandHandler('start', start))
    updater.dispatcher.add_handler(telegram.ext.CommandHandler('set', set_watermark, pass_args=True))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
