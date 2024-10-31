from telethon import TelegramClient
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime, timezone

# Replace with your own values
api_id = '12834603'
api_hash = '84a5daf7ac334a70b3fbd180616a76c6'
bot_token = '6996568724:AAFrjf88-0uUXJumDiuV6CbVuXCJvT-4KbY'

client = TelegramClient('session_name', api_id, api_hash)

async def get_group_age(group_username):
    try:
        group = await client.get_entity(group_username)
        creation_date = group.date

        # Ensure both datetimes are aware
        current_date = datetime.now(timezone.utc)

        # Calculate the age in years
        age_years = (current_date - creation_date).days // 365
        
        # Format the creation date
        creation_date_str = creation_date.strftime('%Y-%m-%d %H:%M:%S')

        return (f'The group "{group.title}" was created on {creation_date_str} '
                f'and is approximately {age_years} years old.')
    except Exception as e:
        return str(e)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Send /age <group_username> to check the group age.')

async def age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 1:
        await update.message.reply_text('Please provide a group username.')
        return
    
    group_username = context.args[0]
    
    # Call the async function
    age_info = await get_group_age(group_username)
    await update.message.reply_text(age_info)

def main():
    app = ApplicationBuilder().token(bot_token).build()
    
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('age', age))
    
    app.run_polling()

if __name__ == '__main__':
    with client:
        main()
