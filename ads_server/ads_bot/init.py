import configparser

from pyrogram import Client

config = configparser.ConfigParser()
config.read('ads_bot/app.ini')
api_id = config['api']['api_id']
api_hash = config['api']['api_hash']
bot_token = config['api']['bot_token']


bot = Client("bot_session", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
