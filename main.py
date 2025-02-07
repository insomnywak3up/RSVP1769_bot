from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

TOKEN = "8042742527:AAFf694R7VSPd3C4GwAc7jmjWM5cgAJBUVk"

app = Application.builder().token(TOKEN).build()
events = {}

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Welcome to the RSVP Bot! Type /createevent to create a new event.")

async def create_event(update: Update, context: CallbackContext):
    event_id = len(events) + 1
    events[event_id] = {"name": "", "date": "", "location": ""}  # Пустые данные

    await update.message.reply_text("Enter the event name:")
    context.user_data["event_id"] = event_id  # Сохраняем ID события

async def event_name(update: Update, context: CallbackContext):
    event_id = context.user_data.get("event_id")
    if not event_id:
        return await update.message.reply_text("Please start with /createevent.")

    events[event_id]["name"] = update.message.text
    await update.message.reply_text("Enter the event date (YYYY-MM-DD):")

    context.user_data["next_step"] = "event_date"  # Переход к следующему шагу

async def event_date(update: Update, context: CallbackContext):
    event_id = context.user_data.get("event_id")
    if not event_id:
        return

    events[event_id]["date"] = update.message.text
    await update.message.reply_text("Enter the event location:")

    context.user_data["next_step"] = "event_location"

async def event_location(update: Update, context: CallbackContext):
    event_id = context.user_data.get("event_id")
    if not event_id:
        return

    events[event_id]["location"] = update.message.text

    keyboard = [[InlineKeyboardButton("RSVP Here", url=f"https://t.me/RSVP1769_bot?start={event_id}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Event created! Share the RSVP link:", reply_markup=reply_markup)

def handle_message(update: Update, context: CallbackContext):
    next_step = context.user_data.get("next_step")
    if next_step == "event_date":
        return event_date(update, context)
    elif next_step == "event_location":
        return event_location(update, context)
    return event_name(update, context)

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("createevent", create_event))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Бот started ismail!")
app.run_polling()
