from aiogram.types import MediaGroup
from aiogram.types import InputFile

messages = {
    "message_1": f"""<b>Выберите язык: 🌐
Tilni tanlang: 🌐</b>""",
    "message_2": {
        "ru": """<b>С возвращением 🙂</b>""",
        "uz": """<b>Xush kelibsiz 🙂</b>"""
    },
    "message_3": {
        "ru": """<b>Выберите одно из следующих ⬇</b>""",
        "uz": """<b>Quyidagilardan birini tanlang ⬇</b>"""
    },
    "message_4": {
        "ru": """<b>Выберите действие ❗</b>""",
        "uz": """<b>Harakatni tanlang ❗</b>"""
    },
    "message_5": {
        "ru": """<b>Выберите основную категорию: ⬇</b>""",
        "uz": """<b>Asosiy kategoriyalardan birini tanlang: ⬇</b>"""
    },
    "message_6": {
        "ru": """<b>Выберите подкатегорию: ⬇</b>""",
        "uz": """<b>Kategoriyalardan birini tanlang: ⬇</b>"""
    },
    "message_7": {
        "ru": """<b>Категория выбрана: </b>""",
        "uz": """<b>Ketegoriya tanlandi: </b>"""
    },
    "message_8": {
        "ru": """<b>Выберите модель: ⬇</b>""",
        "uz": """<b>Modelni tanlang: ⬇</b>"""
    },
    "message_9": {
        "ru": """<b>Вы выбрали раздел скидок ⬇</b>""",
        "uz": """<b>Siz chegirmalar bo'limini tanladingiz ⬇</b>"""
    },
}


def generate_universal_message(action, language):
    if language == 'ru':
        text = f"""<b>Вы выбрали {action} ❗</b>"""
    else:
        text = f"""<b>Siz {action} tanladingiz ❗</b>"""
    return text


# ----------------------------------------------------------------

def generate_contacts_text(contacts: list, language):
    if language == 'ru':
        text = f"""<b>Контакты ❗</b>"""
        for contact in contacts:
            text += f"<b>\n• {contact['name']} : {contact['position']} | {contact['phone']}</b>"
    else:
        text = f"""<b>Kontaktlar ❗</b>"""
        for contact in contacts:
            text += f"<b>\n• {contact['name']} : {contact['position']} | {contact['phone']}</b>"
    return text


def generate_products_text(language, name, model, description, price):
    if language == 'ru':
        text = f"""<b>Модель: </b>{model}
<b>Наименование: </b>{name}
<b>Описание: </b>{description}
<b>Цена: </b>{price if price else 'Неизвестно'}"""

    else:
        text = f"""<b>Model: </b>{model}
<b>Nomi: </b>{name}
<b>Tavsif: </b>{description}
<b>Narxi: </b>{price if price else 'Noaniq'}"""
    return text



def generate_media_group_of_product_photos(photos, text):
    media = MediaGroup()

    for photo in photos:
        print(photo)
        if photos.index(photo) == 0:
            media.attach_photo(InputFile(photo), caption=text)
        else:
            media.attach_photo(InputFile(photo))

    return media
