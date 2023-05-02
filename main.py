from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

TOKEN_API = '6230487116:AAGCKUko_CJOSPSLzDVBibxaMz99WyMV0s4'
HELP_COMMAND = """
<b>/help</b> - <em>показывает список команд</em>
<b>/Start</b> - <em>запускает бота</em>
<b>/description</> - <em>описание бота</em>
"""

bot = Bot(TOKEN_API)
dispather = Dispatcher(bot)

kb = ReplyKeyboardMarkup(resize_keyboard=True,
                         one_time_keyboard=True)
kb.add(KeyboardButton(text='Пополнить баланс'))


async def on_startup(_):
    print('Бот был успешно запущен')


@dispather.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(text=f'Привет, {message.from_user.username}')
    await message.answer(text='Я - бот для пополнения баланса. Нажмите на кнопку, чтобы пополнить баланс',
                         reply_markup=kb)
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
