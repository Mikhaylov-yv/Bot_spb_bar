import sh
sh.git.pull('origin')


import sys
sys.path.append('bot_app')
while True:
    try:
        import bot_app.bot
    except:
        print('Какая-то ошибка')