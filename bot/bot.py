from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import bot_data as bot_data

updater = Updater(token = bot_data.token, use_context=True)

dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text= 'Пришлите мне ваше фото, я попробую определить есть ли там бобёр')


def mesag(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Ты пидор')



start_handler = CommandHandler('start', start)
mesag_handler = MessageHandler(Filters.text & (~Filters.command), mesag)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(mesag_handler)

updater.start_polling()