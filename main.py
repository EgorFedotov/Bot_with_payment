import os
import random

import aiogram
from aiogram import Bot, Dispatcher, executor, types
from pyqiwip2p import QiwiP2P
from dotenv import load_dotenv

from db import Database
from markups import ikb, buy_meny
from logger import add_logger


logger = add_logger(__name__)
load_dotenv()


TOKEN_API = os.getenv('TOKEN_API')
HELP_COMMAND = """
<b>/help</b> - <em>показывает список команд</em>
<b>/Start</b> - <em>запускает бота</em>
<b>/description</> - <em>описание бота</em>
"""

bot = Bot(TOKEN_API)
dispather = Dispatcher(bot)

db = Database("database.db")
p2p = QiwiP2P(auth_key=os.getenv('QIVI_TOKEN'))


def is_number(_str):
    """Проверка что пользователь ввел число."""
    try:
        int(_str)
        return True
    except ValueError:
        logger.error('Сумма пополнения не в виде числа')
        return False


async def on_startup(_):
    logger.info('Бот был успешно запущен')
    print('Бот был успешно запущен')


@dispather.message_handler(commands=['start'])
async def start_command(message: types.Message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
    try:
        await message.answer(text=f'Привет, {message.from_user.username}')
        await message.answer(text='Я - бот для пополнения баланса. Нажмите на кнопку, чтобы пополнить баланс',
                             reply_markup=ikb)
        await message.delete()
    except aiogram.exceptions.MessageError as error:
        logger.error(f'сообщения приветствия не отправленны {error}')


@dispather.callback_query_handler(text='top_up')
async def top_up(callback: types.CallbackQuery):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, 'Введите сумму, на которую вы хотите пополнить баланс')


@dispather.callback_query_handler(text='balance')
async def get_balance(callback: types.CallbackQuery):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, f'ваш баланс {db.user_money(callback.message.from_user.id)}')


@dispather.callback_query_handler(text_contains='check_')
async def check(callback: types.CallbackQuery):
    bill = str(callback.data[6:])
    info = db.get_check(bill)
    if info is not False:
        if str(p2p.check(bill_id=bill).status) == 'PAID':
            user_money = db.user_money(callback.from_user.id)
            money = int(info[2])
            db.set_money(callback.from_user.id, user_money+money)
            await bot.send_message(callback.from_user.id, 'Ваш баланс пополнен')
        else:
            await bot.send_message(callback.from_user.id,
                                   'Вы не оплатили счет!',
                                   reply_markup=buy_meny(False, bill=bill))
    else:
        await bot.send_message(callback.from_user.id, 'Счет не найден')


@dispather.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(text=HELP_COMMAND,
                        parse_mode='HTML')


@dispather.message_handler()
async def bot_mess(message: types.Message):
    if is_number(message.text):
        message_money = int(message.text)
        if message_money >= 10:
            comment = str(message.from_user.id) + '_' + str(random.randint(1000, 9999))
            bill = p2p.bill(amount=message_money, lifetime=5, comment=comment)
            db.add_check(message.from_user.id, message_money, bill.bill_id)
            await message.answer(text=f'Вам нужно отправить {message_money} руб. на наш счет QIWI\nСсылку: {bill.pay_url}\nУказав комментарий к оплате: {comment}',
                                 reply_markup=buy_meny(url=bill.pay_url, bill=bill.bill_id))
        else:
            await message.reply(text='Минимальная сумма для пополнения 10 рублей')
    else:
        await message.reply(text='Введите целое число')


if __name__ == '__main__':
    executor.start_polling(dispather,
                           on_startup=on_startup,
                           skip_updates=True)
