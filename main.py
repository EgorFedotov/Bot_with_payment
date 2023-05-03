import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

from db import Database


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

ikb = InlineKeyboardMarkup(row_width=2)
ikbPay = InlineKeyboardButton(text='Пополнить баланс',
                              url='https://github.com/EgorFedotov')
ikb.add(ikbPay)


async def on_startup(_):
    print('Бот был успешно запущен')


@dispather.message_handler(commands=['start'])
async def start_command(message: types.Message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
    await message.answer(text=f'Привет, {message.from_user.username}')
    await message.answer(text='Я - бот для пополнения баланса. Нажмите на кнопку, чтобы пополнить баланс',
                         reply_markup=ikb)
    await message.delete()


@dispather.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(text=HELP_COMMAND,
                        parse_mode='HTML')


@dispather.message_handler(commands=['description'])
async def desc_command(message: types.Message):
    await message.answer(text='Данный бот умеет пополнять баланс кошелька qiwi')  # Описание бота
    await message.delete()


if __name__ == '__main__':
    executor.start_polling(dispather,
                           on_startup=on_startup,
                           skip_updates=True)
