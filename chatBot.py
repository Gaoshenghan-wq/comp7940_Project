from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          CallbackContext)
import logging
import os

from ChatGPT_HKBU_ENV import HKBU_ChatGPT

def equipped_chatgpt(update, context):
    global chatgpt
    reply_message = chatgpt.submit(update.message.text)
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

def main():
    # Load configuration from environment variables
    telegram_access_token = os.getenv("TELEGRAM_ACCESS_TOKEN")
    chatgpt_base_url = os.getenv("CHATGPT_BASE_URL")
    chatgpt_model_name = os.getenv("CHATGPT_MODEL_NAME")
    chatgpt_api_version = os.getenv("CHATGPT_API_VERSION")
    chatgpt_access_token = os.getenv("CHATGPT_ACCESS_TOKEN")

    print(123)
    # Create an Updater for your Bot
    updater = Updater(token=telegram_access_token, use_context=True)
    dispatcher = updater.dispatcher


    # Set up logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    # Initialize ChatGPT instance
    global chatgpt
    chatgpt = HKBU_ChatGPT()

    # Register handlers
    chatgpt_handler = MessageHandler(Filters.text & (~Filters.command), equipped_chatgpt)
    dispatcher.add_handler(chatgpt_handler)

    # Command handlers
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("hello", hello))
    dispatcher.add_handler(CommandHandler("anzureConnect", gitFly))

    # Start the bot
    updater.start_polling()
    updater.idle()

def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Helping you helping you.')

def hello(update: Update, context: CallbackContext) -> None:
    try:
        name = context.args[0]  # Get the name from the command argument
        update.message.reply_text(f"Good day, {name}!")
    except IndexError:
        update.message.reply_text("Usage: /hello <name>")

def gitFly(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f"anzure connect success!")


if __name__ == '__main__':
    main()