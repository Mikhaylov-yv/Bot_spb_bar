from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import bot_data
import bar_serch

updater = Updater(token = bot_data.token, use_context=True)

dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

class Bot:
    def start(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text= 'Сейчас мы пройдемся по барам пришли свою геолокацию\nя пришлю тебе 5 мест поблизости')


    def mesag(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text='Ты пидор')

    def location(self, update, context):
        loc_data = update.message.effective_attachment

        serch = bar_serch.Bar_serch(loc_data.latitude, loc_data.longitude)

        self.bars = serch.serch()
        self.get_bar(update, context)



    def get_bar(self, update, context):
        bar = self.bars.get_bar()
        name = bar['name']
        review = bar['review']
        latitude = bar['geometry.location.lat']
        longitude = bar['geometry.location.lng']
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=name, parse_mode='Markdown', disable_notification = False)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=review, parse_mode='Markdown', disable_notification=False)
        context.bot.sendLocation(chat_id=update.effective_chat.id,
                                 latitude = latitude, longitude = longitude, disable_notification = False)

        keyboard = [[
                InlineKeyboardButton("Еще!!!", callback_data='1'),
                InlineKeyboardButton("Идем сюда", callback_data='2'),
                ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('И так!', reply_markup=reply_markup, disable_notification = False)



bot = Bot()
start_handler = CommandHandler('start', bot.start)
mesag_handler = MessageHandler(Filters.text & (~Filters.command) & (~Filters.location), bot.mesag)
location_handler = MessageHandler(Filters.location, bot.location)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(mesag_handler)
dispatcher.add_handler(location_handler)

updater.start_polling()