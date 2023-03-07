import os
import subprocess
import telegram
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters

# Define the initial state of the conversation
TIME, DURATION = range(2)

# Define your Telegram API token
TOKEN = '6216536325:AAE4dTlIA3-8PYcJnireGCpwCqvIBLHE9Zw'

# Define the MPD link and key
MPD_LINK = "https://delta34tatasky.akamaized.net/out/i/353.mpd"
MPD_KEY = "ee4cd9845e124e188ccd0468d9400f78:f109e5b3d10644e260234aba543830dd"

# Define the function to start the conversation
def start(update, context):
    # Send a welcome message
    update.message.reply_text('Hi! Welcome to the video recorder bot.')
    # Ask for scheduling time
    update.message.reply_text('Please enter the scheduling time in 24-hour format (e.g. 18:00):')
    # Transition to the TIME state
    return TIME

# Define the function to handle the scheduling time
def time(update, context):
    # Store the scheduling time in the user's context
    context.user_data['time'] = update.message.text
    # Ask for the duration of the recording
    update.message.reply_text('Please enter the duration of the recording in minutes:')
    # Transition to the DURATION state
    return DURATION

# Define the function to handle the recording duration
def duration(update, context):
    # Store the recording duration in the user's context
    context.user_data['duration'] = update.message.text
    # Send a message indicating that the recording is starting
    update.message.reply_text('Starting recording now...')
    # Define the filename for the recorded video
    filename = 'recorded_video.mkv'
    # Use N_m3u8DL-RE to record the video
    subprocess.call(['C:/Users/mrpc/.vscode/Downloads/N_m3u8DL-RE', MPD_LINK, '-sv', 'best', '-sa', 'all', '--live-record-limit', f"0:{context.user_data['duration']}:00", '--decryption-binary-path', 'bin/tools/mp4decrypt', '--key', MPD_KEY, '--live-real-time-merge', '-M', f"format=mkv:muxer=mkvmerge:bin_path=/path/to/mkvmerge:--save-name={filename}"])
    # Send the recorded video to the user
    context.bot.send_video(chat_id=update.message.chat_id, video=open(filename, 'rb'))
    # Indicate that the recording is completed
    update.message.reply_text('Recording completed.')
    # Return to the initial state
    return ConversationHandler.END


# Define the function to handle errors
def error(update, context):
    # Print the error message
    print(f"Update {update} caused error {context.error}")

# Create the updater and dispatcher
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Define the conversation handler
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        TIME: [MessageHandler(Filters.regex('^[0-9]{2}:[0-9]{2}$'), time)],
        DURATION: [MessageHandler(Filters.regex('^[0-9]+$'), duration)]
    },
    fallbacks=[]
)

# Add the conversation handler to the dispatcher
dispatcher.add_handler(conv_handler)

# Add the error handler to the dispatcher
dispatcher.add_error_handler(error)

# Start the bot
updater.start_polling()

# Run the bot until Ctrl-C is pressed or the process receives SIGINT, SIGTERM or SIGABRT
updater.idle()
