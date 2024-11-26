from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot_i import admins, banned

def start_kb(user_telegram_id: int):
    kb_list = []
    
    kb_list.append([InlineKeyboardButton(text='Социльная👨‍👩‍👧‍👦', callback_data='category_social'), InlineKeyboardButton(text='Бытовая🎮', callback_data='category_household')])
    kb_list.append([InlineKeyboardButton(text='Конфликтная ситуация😡', callback_data='category_conflict')])
    kb_list.append([InlineKeyboardButton(text='Неисправности мебели/оборудования🏚', callback_data='category_corruption')])
    kb_list.append([InlineKeyboardButton(text='Прочее🤷‍♂️', callback_data='category_other')])

    if user_telegram_id in admins:
        kb_list.append([InlineKeyboardButton(text="⚙️ Админ панель", callback_data='Admin')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard
    
def change_kb(user_telegram_id: int):
    kb_list = []
    kb_list.append([InlineKeyboardButton(text="Сменить категорию ↩️", callback_data='Home')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def admin_kb():
    kb_list = []
    kb_list.append([InlineKeyboardButton(text="Какой-то функционал ¯\_(ツ)_/¯", callback_data='Adminsmth')])
    kb_list.append([InlineKeyboardButton(text="Вернуться назад", callback_data='Home')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard
