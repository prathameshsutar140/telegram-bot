> Prathamesh:
import random
import logging
from telegram import Update, BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# 🔑 Replace with your Telegram Bot Token from @BotFather
TOKEN = "8814768605:AAGn8Hmuq0hS08FO9O-ot_cu4sOXtVdHUQk"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# In-memory database
user_data = {}

def get_user_storage(user_id):
    if user_id not in user_data:
        user_data[user_id] = {"tasks": [], "goals": []}
    return user_data[user_id]

# Preset funny/friendly responses for generic coding or work requests
CODING_RESPONSES = [
    "Arre bhai, coding ka kaam toh tujhe hi karna padega, main toh sirf tera productivity coach hoon! 😂 Main code likhne wala bot nahi hoon, bas tujhe manage karne wala.\n\nPar tension mat le, agar tu chahe toh main isse ek task ki tarah list mein add kar deta hoon! 🚀",
    "Bhai main tera supervisor hoon, coder nahi! 😜 Tu code likh, main piche se taali bajayega. Shall I add this to your task list? 🔥",
    "Aap dev ho aur main manager! 👑 Main code nahi likhta, bas ensure karta hoon ki tu kaam kare. Bata task list mein daal doon? 🚀"
]

GENERIC_FUNNY_RESPONSES = [
    "Sahi hai boss! 😎 Jo bolege wo karenge, bas mehnat tujhe karni hai!",
    "Full power mood mein lag raha hai aaj! ⚡ Bata kya scene hai?",
    "Arre wah! Second brain active hai aur tu bhi form mein lag raha hai. Let's dominate! 🏆",
    "Tension lene ka nahi, sirf dene ka! 🧠 Bolo agla task kya hai?"
]

# Configure Telegram Menu
async def post_init(application):
    commands = [
        BotCommand("tasks", "View pending tasks"),
        BotCommand("done", "Mark tasks complete"),
        BotCommand("today", "Get today's summary"),
        BotCommand("help", "View all commands"),
    ]
    await application.bot.set_my_commands(commands)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    msg = (
        f"Ayeee {name}! What's good? 😎\n"
        "Your second brain is online and ready to help you dominate! 🏆"
    )
    await update.message.reply_text(msg)

# /tasks command
async def view_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_user_storage(update.effective_user.id)
    pending = [t for t in data["tasks"] if not t["done"]]

    if not pending:
        msg = "Woohoo! 🎉 No pending tasks! You're a productivity BEAST! Time to chill or set new goals? 😎"
        await update.message.reply_text(msg)
        return

    msg = "📋 *Pending Tasks:*\n\n" + "\n".join(f"{idx}. {t['text']}" for idx, t in enumerate(pending, 1))
    await update.message.reply_markdown(msg)

# Smart Rule-Based Text Responder (No API required!)
async def smart_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    text_lower = text.lower()
    user_id = update.effective_user.id
    data = get_user_storage(user_id)

    # 1. Check if user is asking to write code / program
    if any(keyword in text_lower for keyword in ["write a program", "write code", "code likh", "program likh"]):
        # Pick a random funny reply from CODING_RESPONSES
        reply = random.choice(CODING_RESPONSES)
        # Automatically save it as a pending task so they don't forget
        data["tasks"].append({"text": f"Write program: {text}", "done": False})
        await update.message.reply_text(reply)
        return

    # 2. Check for greetings
    elif any(keyword in text_lower for keyword in ["hi", "hello", "hey", "sup", "wassup"]):
        await update.message.reply_text("Ayeee! What's up brother? 😎 Tayyar hai aaj ke tasks ke liye?")
        return

> Prathamesh:
# 3. Default behavior: Save as a task and give a funny/friendly confirmation
    else:
        data["tasks"].append({"text": text, "done": False})
        funny_note = random.choice(GENERIC_FUNNY_RESPONSES)
        await update.message.reply_text(f"📌 *Task Added:* \"{text}\"\n\n{funny_note}", parse_mode="Markdown")

if name == 'main':
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tasks", view_tasks))
    
    # Message handler that triggers smart responses without an API
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, smart_reply))

    print("🚀 Prathamesh OS (No-API Mode) is running...")
    app.run_polling()
