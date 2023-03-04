from pyrogram import Client, filters
from pyrogram.types import Message
import psutil
import time

# Enter your API ID and Hash obtained from Telegram
api_id = 15849735
api_hash = 'b8105dc4c17419dfd4165ecf1d0bc100'
bot_token = '6145559264:AAEkUH_znhpaTdkbnndwP1Vy2ppv-C9Zf4o'

app = Client("status", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Start command to initiate the status update
@app.on_message(filters.command('status'))
async def status(_, message: Message):
    await message.reply("Fetching status...")

    while True:
        # Get CPU and RAM usage
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent

        # Send a message with the usage stats
        await app.send_message(
            message.chat.id,
            f"CPU: {cpu_usage}%\nRAM: {ram_usage}%"
        )

        # Wait for 1 second before sending the next update
        time.sleep(1)

# Start the bot
app.run()
