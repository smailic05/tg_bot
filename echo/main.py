from telegram import Bot
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

from bs4 import BeautifulSoup
import requests


TG_TOKEN = "###"
TG_API_URL = "https://telegg.ru/orig/bot"


def do_start(bot: Bot, update:Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="привет отправь мне что-нибудь",
    )


def log_user(bot:Bot,update:Update):    
    user_id = update.message.chat
    gfile = open(r'tg_bot\writers.txt','a')
    print(user_id,file=gfile)
    gfile.close
    bot.send_message(       
        chat_id="393069936",
        text='тебе написали' + ' ' + update.message.text + ' ' + user_id.username)


def notify_all(bot:Bot,update:Update):
    if update.message.chat_id != 393069936:
        return 0
    i=0
    mas = ''
    gfile = open(r'tg_bot\writers.txt','r')
    while True :
        readf=gfile.readline()
        if readf == '':
            return 0
        q = readf.find("id':")
        z = readf.find(',')
        chat_id_index = q+5
        chat_id = readf[chat_id_index:z]
        if mas.find(chat_id) == False:
            return 0
        bot.send_message(chat_id=chat_id,text=update.message.text[6:])
        mas = chat_id+' '
        i = i+1

    
def music (bot:Bot,update:Update):
    music_name = update.message.text[6:]
    yandex = "https://api.deezer.com/search?q=track:"
    name = yandex+'"'+music_name+'"'
    r = requests.get(name)
    temp = r.json()   
    track_id = temp['data'][0]['id']
    if track_id is None:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="я не нашел трек с таким названием"
             ) 
    else:
        url = "https://deezer.com/track/"+track_id
        bot.send_message(
            chat_id=update.message.chat_id,
            text=url
        )
    

def main():
    bot = Bot(
        token = TG_TOKEN,
        base_url = TG_API_URL,
    )
    updater = Updater(
        bot=bot,
    )
    start_handler = CommandHandler("start",do_start)
    music_handler = CommandHandler("music",music)
    social_handler = CommandHandler( "notify_all", notify_all)
    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(social_handler)
    updater.dispatcher.add_handler(music_handler)

    updater.start_polling()
    updater.idle()


if __name__ =='__main__':
    main()