from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

def cities_setting_kb():
    builder = InlineKeyboardBuilder()

    new_city = InlineKeyboardButton(text="Добавить город", callback_data="add_btn")
    rewrite_btn = InlineKeyboardButton(text="Заполнить города заново", callback_data="rewrite_btn")
    weather_btn = InlineKeyboardButton(text="Получить прогноз погоды", callback_data="weather_btn")


    builder.row(new_city,rewrite_btn, width=2)
    builder.row(weather_btn, width=1)

    return builder.as_markup()

def weather_setting_kb():
    builder = InlineKeyboardBuilder()

    new_type_city = InlineKeyboardButton(text="Изменить тип графика", callback_data="new_type_btn")
    new_day_btn = InlineKeyboardButton(text="Изменить кол-во дней", callback_data="new_day_btn")
    weather_btn = InlineKeyboardButton(text="Заполнить города заново", callback_data="rewrite_btn")

    builder.row(new_type_city,new_day_btn,weather_btn, width=1)

    return builder.as_markup()

def choice_new_type_kb():
    builder = InlineKeyboardBuilder()

    tem_type = InlineKeyboardButton(text="Температура", callback_data="new_type_1")
    wind_type = InlineKeyboardButton(text="Скорость ветра", callback_data="new_type_2")
    pre_type = InlineKeyboardButton(text="Вероятность осадков", callback_data="new_type_3")

    builder.row(tem_type,wind_type,pre_type, width=1)

    return builder.as_markup()

def choice_new_day_kb():
    builder = InlineKeyboardBuilder()

    o_day = InlineKeyboardButton(text="1", callback_data="new_day_1")
    t_day = InlineKeyboardButton(text="2", callback_data="new_day_2")
    th_day = InlineKeyboardButton(text="3", callback_data="new_day_3")
    f_day = InlineKeyboardButton(text="4", callback_data="new_day_4")
    fi_day = InlineKeyboardButton(text="5", callback_data="new_day_5")


    builder.row(o_day,t_day,th_day, f_day, fi_day, width=5)

    return builder.as_markup()