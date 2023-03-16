from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, CallbackContext)
from telegram import Update
# The messageHandler is used for all message updates
import os
import logging
import redis

global redis1


def main():
    # Load your token and create an Updater for your Bot
    updater = Updater(token=(os.environ['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    global redis1
    redis1 = redis.Redis(host=os.environ['HOST'],
                         password=os.environ['PASSWORD'],
                         port=os.environ['REDISPORT'])

    # register a dispatcher to handle message: here we register an echo dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)

    dispatcher.add_handler(echo_handler)
    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("hello", hello))

    # To start the bot:
    updater.start_polling()
    updater.idle()


def echo(update: Update, context: CallbackContext):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=reply_message)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Helping you helping you.')


def add(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try:
        global redis1
        logging.info(f"/add:{context.args[0]}")
        msg = context.args[0]  # /add keyword <-- this should store the keyword
        redis1.incr(msg)
        update.message.reply_text(
            f'You have said {msg} for {redis1.get(msg).decode("UTF-8")} times.')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')


def hello(update: Update, context: CallbackContext) -> None:
    message = update.message.text.removeprefix("/hello").strip()
    update.message.reply_text(f'Good day, {message}!')


if __name__ == "__main__":
    main()


"""

redis-cli -u redis://default:4EMvLLWOAKiuO9BkyIMUPHnvH15mgbzu@redis-19618.c292.ap-southeast-1-1.ec2.cloud.redislabs.com:19618

"""
