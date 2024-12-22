import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.utils import executor
from weather import fetch_location_key, fetch_daily_forecast
from graph import generate_ascii_graph
import pandas as pd

API_TOKEN = '5368650379:AAG3me15KQYWdSoKBccuWmPySoQsciTUu3g'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Список пользователей, которым будет отправлен результат
cities = []

# Команда /start
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот, который поможет узнать погоду в разных городах.\n"
                         "Используй команду /weather для запроса прогноза погоды.")

# Команда /help
@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    await message.answer("Доступные команды:\n"
                         "/start - Приветствие\n"
                         "/help - Справка по командам\n"
                         "/weather - Прогноз погоды")

# Команда /weather для запроса прогноза
@dp.message_handler(commands=['weather'])
async def cmd_weather(message: types.Message):
    await message.answer("Введите начальный город:")

    @dp.message_handler()
    async def get_start_city(message: types.Message):
        start_city = message.text
        cities.append(start_city)
        await message.answer(f"Начальный город: {start_city}\nВведите конечный город:")

        @dp.message_handler()
        async def get_end_city(message: types.Message):
            end_city = message.text
            cities.append(end_city)
            await message.answer(f"Конечный город: {end_city}\nВведите промежуточный город (или нажмите /finish для завершения):")

            @dp.message_handler(commands=['finish'])
            async def finish_weather(message: types.Message):
                weather_info = ""
                for city in cities:
                    location = fetch_location_key(city)
                    if location:
                        forecast = fetch_daily_forecast(location[0])
                        if forecast:
                            df = pd.DataFrame([{
                                'time': item['Date'][:10],
                                'temperature': item['Temperature']['Maximum']['Value'],
                                'wind_speed': item['Day']['Wind']['Speed']['Value'],
                                'precipitation_probability': item['Day']['PrecipitationProbability']
                            } for item in forecast])

                            # Генерация графика в ASCII
                            graph = generate_ascii_graph(df, 'time', 'temperature')

                            weather_info += f"Прогноз погоды для города {city}:\n{graph}\n"
                        else:
                            weather_info += f"Не удалось получить прогноз для города {city}.\n"
                    else:
                        weather_info += f"Не удалось найти информацию о городе {city}.\n"

                await message.answer(weather_info)

# Обработчик ошибок
@dp.errors_handler(exception=Exception)
async def error_handler(update, exception):
    logging.error(f"Exception occurred: {exception}")
    return True

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
