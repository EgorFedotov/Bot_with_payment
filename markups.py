from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ikb = InlineKeyboardMarkup(row_width=1)
ikbPay = InlineKeyboardButton(text='Пополнить баланс',
                              callback_data='top_up')
ikb.add(ikbPay)
