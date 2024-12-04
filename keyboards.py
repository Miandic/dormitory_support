from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot_i import admins, banned

def start_kb(user_telegram_id: int):
    kb_list = [
        [InlineKeyboardButton(text='Социльная👨‍👩‍👧‍👦', callback_data='category_social'), InlineKeyboardButton(text='Бытовая🎮', callback_data='category_household')],
        [InlineKeyboardButton(text='Неисправности мебели/оборудования🏚', callback_data='category_corruption')],
        [InlineKeyboardButton(text='Прочее🤷‍♂️', callback_data='category_other')]
    ]

    if user_telegram_id in admins:
        kb_list.append([InlineKeyboardButton(text="⚙️Ответить на обращения", callback_data='Admin')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard
    
def change_kb():
    kb_list = [
        [InlineKeyboardButton(text="Главная страница ↩️", callback_data='Home')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def link_kb(user_telegram_url: str):
    kb_list = [
        [InlineKeyboardButton(text="Отправитель", url=user_telegram_url)]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def is_valid_kb():
    kb_list = [
        [InlineKeyboardButton(text="✅Все верно", callback_data='correct'), InlineKeyboardButton(text="❌Заново", callback_data='incorrect')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def admin_kb():
    kb_list = [
        [InlineKeyboardButton(text='Социльная👨‍👩‍👧‍👦', callback_data='admin_category_social'), InlineKeyboardButton(text='Бытовая🎮', callback_data='admin_category_household')],
        [InlineKeyboardButton(text='Неисправности мебели/оборудования🏚', callback_data='admin_category_corruption')],
        [InlineKeyboardButton(text='Прочее🤷‍♂️', callback_data='admin_category_other')],
        [InlineKeyboardButton(text='Закрытые тикеты (история)', callback_data='admin_history_')],
        [InlineKeyboardButton(text="Вернуться назад", callback_data='Home')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def answer_kb(ticket_id: int, user_telegram_url: str):
    kb_list = [
        [InlineKeyboardButton(text='Отправитель', url=user_telegram_url)],
        [InlineKeyboardButton(text='Закрыть тикет', callback_data=('close_ticket_' + str(ticket_id)))],
        [InlineKeyboardButton(text="К тикетам", callback_data='Admin')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def answer_kb_history(ticket_id: int, user_telegram_url: str):
    kb_list = [
        [InlineKeyboardButton(text='Отправитель', url=user_telegram_url)],
        [InlineKeyboardButton(text='Восстановить тикет', callback_data=('reopen_ticket_' + str(ticket_id)))],
        [InlineKeyboardButton(text='Удалить из истории (навсегда)', callback_data=('delete_ticket_' + str(ticket_id)))],
        [InlineKeyboardButton(text="К тикетам", callback_data='Admin')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def closed_ticket_kb(user_telegram_url: str):
    kb_list = [
        [InlineKeyboardButton(text='Отправитель', url=user_telegram_url)],
        [InlineKeyboardButton(text="К тикетам", callback_data='Admin')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard


def deleted_ticket_kb():
    kb_list = [
        [InlineKeyboardButton(text="К тикетам", callback_data='Admin')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

