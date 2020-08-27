import telebot as tb
import requests
import json
import base64

CONF = json.load(open('src/telegram_conf.json', 'r'))
"""
create and write in this file src/telegram_conf.json

{
    "token": "put here your telegram bot token",
    "discord_bot_host": "put here your remote discord bot server address also the port in case when the value distinct 80"
}
"""

URL = 'http://' + CONF['discord_bot_host'] + '/sendChannelPost'
tele_bot = tb.TeleBot(CONF['token'])


@tele_bot.channel_post_handler(content_types=['text', 'photo'])
def resend_text_to_discord(post):
    image_str = None
    if post.photo:
        downloaded_file = tele_bot.download_file(
            tele_bot.get_file(post.photo[-1].file_id).file_path)
        image_byte = base64.b64encode(downloaded_file)
        image_str = image_byte.decode('ascii')
    aviso = {'text': post.text, "caption": post.caption, "photo": image_str}
    try:
        requests.post(URL, json=aviso)
    except:
        print('Error en la conexion, post no enviado')


tele_bot.polling(none_stop=False, interval=0, timeout=20)
