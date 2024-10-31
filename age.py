from telethon import TelegramClient, errors
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime, timezone

# Replace with your own values
api_id = '12834603'
api_hash = '84a5daf7ac334a70b3fbd180616a76c6'
bot_token = '6996568724:AAFrjf88-0uUXJumDiuV6CbVuXCJvT-4KbY'

client = TelegramClient('session_name', api_id, api_hash)

async def get_group_age(group_identifier):
    try:
        # Convert the identifier to an integer if it's a valid ID
        if group_identifier.startswith('-') or group_identifier.isdigit():
            group_identifier = int(group_identifier)

        # Get the group entity using either username or ID
        group = await client.get_entity(group_identifier)
        creation_date = group.date

        # Ensure both datetimes are aware
        current_date = datetime.now(timezone.utc)

        # Calculate the age in years
        age_years = (current_date - creation_date).days // 365
        
        # Format the creation date
        creation_date_str = creation_date.strftime('%Y-%m-%d %H:%M:%S')

        return (f'The group "{group.title}" was created on {creation_date_str} '
                f'and is approximately {age_years} years old.')
    except errors.FloodWait as e:
        return f"Please wait for {e.seconds} seconds before trying again."
    except (errors.ChannelPrivate, errors.ChannelInvalid, errors.UserNotParticipant) as e:
        return "The bot cannot access this group. Please ensure it is a member."
    except ValueError:
        return "Invalid group ID or username."
    except Exception as e:
        return f"An error occurred: {str(e)}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Send /age <group_id_or_username> to check the group age.')

async def age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 1:
        await update.message.reply_text('Please provide a group ID or username.')
        return
    
    group_identifier = context.args[0]
    
    # Call the async function
    age_info = await get_group_age(group_identifier)
    await update.message.reply_text(age_info)

def main():
    app = ApplicationBuilder().token(bot_token).build()
    
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('age', age))
    
    app.run_polling()

if __name__ == '__main__':
    with client:
        main()
