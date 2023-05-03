from aiogram.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup,
                           KeyboardButton,
                           ReplyKeyboardMarkup)

kb = ReplyKeyboardMarkup(resize_keyboard=True)
balancekb = KeyboardButton(text='Баланс')
kb.add(balancekb)

ikb = InlineKeyboardMarkup(row_width=1)
ikbPay = InlineKeyboardButton(text='Пополнить баланс',
                              callback_data='top_up')
ikb.add(ikbPay)


def buy_meny(isUrl=True, url='', bill=''):
    qiwiMenu = InlineKeyboardMarkup(row_width=1)
    if isUrl:
        kbUrlQiwi = InlineKeyboardButton(text='Ссылка на оплату', url=url)
        qiwiMenu.add(kbUrlQiwi)

    kbcheckQiwi = InlineKeyboardButton(text='Проверить оплату', callback_data='check_'+bill)
    qiwiMenu.add(kbcheckQiwi)
    return qiwiMenu
