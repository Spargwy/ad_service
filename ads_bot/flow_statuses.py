"""Файл в котором прописаны различные статусы, которые будут присуждаться
пользователю в процессе совершения каких-либо действий"""
from pyrogram import filters
import config
import dbworker


# первый шаг для создания обьявления - текст
async def ad_text_status(_, __, message):
    return dbworker.get_current_state(message.chat.id) == config.States.S_AD_TEXT.value


# второй шаг - цена
async def ad_price_status(_, __, message):
    return dbworker.get_current_state(message.chat.id) == config.States.S_AD_PRICE.value


# узнаем о хот прайсе обьявления
async def user_answer_about_hot_price(_, __, message):
    return dbworker.get_current_state(message.chat.id) == config.States.S_ANSWER_ABOUT_HOT_PRICE.value


async def set_ad_hot_price_status(_, __, message):
    return dbworker.get_current_state(message.chat.id) == config.States.S_SET_HOT_PRICE.value

# Ниже, мы создаем фильтры, основываясь на логике функций выше
ad_text_status = filters.create(ad_text_status)
ad_price_status = filters.create(ad_price_status)
user_answer_about_hot_price = filters.create(user_answer_about_hot_price)
set_ad_hot_price = filters.create(set_ad_hot_price_status)
