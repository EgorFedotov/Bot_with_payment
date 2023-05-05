from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


ikb = InlineKeyboardMarkup(row_width=1)
ikbPay = InlineKeyboardButton(text='Пополнить баланс',
                              callback_data='top_up')
balancekb = InlineKeyboardButton(text='Баланс',
                                 callback_data='balance')

ikb.add(ikbPay, balancekb)


def buy_meny(isUrl=True, url='', bill=''):
    qiwiMenu = InlineKeyboardMarkup(row_width=1)
    if isUrl:
        kbUrlQiwi = InlineKeyboardButton(text='Ссылка на оплату', url=url)
        qiwiMenu.add(kbUrlQiwi)

    kbcheckQiwi = InlineKeyboardButton(text='Проверить оплату', callback_data='check_'+bill)
    qiwiMenu.add(kbcheckQiwi)
    return qiwiMenu
