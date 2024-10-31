from telethon import TelegramClient
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from datetime import datetime

# Replace with your own values
api_id = '12834603'
api_hash = '84a5daf7ac334a70b3fbd180616a76c6'
bot_token = '6996568724:AAFrjf88-0uUXJumDiuV6CbVuXCJvT-4KbY'

client = TelegramClient('session_name', api_id, api_hash)

async def get_group_age(group_username):
    try:
        group = await client.get_entity(group_username)
        creation_date = group.date
        current_date = datetime.now()
        age_years = (current_date - creation_date).days // 365
        return f'The group "{group.title}" is approximately {age_years} years old.'
    except Exception as e:
        return str(e)

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Send /age <group_username> to check the group age.')

def age(update: Update, context: CallbackContext):
    if len(context.args) < 1:
        update.message.reply_text('Please provide a group username.')
        return
    
    group_username = context.args[0]
    
    # Call the async function
    age_info = client.loop.run_until_complete(get_group_age(group_username))
    update.message.reply_text(age_info)

def main():
    updater = Updater(bot_token)
    
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('age', age))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    with client:
        main()
