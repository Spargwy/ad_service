import os

from asgiref.sync import sync_to_async
from pyrogram import filters
from asgiref.sync import async_to_sync

from . import dbworker
from .storage import con
from .flow_statuses import ad_text_status, ad_price_status, user_answer_about_hot_price, set_ad_hot_price
from .init import bot
from . import config
from pyrogram.types import ReplyKeyboardMarkup
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ad_page.models import Ad

user_ad = {}

scheduler = AsyncIOScheduler()
scheduler.start()


@sync_to_async
def update_ad(chat_id, **kwargs):
    ad = Ad.objects.filter(chat_id=chat_id, is_published=False).first()
    print(Ad.objects.filter(chat_id=chat_id).values('is_published'))
    for field, value in kwargs.items():
        setattr(ad, field, value)
    ad.save()
    return ad


@sync_to_async
def create_ad(chat_id):
    return Ad.objects.create(chat_id=chat_id)


@sync_to_async
def delete_ads():
    Ad.objects.filter().delete()


scheduler.add_job(func=delete_ads, trigger='cron', minute=0)


@bot.on_message(filters.command('start'))
async def start(_, message):
    print("start")
    await bot.send_message(chat_id=message.chat.id,
                           text="Hello!\n This bot can help you to create ad on website."
                                "If you want to create it, you should be click to **new ad** button",
                           reply_markup=ReplyKeyboardMarkup(
                               [
                                   ["/new ad"],
                                   ["/help"]

                               ],
                               resize_keyboard=True
                           )
                           )

    dbworker.set_state(message.chat.id, config.States.S_START)


@bot.on_message(filters.command('new ad'))
async def new_ad(_, message):
    await create_ad(message.chat.id)
    await bot.send_message(message.chat.id, "The first thing you need to do to create an ad is write your ad text.")
    dbworker.set_state(message.chat.id, config.States.S_AD_TEXT.value)


@bot.on_message(ad_text_status)
async def get_ad_text(_, message):
    await update_ad(message.chat.id, text=message.text)
    await bot.send_message(message.chat.id, "Great\nNow you should to write price for it")
    dbworker.set_state(message.chat.id, config.States.S_AD_PRICE.value)


@bot.on_message(ad_price_status)
async def answer_user_about_hot_price(_, message):
    try:
        price = int(message.text)
        await update_ad(message.chat.id, price=price)
    except Exception as e:
        print("Error in price value: ", e)
        await bot.send_message(message.chat.id, "Please, enter the number value")
        return
    await bot.send_message(chat_id=message.chat.id,
                           text="Do you want to set hot price for your ad?",
                           reply_markup=ReplyKeyboardMarkup(
                               [
                                   ["yes"],
                                   ["no"]
                               ],
                               resize_keyboard=True
                           )
                           )
    dbworker.set_state(message.chat.id, config.States.S_ANSWER_ABOUT_HOT_PRICE.value)


@bot.on_message(user_answer_about_hot_price)
async def handle_user_answer_about_hot_price(_, message):
    if message.text == "yes":
        message_text = "Your ad will be pin on the top of the site while " \
                       "another user not set ad with hot price. \n" \
                       "Now, please, set the hot price"
        await bot.send_message(message.chat.id, text=message_text,
                               reply_markup=ReplyKeyboardMarkup(
                                   [
                                       ["/new ad"],
                                       ["/help"]

                                   ],
                                   resize_keyboard=True
                               )
                               )
        dbworker.set_state(message.chat.id, config.States.S_SET_HOT_PRICE.value)
        return
    elif message.text == "no":
        message_text = "Your message will be locate in our site"
        await bot.send_message(chat_id=message.chat.id,
                               text=message_text,
                               reply_markup=ReplyKeyboardMarkup(
                                   [
                                       ["/new ad"],
                                       ["/help"]

                                   ],
                                   resize_keyboard=True
                               )
                               )
        await update_ad(message.chat.id)(is_published=True)
        dbworker.set_state(message.chat.id, config.States.S_START.value)
    else:
        message_text = "please, choose the correct variant"
        await bot.send_message(message.chat.id, message_text)


@bot.on_message(set_ad_hot_price)
async def set_hot_price_value(_, message):
    try:
        await update_ad(message.chat.id, is_published=True, hot_price=int(message.text))
    except Exception as e:
        print("Error in price value: ", e)
        await bot.send_message(message.chat.id, "Please, enter the number value")
        return
    else:
        await bot.send_message(message.chat.id, "Your ad will be locate in our site")
