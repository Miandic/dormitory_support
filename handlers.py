from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from keyboards import *

start_router = Router()


start_text = 'Привет!\n\nЯ чат-бот, для решения проблем, возникающих в общежитии.\n\nВыбери, пожалуйста, категорию 🤔:'

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(start_text, reply_markup=start_kb(message.from_user.id))


@start_router.callback_query(F.data == 'Home')
async def cmd_start(call: CallbackQuery):
    await call.message.edit_text(start_text, reply_markup=start_kb(call.from_user.id))


@start_router.callback_query(F.data.startswith('category_'))
async def show_team(call: CallbackQuery):
    category = call.data.replace('category_', '')
    formatted_message = 'Выбранная категория: '

    if category == 'social':
        formatted_message += 'социльная👨‍👩‍👧'
    if category == 'household':
        formatted_message += 'бытовая🎮'
    if category == 'conflict':
        formatted_message += 'Конфликтная ситуация😡'
    if category == 'corruption':
        formatted_message += 'неисправности мебели/оборудования🏚'
    if category == 'other':
        formatted_message += 'прочее🤷‍♂️'

    formatted_message += '\n\nПожалуйста, опиши свою проблему подробнее:'
    await call.message.edit_text(formatted_message, reply_markup=change_kb(call.from_user.id))


@start_router.callback_query(F.data == 'Admin')
async def admin(call: CallbackQuery):
    await call.message.edit_text('Я получил власть, которая и не снилась моему отцу!', reply_markup=admin_kb())
