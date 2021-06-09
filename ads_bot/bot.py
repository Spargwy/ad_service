import threading
import time

from pyrogram import filters
import dbworker
from ad import Ad
from storage import migrations, cur, con
from flow_statuses import ad_text_status, ad_price_status, user_answer_about_hot_price, set_ad_hot_price
from init import bot
import config
from pyrogram.types import ReplyKeyboardMarkup
from apscheduler.schedulers.asyncio import AsyncIOScheduler

migrations()
user_ad = {}

scheduler = AsyncIOScheduler()
scheduler.start()


async def delete_ads():
    print("START")
    req = "delete from ad"
    cur.execute(req)
    con.commit()
    print("FINISH")

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
    ad = Ad()
    user_ad[message.chat.id] = ad
    await bot.send_message(message.chat.id, "The first thing you need to do to create an ad is write your ad text.")
    dbworker.set_state(message.chat.id, config.States.S_AD_TEXT.value)


@bot.on_message(ad_text_status)
async def get_ad_text(_, message):
    user_ad[message.chat.id].ad_text = message.text
    await bot.send_message(message.chat.id, "Great\nNow you should to write price for it")
    dbworker.set_state(message.chat.id, config.States.S_AD_PRICE.value)


@bot.on_message(ad_price_status)
async def answer_user_about_hot_price(_, message):
    try:
        price = int(message.text)
        user_ad[message.chat.id].price = price
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
        req = "INSERT INTO ad(user_id, ad_text, price) VALUES(%s, %s, %s)"
        cur.execute(req, (message.chat.id,
                          user_ad[message.chat.id].ad_text,
                          user_ad[message.chat.id].price))
        con.commit()
        dbworker.set_state(message.chat.id, config.States.S_START.value)
    else:
        message_text = "please, choose the correct variant"
        await bot.send_message(message.chat.id, message_text)


@bot.on_message(set_ad_hot_price)
async def set_hot_price_value(_, message):
    try:
        hot_price = int(message.text)
        user_ad[message.chat.id].hot_price = hot_price
    except Exception as e:
        print("Error in price value: ", e)
        await bot.send_message(message.chat.id, "Please, enter the number value")
        return
    req = "update ad set top = false where top = true"
    cur.execute(req)
    req = "insert into ad(user_id, ad_text, price, hot_price, top) values (%s, %s, %s, %s, %s)"
    cur.execute(req,
                (message.chat.id,
                 user_ad[message.chat.id].ad_text,
                 user_ad[message.chat.id].price,
                 user_ad[message.chat.id].hot_price,
                 True))
    await bot.send_message(message.chat.id, "Your ad will be locate in our site")
    con.commit()


bot.run()
