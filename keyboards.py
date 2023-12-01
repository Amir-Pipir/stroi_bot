from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

start_kb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text="Принять квартиру со специалистом", callback_data='w_Принять квартиру со специалистом'),
                                                 InlineKeyboardButton(text="Проверить дом перед покупкой", callback_data='w_Проверить дом перед покупкой'),
                                                 InlineKeyboardButton(text="Провести экспертизу квартиры", callback_data='w_Провести экспертизу квартиры'),
                                                 InlineKeyboardButton(text="Провести экспертизу дома", callback_data='w_Провести экспертизу дома'))


hours = ['08', '09', '10', '11', '12']
hours2 = ['13', '14', '15', '16', '17']
minutes = ['00', '30']

buttons = []
for hour in hours:
    for minute in minutes:
        text = f"{hour}:{minute}"
        callback_data = f"time_{hour}_{minute}"
        button = InlineKeyboardButton(text, callback_data=callback_data)
        buttons.append(button)

mkp = InlineKeyboardMarkup(row_width=2)
mkp.add(*buttons).add(InlineKeyboardButton(text='>>>', callback_data='time_>_>'))

buttons2 = []
for hour in hours2:
    for minute in minutes:
        text = f"{hour}:{minute}"
        callback_data = f"time_{hour}_{minute}"
        button = InlineKeyboardButton(text, callback_data=callback_data)
        buttons2.append(button)

mkp2 = InlineKeyboardMarkup(row_width=2)
mkp2.add(*buttons2).add(InlineKeyboardButton(text='<<<', callback_data='time_<_<'))

phone_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('Отправить свой контакт ☎️', request_contact=True))
