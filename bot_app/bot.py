from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

import bot_data
import bar_serch

updater = Updater(token = bot_data.token, use_context=True)

dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

class Bot:
    def __init__(self):
        self.bar_serch = bar_serch.Bar_serch()


    def start(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text= 'Сейчас мы пройдемся по барам пришли свою геолокацию\nя буду предлагать')


    def mesag(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text='Так я тебя не понимаю...')

    def location(self, update, context):
        loc_data = update.message.effective_attachment
        self.bars = self.bar_serch.serch(loc_data.latitude, loc_data.longitude)
        self.get_bar_(update, context)

    def button_next(self, update, context):
        if 'bars'  in self.__dict__.keys():
            self.get_bar_(update, context)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text='Не заню где ты', parse_mode='Markdown', disable_notification=False)


    def get_bar_(self, update, context):
        bar = self.bars.get_bar()
        if str(type(bar)) == "<class 'NoneType'>":
            mes = 'Похоже баров тут больше нет'
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=mes, parse_mode='Markdown', disable_notification=False)
            return None
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
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='И так!', reply_markup=reply_markup,
                                 disable_notification = False)




bot = Bot()
start_handler = CommandHandler('start', bot.start)
mesag_handler = MessageHandler(Filters.text & (~Filters.command) & (~Filters.location), bot.mesag)
location_handler = MessageHandler(Filters.location, bot.location)
next_bar_handler = CallbackQueryHandler(bot.button_next, pattern = "1")
stop_bar_handler = CallbackQueryHandler(bot.start, pattern = "2")


dispatcher.add_handler(start_handler)
dispatcher.add_handler(mesag_handler)
dispatcher.add_handler(location_handler)
dispatcher.add_handler(next_bar_handler)
dispatcher.add_handler(stop_bar_handler)
updater.start_polling()