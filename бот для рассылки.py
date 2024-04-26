import asyncio
import datetime
import time
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram import executor
import sqlite3


# Обозначения токена для бота
API_TOKEN = '7193032252:AAGE-TKF2eZ85hs5-Oo9O1qC282pyy9nKRs'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
USERS = []

# Обозначения инлайн кнопок
button1 = types.InlineKeyboardButton(text="Кординаты станции МКС", callback_data="button1_pressed")
button2 = types.InlineKeyboardButton(text="Настроить время", callback_data="button2_pressed")
button3 = types.InlineKeyboardButton(text="Назад", callback_data="back_to_main")
button4 = types.InlineKeyboardButton(text="Напоминание", callback_data="button3_pressed")
inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[[button1, button2], [button3, button4]])

# Кординаты станции МКС
def requst():
    api_url = 'http://api.open-notify.org/iss-now.json'
    get = requests.get(api_url)
    list_1 = []
    if get.status_code == 200:
        list_1.append(get.json()['iss_position']['latitude'])
        list_1.append(get.json()['iss_position']['longitude'])
        return list_1
    else:
        return get.status_code

def new_time_user():
    @dp.message_handler()
    async def send_echo(message: Message):

        second_value = message.text
        first_value = message.from_user.id
        USERS.append(first_value)

        if int(second_value[:2]) <= 24 and int(second_value[3:]) <= 60 and len(second_value) == 5:
            conn = sqlite3.connect('user.sqlite')
            cursor = conn.cursor()

            # Проверка наличия таблицы users и, если она не существует, создание её
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT NOT NULL,
                    time TEXT NOT NULL
                )
            ''')

            if first_value in USERS:
                await bot.send_message(first_value, "Простите, но это можно было менять один раз.")

            else:
                cursor.execute(f'''
                    INSERT INTO users (id, time) VALUES ("{str(first_value)}", "{str(second_value)}")
                ''')
                conn.commit()
                await bot.send_message(first_value, "Спасибо за ваш ответ.")
                conn.close()

        else:
            await bot.send_message(first_value,"Просим вас ввесте правильное время.")
            new_time_user()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message_handler(commands=["start"])
async def process_start_command(message: Message):
    await message.answer("Привет! Нажми на одну из кнопок ниже:", reply_markup=inline_keyboard)



# Обработчик нажатия на кнопку 1
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'button1_pressed')
async def process_callback_button1(callback_query: types.CallbackQuery):
    latitude = requst()[0]
    longitude = requst()[1]
    await bot.send_message(callback_query.from_user.id, f'Долгота - {longitude} и  широта - {latitude}, а если хотите узнать решение то заходите на наш сайт.')

# Обработчик нажатия на кнопку 2
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'button2_pressed')
async def process_callback_button2(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Прошу вас ввести новое время в виде: '10:00', '17:59', '09:00'.")
    new_time_user()

# Обработчик нажатия на кнопку 3
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'back_to_main')
async def process_callback_back_to_main(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Вы вернулись на главную", reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'button3_pressed')
async def process_callback_back_to_main(callback_query: types.CallbackQuery):
    mes = callback_query.from_user.id
    await bot.send_message(callback_query.from_user.id, "Вы запустили напоминание")

    conn = sqlite3.connect('user.sqlite')
    cursor = conn.cursor()
    result = cursor.execute(f"""SELECT * FROM users WHERE id = {mes}""").fetchall()
    n = int(result[-1][1][:2])
    m = int(result[-1][1][3:])
    conn.close()
    while True:
        now = datetime.datetime.now()
        if now.hour == n and now.minute == m:  # отправляем сообщение в 17:00
            await bot.send_message(mes, "Пора позаниматься.")
            break

        await asyncio.sleep(1)



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    executor.start_polling(dp, loop=loop)