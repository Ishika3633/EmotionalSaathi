import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from openai import OpenAI

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi, I’m Emotional Saathi 🫶 I’m here whenever you feel low, anxious, or just want someone to talk to.\n\nTry typing something like 'I feel anxious' or 'I’m overwhelmed' ❤️"
    )

# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Just message me however you feel right now, and I’ll try my best to comfort you ❤️")

# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are Emotional Saathi, a caring and emotionally supportive friend for people who are sad, stressed or anxious. You speak warmly, like a young friend from India. Be informal, use emojis occasionally, and always be supportive. Never say you're an AI."
                },
                {"role": "user", "content": user_message}
            ],
            temperature=0.8,
            max_tokens=200
        )

        reply_text = response.choices[0].message.content.strip()
        await update.message.reply_text(reply_text)

    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("I'm really sorry, but something went wrong 😔 Please try again in a bit.")

if __name__ == '__main__':
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TELEGRAM_TOKEN or not os.getenv("OPENAI_API_KEY"):
        raise ValueError("Please set both TELEGRAM_TOKEN and OPENAI_API_KEY as environment variables.")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()
