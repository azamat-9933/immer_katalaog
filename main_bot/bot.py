import logging
import aiohttp
from aiogram import Bot, Dispatcher, executor
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, Message, CallbackQuery

from keyboards import *
from queries import *
from messages import *
from states import *
from configs import *

# Устанавливаем уровень логирования
logging.basicConfig(level=logging.INFO)

API_TOKEN = TOKEN
bot = Bot(token=API_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())


async def check_connection():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.telegram.org') as response:
                return response.status == 200
    except Exception as e:
        logging.error(f"Ошибка соединения: {e}")
        return False


@dp.errors_handler()
async def error_handler(update, exception):
    logging.error(f"Ошибка: {exception}")
    return True


@dp.message_handler(commands=['start'], state=['*'])
async def cmd_start(message: Message) -> None:
    telegram_id = message.chat.id
    users = get_users_telegram_ids()
    if telegram_id not in users:
        insert_user_telegram_id(telegram_id)
        await bot.send_message(telegram_id, text=messages['message_1'],
                               reply_markup=generate_languages_buttons())
    else:
        user_language = get_user_language(telegram_id)
        await bot.send_message(telegram_id, text=f"""{messages['message_2'][user_language]}""")
        await main_menu(message)


@dp.callback_query_handler(lambda call: call.data in ["ru", "uz"], state=['*'])
async def set_user_language(call: CallbackQuery) -> None:
    telegram_id = call.message.chat.id
    message_id = call.message.message_id
    language = call.data
    update_user_language(telegram_id, language)
    await bot.delete_message(telegram_id, message_id)
    await main_menu(call.message)


async def main_menu(message: Message) -> None:
    telegram_id = message.chat.id
    user_language = get_user_language(telegram_id)
    await bot.send_message(telegram_id, text=f"""{messages['message_3'][user_language]}""",
                           reply_markup=generate_main_menu_buttons(user_language))


@dp.message_handler(lambda message: "🛠" in message.text and message.chat.id in get_users_telegram_ids())
async def change_settings(message: Message) -> None:
    telegram_id = message.chat.id
    user_language = get_user_language(telegram_id)
    await bot.send_message(telegram_id, text=f"""{messages['message_4'][user_language]}""",
                           reply_markup=generate_settings_buttons(user_language))
    await SettingsStatesGroup.settings.set()


@dp.message_handler(state=SettingsStatesGroup.settings)
async def check_user_answer_settings(message: Message, state: FSMContext) -> None:
    chat_id = message.chat.id
    language = get_user_language(chat_id)
    if '⬅' in message.text:
        await state.finish()
        await main_menu(message)
    elif '🌐' in message.text:
        text = generate_universal_message(action=message.text, language=language)
        await bot.send_message(chat_id, f"""{text}""", reply_markup=ReplyKeyboardRemove())
        await bot.send_message(chat_id, f"""<b>Выберите язык: 🌐
Tilni tanlang: 🌐</b>""",
                               reply_markup=generate_languages_buttons())
        await state.finish()


@dp.message_handler(lambda message: "📘" in message.text and message.chat.id in get_users_telegram_ids())
async def show_contacts(message: Message) -> None:
    telegram_id = message.chat.id
    user_language = get_user_language(telegram_id)
    contacts = get_all_contacts()
    text = generate_contacts_text(contacts, user_language)
    await bot.send_message(telegram_id, text=text)
    await main_menu(message)


@dp.message_handler(lambda message: "📝" in message.text and message.chat.id in get_users_telegram_ids())
async def show_main_categories(message: Message) -> None:
    telegram_id = message.chat.id
    user_language = get_user_language(telegram_id)
    categories = get_all_categories_names(user_language)
    await bot.send_message(telegram_id, text=f"""{messages['message_5'][user_language]}""",
                           reply_markup=generate_categories_buttons(categories, user_language))
    await KatalogStatesGroup.main_category.set()


@dp.message_handler(state=KatalogStatesGroup.main_category)
async def show_subcategories(message: Message, state: FSMContext) -> None:
    telegram_id = message.chat.id
    if "⬅" in message.text:
        await main_menu(message)
        await state.finish()
    elif "💥" in message.text:
        user_language = get_user_language(telegram_id)
        products = get_all_sale_products(user_language)
        await show_products_by_category(message, products)
    else:
        user_language = get_user_language(telegram_id)
        category_name = message.text
        subcategories = get_subcategories_by_category_name(category_name, user_language)
        if subcategories:
            await bot.send_message(telegram_id, text=f"""{messages['message_6'][user_language]} {category_name}""",
                                   reply_markup=generate_subcategories_buttons(subcategories, user_language))
            await KatalogStatesGroup.subcategory.set()
        else:
            await state.finish()
            await show_products_by_category(message)


@dp.message_handler(state=KatalogStatesGroup.subcategory)
async def show_products_subcategory(message: Message, state: FSMContext) -> None:
    telegram_id = message.chat.id
    user_language = get_user_language(telegram_id)
    subcategory_name = message.text

    if "⬅" in message.text:
        await show_main_categories(message)
    else:
        products = get_all_products(user_language, subcategory_name)
        await bot.send_message(telegram_id, text=f"""{messages['message_7'][user_language]} {subcategory_name} ⬇""",
                               reply_markup=ReplyKeyboardRemove())
        await show_products_by_category(message, products)


async def show_products_by_category(message: Message, taked_products=None) -> None:
    telegram_id = message.chat.id
    user_language = get_user_language(telegram_id)
    category_name = message.text

    if taked_products:
        products = taked_products
    elif get_all_products(user_language, category_name):
        products = get_all_products(user_language, category_name)
    else:
        products = None
    if products:
        for product in products:
            text = generate_products_text(user_language,
                                          product['name'],
                                          product['model'],
                                          product['description'],
                                          product['price'])
            if len(product['photos']) == 0:
                await bot.send_photo(telegram_id,
                                     photo=open("no_photo.jpg", mode='rb'),
                                     caption=text)
            elif len(product['photos']) == 1:
                try:
                    await bot.send_photo(telegram_id,
                                         photo=open(product['photos'][0], mode='rb'),
                                         caption=text)
                except:
                    await bot.send_document(telegram_id,
                                            document=open(product['photos'][0], mode='rb'),
                                            caption=text)
            elif len(product['photos']) > 1:
                photos = generate_media_group_of_product_photos(product['photos'], text)

                await bot.send_media_group(telegram_id, media=photos)
    else:
        await bot.send_message(telegram_id, text=f"""{messages['message_8'][user_language]}""")

    await show_main_categories(message)




@dp.callback_query_handler(state=['*'])
async def show_product_button(call: CallbackQuery, state: FSMContext) -> None:
    telegram_id = call.message.chat.id
    if "back" == call.data:
        await main_menu(call.message)
        await state.finish()
    else:
        user_language = get_user_language(telegram_id)
        product_model_name = call.data
        product_info = return_product_all_info_with_photo(product_model_name, user_language)
        text = generate_products_text(user_language, product_info['name'],
                                      product_info['model'], product_info['description'],
                                      product_info['price'])
        photos = generate_media_group_of_product_photos(product_info['photos'], text)
        await bot.send_media_group(telegram_id, media=photos)


async def on_startup(dp):
    if not await check_connection():
        logging.error("Ошибка подключения к Telegram API. Бот не будет запущен.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
