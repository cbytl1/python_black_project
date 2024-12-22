import os
import requests

from aiogram import types, F, Router, Bot
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import text
import kb
import config

img_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')

bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
router = Router()

cities_names = []
cities_data = []

class Form(StatesGroup):
    city_first = State()
    city_end = State()
    city_other = State()
    city_setting = State()
    city_days = State()
    

@router.message(Command("start"))
async def start_handler(msg: Message):
    user_name = msg.from_user.first_name
    reply_msg = text.start_msg(user_name)
    photo_file = FSInputFile(path=os.path.join(img_dir, 'img.jpg'))
    await msg.answer_photo(photo=photo_file, caption=reply_msg)

@router.message(Command("help"))
async def help_handler(msg: Message):
    reply_msg = text.help_msg()
    await msg.answer(text=reply_msg)

@router.message(Command("help"))
async def help_handler(msg: Message):
    reply_msg = text.help_msg()
    await msg.answer(text=reply_msg)

@router.message(Command("weather"))
async def weather_handler(msg: Message, state: FSMContext):
    reply_msg = text.city_first_msg()
    await msg.answer(text=reply_msg)
    await state.set_state(Form.city_first)

@router.message(Form.city_first)
async def save_city(msg: Message, state: FSMContext):
    txt = msg.text.strip().lower()
    cities_names.append(txt)
    reply_msg = text.city_last_msg()
    await state.clear()
    await state.set_state(Form.city_end)
    await msg.answer(text=reply_msg)

@router.message(Form.city_end)
async def save_city(msg: Message, state: FSMContext):
    txt = msg.text.strip().lower()
    cities_names.append(txt)
    reply_msg = text.cities_setting_msg(cities_names)
    keyboard = kb.cities_setting_kb()
    photo_file = FSInputFile(path=os.path.join(img_dir, 'img1.jpg'))
    await msg.answer_photo(photo=photo_file, caption=reply_msg, reply_markup=keyboard)
    await state.clear()

@router.callback_query(F.data == 'add_btn')
async def link_handler(call: CallbackQuery, state: FSMContext):
    reply_msg = text.city_other_msg()
    await state.set_state(Form.city_other)
    await call.message.answer(text=reply_msg)

@router.message(Form.city_other)
async def save_city(msg: Message, state: FSMContext):
    txt = msg.text.strip().lower()
    cities_names.append(txt)
    reply_msg = text.cities_setting_msg(cities_names)
    keyboard = kb.cities_setting_kb()
    photo_file = FSInputFile(path=os.path.join(img_dir, 'img1.jpg'))
    await msg.answer_photo(photo=photo_file, caption=reply_msg, reply_markup=keyboard)
    await state.clear()

@router.callback_query(F.data == 'rewrite_btn')
async def link_handler(call: CallbackQuery, state: FSMContext):
    global cities_names
    cities_names = []
    await state.set_state(Form.city_first)
    await call.message.answer(text=text.cities_clear_msg())
    await call.message.answer(text=text.city_first_msg())

@router.callback_query(F.data == 'weather_btn')
async def link_handler(call: CallbackQuery):
    response = requests.get(f"http://127.0.0.1:8050/get_data?cities={','.join(cities_names)}")
    if response.status_code == 200:
        global cities_data
        cities_data = response.json()
        for city in cities_data:
            reply_msg = text.get_graph_msg(city)
            await call.message.answer(text=reply_msg)
        reply_msg = text.last_graph_msg(cities=cities_names)
        keyboard = kb.weather_setting_kb()
        await call.message.answer(text=reply_msg, reply_markup=keyboard)
    else:
        reply_msg = str(response)    
        await call.message.answer(text=reply_msg)

@router.callback_query(F.data == 'new_type_btn')
async def link_handler(call: CallbackQuery, state: FSMContext):
    reply_msg = text.new_type_msg()
    await call.message.answer(text=reply_msg)
    await state.set_state(Form.city_setting)

@router.message(Form.city_setting)
async def save_city(msg: Message, state: FSMContext):
    txt = msg.text.strip().lower()
    
    if txt in cities_names:
        reply_msg = text.choice_new_type_msg()
        keyboard = kb.choice_new_type_kb()
        await msg.answer(text=reply_msg, reply_markup=keyboard)
        await state.update_data(city_setting=txt)
    else:
        reply_msg = text.city_not_found_msg()
        await msg.answer(text=reply_msg)
        await state.clear()
        await state.set_state(Form.city_setting)

callbacks_types = ['new_type_1', 'new_type_2', 'new_type_3']

@router.callback_query(lambda callback: callback.data in callbacks_types)
async def link_handler(call: CallbackQuery, state: FSMContext):
    typ = call.data.split('_')[-1]
    if typ == "1":
        new_type = 'Температура'
    elif typ == "2":
        new_type = 'Скорость ветра'
    else:
        new_type = 'Вероятность осадков'
    global cities_data
    states = await state.get_data()
    city_data = [x for x in cities_data if x['name'].lower() == states.get('city_setting').lower()][0]

    reply_msg = text.get_graph_msg(city_data, type=new_type)
    reply_msg1 = text.last_graph_msg(cities=cities_names)
    keyboard = kb.weather_setting_kb()
    print(reply_msg, reply_msg1)
    await call.message.answer(text=reply_msg)
    await call.message.answer(text=reply_msg1, reply_markup=keyboard)
    await state.clear()

@router.callback_query(F.data == 'new_day_btn')
async def link_handler(call: CallbackQuery, state: FSMContext):
    reply_msg = text.new_day_msg()
    await call.message.answer(text=reply_msg)
    await state.set_state(Form.city_days)

@router.message(Form.city_days)
async def save_city(msg: Message, state: FSMContext):
    txt = msg.text.strip().lower()
    
    if txt in cities_names:
        reply_msg = text.choice_new_day_msg()
        keyboard = kb.choice_new_day_kb()
        await msg.answer(text=reply_msg, reply_markup=keyboard)
        await state.update_data(city_days=txt)
    else:
        reply_msg = text.city_not_found_msg()
        await msg.answer(text=reply_msg)
        await state.clear()
        await state.set_state(Form.city_days)

callbacks_days = ['new_day_1', 'new_day_2', 'new_day_3', 'new_day_4', 'new_day_5']

@router.callback_query(lambda callback: callback.data in callbacks_days)
async def link_handler(call: CallbackQuery, state: FSMContext):
    new_day = int(call.data.split('_')[-1])
    global cities_data
    states = await state.get_data()
    city_data = [x for x in cities_data if x['name'].lower() == states.get('city_days').lower()][0]

    reply_msg = text.get_graph_msg(city_data, days=new_day)
    reply_msg1 = text.last_graph_msg(cities=cities_names)
    keyboard = kb.weather_setting_kb()
    print(reply_msg, reply_msg1)
    await call.message.answer(text=reply_msg)
    await call.message.answer(text=reply_msg1, reply_markup=keyboard)
    await state.clear()