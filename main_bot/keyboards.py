from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def generate_languages_buttons():
    markup = InlineKeyboardMarkup(row_width=1)

    btn_rus = InlineKeyboardButton(text="Русский 🇷🇺", callback_data="ru")
    btn_uzb = InlineKeyboardButton(text="O‘zbekcha 🇺🇿", callback_data="uz")

    markup.add(btn_rus, btn_uzb)

    return markup


def generate_main_menu_buttons(language):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    if language == 'ru':
        btn_katalog = KeyboardButton(text="Каталог товаров 📝")
        btn_settings = KeyboardButton(text="Настройки 🛠")
        btn_support = KeyboardButton(text="Контакты 📘")
        markup.row(btn_katalog)
        markup.row(btn_support, btn_settings)
    else:
        btn_katalog = KeyboardButton(text="Katalog 📝")
        btn_settings = KeyboardButton(text="Sozlamalar 🛠")
        btn_support = KeyboardButton(text="Kontaktlar 📘")
        markup.row(btn_katalog)
        markup.row(btn_support, btn_settings)

    return markup


def generate_settings_buttons(language):
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    if language == 'ru':
        btn_language = KeyboardButton(text="Изменить язык 🌐🔁")
        btn_back = KeyboardButton(text="Назад ⬅")
    else:
        btn_language = KeyboardButton(text="Tilni o‘zgartirish 🌐🔁")
        btn_back = KeyboardButton(text="Ortga ⬅")
    markup.add(btn_language, btn_back)
    return markup


def generate_categories_buttons(categories: list, language):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    if language == 'ru':
        sale_button = KeyboardButton(text="Скидки 🈹")
    else:
        sale_button = KeyboardButton(text="Chegirmalar 🈹")

    markup.add(sale_button)
    for category in categories:
        btn_category = KeyboardButton(text=category)
        markup.add(btn_category)

    if language == "ru":
        btn_back = KeyboardButton(text="Назад ⬅")
    else:
        btn_back = KeyboardButton(text="Ortga ⬅")

    markup.add(btn_back)

    return markup


def generate_subcategories_buttons(categories: list, language):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for category in categories:
        btn_subcategory = InlineKeyboardButton(text=category)
        markup.add(btn_subcategory)

    if language == "ru":
        btn_back = KeyboardButton(text="Назад ⬅")
    else:
        btn_back = KeyboardButton(text="Ortga ⬅")

    markup.add(btn_back)

    return markup


def generate_products_models_buttons(products: list, language):
    markup = InlineKeyboardMarkup(row_width=1)
    for product in products:
        btn_product = InlineKeyboardButton(text=product, callback_data=product)
        markup.add(btn_product)

    if language == "ru":
        btn_back = InlineKeyboardButton(text="Назад ⬅", callback_data='back')
    else:
        btn_back = InlineKeyboardButton(text="Ortga ⬅", callback_data='back')

    markup.add(btn_back)

    return markup