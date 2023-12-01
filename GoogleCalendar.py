from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, time

SCOPES = ['https://www.googleapis.com/auth/calendar']
FILE_PATH = 'credentials.json'  # Это файл с ключами доступа Гугл Календаря(Нужно скачать и переименовать)

credentials = service_account.Credentials.from_service_account_file(filename=FILE_PATH, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)


# Перед использованием всех функций нужно активировать календарь с помощью функции ниже
def add_calendar(calendar_id):
    calendar_list_entry = {'id': calendar_id}
    return service.calendarList().insert(body=calendar_list_entry).execute()


calendar = 'amirlu2006@gmail.com'  # Сюда нужно вставить id вашего календаря(У меня была моя эл почта)


async def add_event(type_work, address, username, date, time_work, phone_number, product_price):
    event = {
        'summary': type_work,
        'location': address,
        'description': f"{username}\nНомер телефона: {phone_number}\nЦена услуги: {product_price}",
        'start': {
            'dateTime': f'{date}T{time_work}:00',
            'timeZone': 'Europe/Moscow',
        },
        'end': {
            'dateTime': f'{date}T{time_work}:00',
            'timeZone': 'Europe/Moscow',
        }
    }

    event = service.events().insert(calendarId=calendar, body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))


async def get_events_count(date):
    start_date = datetime.combine(date, time.min).isoformat() + 'Z'
    end_date = datetime.combine(date, time.max).isoformat() + 'Z'

    events_result = service.events().list(calendarId=calendar, timeMin=start_date,
                                          timeMax=end_date, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    times = []
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        start_time = datetime.fromisoformat(start).time().strftime('%H:%M')
        times.append(start_time)
    return times
