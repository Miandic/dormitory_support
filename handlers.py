from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.chat_action import ChatActionSender
from keyboards import *
from bot_i import bot, admins, banned, pg_manager
from sqlalchemy import Integer, String


class Form(StatesGroup):
    category = State()
    username = State()
    question = State()
    validation = State()

start_router = Router()

start_text = 'Привет!\n\nЯ чат-бот, для решения проблем, возникающих в общежитии.\n\nВыбери, пожалуйста, категорию 🤔:'


async def create_table_questions(table_name='questions_reg'):
    async with pg_manager:
        columns = [
            {"name": "id", "type": Integer, "options": {"primary_key": True, "autoincrement": True}},
            {"name": "category", "type": String},
            {"name": "username", "type": String},
            {"name": "question", "type": String},
            {"name": "active", "type": String}]
        await pg_manager.create_table(table_name=table_name, columns=columns)


async def insert_table_questions(category: str, username: str, question: str, table_name='questions_reg'):
    async with pg_manager:
        users_info = {'category': category, 'username': username, 'question': question, 'active': 'True'}
        await pg_manager.insert_data_with_update(table_name=table_name, records_data=users_info, conflict_column='id', update_on_conflict=True)


async def get_table_questions():
    async with pg_manager:
        all_data = await pg_manager.select_data('questions_reg')
        ret = []
        for i in all_data:
            if(i.get('solved') == False):
                ret.append(i)
        return ret


@start_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()

    if message.from_user.id in banned:
        await message.edit_text('Ты в бане! По вопросам разбана пиши администратору :P', reply_markup=None)
        return

    await message.answer(start_text, reply_markup=start_kb(message.from_user.id))


@start_router.callback_query(F.data == 'Home')
async def cmd_start(call: CallbackQuery, state: FSMContext):
    await state.clear()

    if call.message.from_user.id in banned:
        await call.message.edit_text('Ты в бане! По вопросам разбана пиши администратору :P', reply_markup=None)
        return

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
        await state.update_data(category='бытовая')
    if category == 'corruption':
        formatted_message += 'неисправности мебели/оборудования🏚'
        await state.update_data(category='неисправности мебели/оборудования')
    if category == 'other':
        formatted_message += 'прочее🤷‍♂️'
        await state.update_data(category='прочее')

    await state.set_state(Form.username)
    #await state.set_state(Form.question)

    formatted_message += '\n\nПожалуйста, опиши свою проблему подробнее:'
    #link = call.message.chat.id
    #formatted_message += '\n\ntg://openmessage?user_id=' + str(link)
    await call.message.edit_text(formatted_message, reply_markup=change_kb())


@start_router.message(Form.username)
async def process_usrname(message: Message, state: FSMContext):
    if not message.from_user.username:
        #link='tg://openmessage?user_id=' + str(message.from_user.id)
        await state.update_data(username=('ID_' +  str(message.from_user.id)))
    else:
        #link='t.me/' + str(message.from_user.username)
        await state.update_data(username=message.from_user.username)
    
    await state.set_state(Form.question)    
    
    await process_question_text(message, state)



@start_router.message(Form.question)
async def process_question_text(message: Message, state: FSMContext):  
    if not message.text:
        await message.answer('Бот принимает только текстовые обращения.\nЕсли хочешь сменить категорию, нажми на кнопку нииже', reply_markup=change_kb())
        return
    await state.update_data(question=message.text)
    data = await state.get_data()
    #print(data)
    #link='tg://openmessage?user_id=' + str(message.from_user.id)
    if 'ID_' in str(data.get("username")):
        uid = str(data.get("username")).replace('ID_', '')
        link = 'tg://openmessage?user_id=' + uid
    else:
        link = 't.me/' + str(data.get("username"))

    #for id in admins:
    #    await bot.send_message(id, reply_text, reply_markup=link_kb(link))

    reply_text = 'Вот твоё обращение:\n\nКатегория: ' + data.get("category") +  '\n\nТекст обращения:\n' + data.get("question") + '\n\nЕсли что-то не так, начни с начала'
    
    await message.answer(reply_text, reply_markup=is_valid_kb())
    await state.set_state(Form.validation) 


@start_router.callback_query(F.data == 'correct', Form.validation)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if call.message.from_user.id in banned:
        await call.message.edit_text('Ты в бане! По вопросам разбана пиши администратору :P', reply_markup=None)
        await state.clear()
        return
    
    reply_text = 'Новое обращение! Категория: ' + data.get('category')
    for id in admins:
        await bot.send_message(id, reply_text, reply_markup=None)
    
    await insert_table_questions(data.get('category'), data.get('username'), data.get('question'))

    await call.message.edit_text('Спасибо за обращение, ваш запрос передан на рассмотрение! Скоро с тобой свяжется один из админов и поможет решить твои вопросы :)', reply_markup=change_kb())
    await state.clear()


@start_router.callback_query(F.data == 'incorrect', Form.validation)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    await cmd_start(call, state)


