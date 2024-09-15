from aiogram.dispatcher.filters.state import StatesGroup, State


class SettingsStatesGroup(StatesGroup):
    settings = State()


class KatalogStatesGroup(StatesGroup):
    main_category = State()
    subcategory = State()
    product = State()