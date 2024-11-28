from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards import *
from bot_i import bot, admins

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

class Form(StatesGroup):
    category = State()
    username = State()
    question = State()

start_router = Router()


start_text = 'Привет!\n\nЯ чат-бот, для решения проблем, возникающих в общежитии.\n\nВыбери, пожалуйста, категорию 🤔:'

@start_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(start_text, reply_markup=start_kb(message.from_user.id))


@start_router.callback_query(F.data == 'Home')
async def cmd_start(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(start_text, reply_markup=start_kb(call.from_user.id))


@start_router.callback_query(F.data.startswith('category_'))
async def show_team(call: CallbackQuery, state: FSMContext):
    category = call.data.replace('category_', '')
    formatted_message = 'Выбранная категория: '

    await state.set_state(Form.category)
    
    if category == 'social':
        formatted_message += 'социльная👨‍👩‍👧'
        await state.update_data(category='социльная')
    if category == 'household':
        formatted_message += 'бытовая🎮'
        await state.update_data(category='бытовая🎮')
    if category == 'corruption':
        formatted_message += 'неисправности мебели/оборудования🏚'
        await state.update_data(category='неисправности мебели/оборудования')
    if category == 'other':
        formatted_message += 'прочее🤷‍♂️'
        await state.update_data(category='прочее🤷‍♂️')

    await state.set_state(Form.username)
    #await state.set_state(Form.question)

    formatted_message += '\n\nПожалуйста, опиши свою проблему подробнее:'
    #link = call.message.chat.id
    #formatted_message += '\n\ntg://openmessage?user_id=' + str(link)
    await call.message.edit_text(formatted_message, reply_markup=change_kb(call.from_user.id))


@start_router.message(Form.username)
async def process_name(message: Message, state: FSMContext):
    if not message.from_user.username:
        #link='tg://openmessage?user_id=' + str(message.from_user.id)
        await state.update_data(username=('ID_' +  str(message.from_user.id)))
    else:
        #link='t.me/' + str(message.from_user.username)
        await state.update_data(username=message.from_user.username)
    
    await state.set_state(Form.question)    
    
    if not message.text:
        await message.answer('Бот принимает только текстовые обращения.\nЕсли хочешь сменить категорию, нажми на кнопку нииже', reply_markup=change_kb(message.from_user.id))
        return
    await state.update_data(name=message.text)
    data = await state.get_data()
    print(data)
    reply_text = 'Категория: ' + data.get("category") +  '\n\nТекст обращения:\n' + message.text
    #link='tg://openmessage?user_id=' + str(message.from_user.id)
    if 'ID_' in str(data.get("username")):
        uid = str(data.get("username")).replace('ID_', '')
        link = 'tg://openmessage?user_id=' + uid
    else:
        link = 't.me/' + str(data.get("username"))

    for id in admins:
        await bot.send_message(id, reply_text, reply_markup=link_kb(link))

    await message.answer('Спасибо за обращение. Если хочешь оставить ещё, вернись на главную', reply_markup=change_kb(message.from_user.id))
    await state.clear()


@start_router.message(Form.question)
async def process_name(message: Message, state: FSMContext):  
    if not message.text:
        await message.answer('Бот принимает только текстовые обращения.\nЕсли хочешь сменить категорию, нажми на кнопку нииже', reply_markup=change_kb(message.from_user.id))
        return
    await state.update_data(name=message.text)
    data = await state.get_data()
    print(data)
    reply_text = 'Категория: ' + data.get("category") +  '\n\nТекст обращения:\n' + message.text
    #link='tg://openmessage?user_id=' + str(message.from_user.id)
    if 'ID_' in str(data.get("username")):
        uid = str(data.get("username")).replace('ID_', '')
        link = 'tg://openmessage?user_id=' + uid
    else:
        link = 't.me/' + str(data.get("username"))

    for id in admins:
        await bot.send_message(id, reply_text, reply_markup=link_kb(link))

    await message.answer('Спасибо за обращение. Если хочешь оставить ещё, вернись на главную', reply_markup=change_kb(message.from_user.id))
    await state.clear()




@start_router.callback_query(F.data == 'Admin')
async def admin(call: CallbackQuery):
    await call.message.edit_text('Я получил власть, которая и не снилась моему отцу!', reply_markup=admin_kb())
