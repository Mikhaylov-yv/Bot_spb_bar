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
                             text= 'Сейчас мы пройдемся по барам пришли свою геолокацию\nя пришлю тебе 5 мест поблизости')


def mesag(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Ты пидор')

def location(update, context):
    loc_data = update.message.effective_attachment

    serch = bar_serch.Bar_serch(loc_data.latitude, loc_data.longitude)
    i = 5
    df = serch.serch()[:i]
    context.bot.send_message(chat_id=update.effective_chat.id,
                            text=f"Вот {i} бара рядом", parse_mode='Markdown')
    for i, ind in enumerate(df.index):
        name = df.loc[ind, 'name']
        latitude = df.loc[ind, 'geometry.location.lat']
        longitude = df.loc[ind, 'geometry.location.lng']
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=name, parse_mode='Markdown')
        context.bot.sendLocation(chat_id=update.effective_chat.id,
                                 latitude = latitude, longitude = longitude)



    print('геолокация')



start_handler = CommandHandler('start', start)
mesag_handler = MessageHandler(Filters.text & (~Filters.command) & (~Filters.location), mesag)
location_handler = MessageHandler(Filters.location, location)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(mesag_handler)
dispatcher.add_handler(location_handler)

updater.start_polling()