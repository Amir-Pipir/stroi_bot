import requests


async def insert_contact(number, username):
    url_contact = "https://b24-muftco.bitrix24.ru/rest/1/2w1nnxsqz0rk3xlt/crm.contact.add.json"  # Это вебхук моего тестового Битрикса

    params = {
        'fields': {
            'NAME': username,
            'PHONE': [{'VALUE': number, 'VALUE_TYPE': 'WORK'}],
            'SOURCE_ID': "OTHER",
            'SOURCE_DESCRIPTION': "Telegram"
        },
        'params': {'REGISTER_SONET_EVENT': 'Y'}
    }
    response1 = requests.post(url_contact, json=params)
    return response1.json()['result']


async def insert_deal(contact_id, address, date, time, service, price):
    url_deal = "https://b24-muftco.bitrix24.ru/rest/1/936ek90my0c99692/crm.deal.add.json"  # Это вебхук моего тестового Битрикса

    params2 = {
        'fields': {
            'TITLE': service,
            'CONTACT_ID': contact_id,
            'UF_CRM_1699644393320': date,  # Это созданное поле
            'UF_CRM_1699644400695': time,  # Это созданное поле
            'UF_CRM_1699644455467': address,  # Это созданное поле
            'UF_CRM_1699644408758': price  # Это созданное поле
        }
    }
    response2 = requests.post(url_deal, json=params2)
