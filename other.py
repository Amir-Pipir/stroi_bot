from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram_calendar import simple_cal_callback, SimpleCalendar
from create_bot import dp
from keyboards import start_kb, mkp, mkp2, phone_button
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher, types
import datetime
from aiogram.dispatcher.filters.state import State, StatesGroup
import BitrixAPI
import GoogleCalendar
import re

user_times = {}


class Add(StatesGroup):
    price = State()
    address = State()
    number = State()
    name = State()


async def start(message: Message):
    await message.answer("Что вас интересует?", reply_markup=start_kb)


@dp.callback_query_handler(Text(startswith='w_'))
async def nav_cal_handler(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    async with state.proxy() as data:
        data['service'] = call.data.split('_')[1]
    await call.message.answer("Выберите дату ", reply_markup=await SimpleCalendar().start_calendar())


@dp.callback_query_handler(simple_cal_callback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected and date.date() < datetime.datetime.now().date():
        await callback_query.message.edit_text("Выберите дату ", reply_markup=await SimpleCalendar().start_calendar())
        await callback_query.answer("Нельзя записаться на прошлое)", show_alert=True)
    elif selected and date.date() >= datetime.datetime.now().date() \
            and len(await GoogleCalendar.get_events_count(date)) <= 11:
        await callback_query.message.delete()
        user_times[callback_query.from_user.id] = await GoogleCalendar.get_events_count(date)
        async with state.proxy() as data:
            data['date'] = date.strftime("%d.%m.%Y")
            data['dateGoogle'] = date.strftime("%Y-%m-%d")
        await callback_query.message.answer("На какое время хотите записаться?", reply_markup=mkp)
    elif selected and len(await GoogleCalendar.get_events_count(date)) > 11:
        await callback_query.message.answer("Выберите дату ", reply_markup=await SimpleCalendar().start_calendar())
        await callback_query.answer("Это день весь заполнен", show_alert=True)
        await callback_query.message.delete()


async def check_time(button_time, time):
    for x in time:
        if button_time == x:
            return True
    return False


async def choose_time(call: CallbackQuery, state: FSMContext):
    act = call.data.split("_")
    if act[1] == ">":
        await call.message.edit_text("На какое время хотите записаться?", reply_markup=mkp2)
    elif act[1] == "<":
        await call.message.edit_text("На какое время хотите записаться?", reply_markup=mkp)
    else:
        if await check_time(f"{act[1]}:{act[2]}", user_times[call.from_user.id]):
            await call.answer("Это время уже занято", show_alert=True)
        else:
            await call.message.delete()
            await call.answer()
            async with state.proxy() as data:
                data['time'] = f"{act[1]}:{act[2]}"
                serv = data['service']
            if serv == "Принять квартиру со специалистом":
                await call.message.answer("Услуга включает в себя выезд(1500 руб) и размер работы(60 руб/кв.метр)\n"
                                          "Укажите сколько всего квадратных метров у вас квартира")
                await Add.price.set()
            else:
                async with state.proxy() as data:
                    data['price'] = "Договорная цена"
                await call.message.answer("Укажите адрес, куда нужно будет подъехать")
                await Add.address.set()


async def price(message: Message, state: FSMContext):
    price_mes = message.text
    if re.match("^[0-9]+$", price_mes):
        new_price = f"{int(price_mes) * 60 + 1500} руб"
        await message.answer(f"Услуга будет стоить {new_price}")
        async with state.proxy() as data:
            data['price'] = new_price
        await message.answer("Укажите адрес, куда нужно будет подъехать")
        await Add.next()
    else:
        await message.answer("Сообщение не является числом")


async def address(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text
    await message.answer("Нам нужен ваш номер телефона для связи", reply_markup=phone_button)
    await Add.next()


async def phone_str(message: Message, state: FSMContext):
    phone_text = message.text
    pattern = r'^(\+7|8)9\d{9}$'
    if re.match(pattern, phone_text):
        async with state.proxy() as data:
            data['number'] = phone_text
        await message.answer("Напишите ваше ФИО, чтобы мы знали как к вам обращаться")
        await Add.next()
    else:
        await message.reply("Сообщение не является номером телефона, напишите еще раз")


async def phone(message: Message, state: FSMContext):
    phone_number = message.contact.phone_number
    async with state.proxy() as data:
        data['number'] = phone_number
    await message.answer("Напишите ваше имя, чтобы мы знали как к вам обращаться")
    await Add.next()


async def user_name(message: Message, state: FSMContext):
    us_name = message.text
    pattern = r'^[а-яА-ЯёЁ\s]+$'
    if bool(re.match(pattern, us_name)) is False:
        await message.answer("Пожалуйста, напишите киррилицей")
    else:
        async with state.proxy() as data:
            service = data['service']
            product_price = data['price']
            date = data['date']
            dateGoogle = data['dateGoogle']
            time = data['time']
            user_address = data['address']
            phone_number = data['number']
        await message.answer(f"{us_name}\n{service}\n{product_price}\n{date}\n{time}\n{user_address}\n{phone_number}")
        await GoogleCalendar.add_event(service, user_address, message.from_user.first_name, dateGoogle, time, phone_number, product_price)
        contact_id = await BitrixAPI.insert_contact(phone_number, us_name)
        if contact_id:
            await BitrixAPI.insert_deal(contact_id, user_address, date, time, service, product_price)
        await state.finish()


async def state_cansel(message: types.Message, state: FSMContext):
    cur_state = state.get_state()
    if cur_state is None:
        return
    await state.finish()
    await message.answer("Была прервана запись на услугу, если хотите повторно записаться напишите\n/start")


def register_handlers(disp: Dispatcher):
    disp.register_message_handler(start, commands=['start'])
    disp.register_message_handler(state_cansel, state="*", commands="stop")
    disp.register_message_handler(state_cansel, Text(equals='отмена', ignore_case=True), state="*")
    disp.register_message_handler(price, state=Add.price)
    disp.register_callback_query_handler(choose_time, Text(startswith='time_'))
    disp.register_message_handler(address, state=Add.address)
    disp.register_message_handler(phone_str, state=Add.number)
    disp.register_message_handler(phone, content_types=types.ContentType.CONTACT, state=Add.number)
    disp.register_message_handler(user_name, state=Add.name)