@start_router.callback_query(F.data == 'Admin')
async def admin(call: CallbackQuery):
    #await create_table_questions()
    await call.message.edit_text('Получаю данные...', reply_markup=None)
    cntrs = 0
    cntrh = 0
    cntrc = 0
    cntro = 0
    async with ChatActionSender.typing(bot=bot, chat_id=call.message.chat.id):
        async with pg_manager:
            all_data = await pg_manager.select_data('questions_reg', where_dict={'active': 'True'})
            for i in all_data:
                if i.get('category') == 'социльная':
                    cntrs += 1
                if i.get('category') == 'бытовая':
                    cntrh += 1
                if i.get('category') == 'неисправности мебели/оборудования':
                    cntrc += 1
                if i.get('category') == 'прочее':
                    cntro += 1
                print(i)
    answer_text = '<b>Тикеты</b>\n\n' + 'Социальных: ' + str(cntrs) + '\nБытовых: ' + str(cntrh) + '\nМебель/оборудование: ' + str(cntrc) + '\nПрочие: ' + str(cntro) + '\n\nЧтобы посмотреть тикеты, выбери категорию'
    await call.message.edit_text(answer_text, reply_markup=admin_kb())


@start_router.callback_query(F.data.startswith('admin_category_'))
async def show_tickets(call: CallbackQuery):
    category = call.data.replace('admin_category_', '')
    
    async with pg_manager:
        if category == 'social':
            data = await pg_manager.select_data('questions_reg', where_dict={'category': 'социльная'})
            
        if category == 'household':
            data = await pg_manager.select_data('questions_reg', where_dict={'category': 'бытовая'})
            
        if category == 'corruption':
            data = await pg_manager.select_data('questions_reg', where_dict={'category': 'неисправности мебели/оборудования'})
            
        if category == 'other':
            data = await pg_manager.select_data('questions_reg', where_dict={'category': 'прочее'})
        
    for i in data:
        if 'ID_' in str(i.get("username")):
            uid = str(i.get("username")).replace('ID_', '')
            link = 'tg://openmessage?user_id=' + uid
        else:
            link = 't.me/' + str(i.get("username"))
        reply_text = '<b>ID:' + str(i.get('id')) + '</b>\n\n' + str(i.get('question'))
        if i.get('active') == 'True':
            await call.message.answer(reply_text, reply_markup=answer_kb(int(i.get('id')), link))

        
@start_router.callback_query(F.data.startswith('close_ticket_'))
async def show_tickets(call: CallbackQuery):
    ticket_id = call.data.replace('close_ticket_', '')
    async with pg_manager:
        i = await pg_manager.select_data('questions_reg', where_dict={'id': int(ticket_id)})
        i[0]['active'] = 'False'
        await pg_manager.insert_data_with_update(table_name='questions_reg', records_data=i, conflict_column='id', update_on_conflict=True)
    print(i)
    if 'ID_' in str(i[0].get("username")):
        uid = str(i[0].get("username")).replace('ID_', '')
        link = 'tg://openmessage?user_id=' + uid
    else:
        link = 't.me/' + str(i[0].get("username"))
    
    await call.message.edit_text('Этот тикет закрыт', reply_markup=closed_ticket_kb(link))


@start_router.callback_query(F.data.startswith('delete_ticket_'))
async def show_tickets(call: CallbackQuery):
    ticket_id = call.data.replace('delete_ticket_', '')
    async with pg_manager:
        i = await pg_manager.select_data('questions_reg', where_dict={'id': int(ticket_id)})
        if i[0].get('active') == 'False':
            await pg_manager.delete_data(table_name='questions_reg', where_dict={'id': int(ticket_id)})
    print(i)
    if 'ID_' in str(i[0].get("username")):
        uid = str(i[0].get("username")).replace('ID_', '')
        link = 'tg://openmessage?user_id=' + uid
    else:
        link = 't.me/' + str(i[0].get("username"))
    
    await call.message.edit_text('Этот тикет удалён из истории', reply_markup=deleted_ticket_kb())


@start_router.callback_query(F.data.startswith('reopen_ticket_'))
async def show_tickets(call: CallbackQuery):
    ticket_id = call.data.replace('reopen_ticket_', '')
    async with pg_manager:
        i = await pg_manager.select_data('questions_reg', where_dict={'id': int(ticket_id)})
        i[0]['active'] = 'True'
        await pg_manager.insert_data_with_update(table_name='questions_reg', records_data=i, conflict_column='id', update_on_conflict=True)
    print(i)
    if 'ID_' in str(i[0].get("username")):
        uid = str(i[0].get("username")).replace('ID_', '')
        link = 'tg://openmessage?user_id=' + uid
    else:
        link = 't.me/' + str(i[0].get("username"))
    
    await call.message.edit_text('Этот тикет восстановлен', reply_markup=answer_kb(int(i[0].get('id')), link))


@start_router.callback_query(F.data.startswith('admin_history_'))
async def show_tickets(call: CallbackQuery):
    #category = call.data.replace('admin_history_', '')
    
    async with pg_manager:
        '''if category == 'social':
            data = await pg_manager.select_data('questions_reg', where_dict={'category': 'социльная'})
            
        if category == 'household':
            data = await pg_manager.select_data('questions_reg', where_dict={'category': 'бытовая'})
            
        if category == 'corruption':
            data = await pg_manager.select_data('questions_reg', where_dict={'category': 'неисправности мебели/оборудования'})
            
        if category == 'other':
            data = await pg_manager.select_data('questions_reg', where_dict={'category': 'прочее'})'''
        data = await pg_manager.select_data('questions_reg', where_dict={'active': 'False'})
        
    for i in data:
        if 'ID_' in str(i.get("username")):
            uid = str(i.get("username")).replace('ID_', '')
            link = 'tg://openmessage?user_id=' + uid
        else:
            link = 't.me/' + str(i.get("username"))
        reply_text = '<b>ID:' + str(i.get('id')) + '</b>\n\n' + str(i.get('question'))
        
        await call.message.answer(reply_text, reply_markup=answer_kb_history(int(i.get('id')), link))