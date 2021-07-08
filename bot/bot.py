from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import bot_data
import bar_serch

updater = Updater(token = bot_data.token, use_context=True)

dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text= 'Сейчас мы пройдемся по барам пришли свою геолокацию')


def mesag(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Ты пидор')

def location(update, context):
    loc_data = update.message.effective_attachment

    serch = bar_serch.Bar_serch(loc_data.latitude, loc_data.longitude)
    msg = serch.serch()
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=msg, parse_mode = 'Markdown',
                             location = serch.location)

    print('геолокация')



start_handler = CommandHandler('start', start)
mesag_handler = MessageHandler(Filters.text & (~Filters.command) & (~Filters.location), mesag)
location_handler = MessageHandler(Filters.location, location)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(mesag_handler)
dispatcher.add_handler(location_handler)

updater.start_polling()