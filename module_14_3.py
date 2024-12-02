from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from  aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = '8143181263:AAHYq9di-YxBuZlHf1bP_ddnqmGky_2rovI'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['Start'])
async def start_message(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton(text='Рассчитать')
    button_2 = types.KeyboardButton(text='Информация')
    button_3 = types.KeyboardButton(text='Купить')
    kb.add(button_1, button_2, button_3)
    await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=kb)

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    products = [
        {'name': 'Product1', 'description': 'Описание 1', 'price': 100, 'image': '1.jpeg'},
        {'name': 'Product2', 'description': 'Описание 2', 'price': 200, 'image': '2.jpg'},
        {'name': 'Product3', 'description': 'Описание 3', 'price': 300, 'image': '3.jpg'},
        {'name': 'Product4', 'description': 'Описание 4', 'price': 400, 'image': '4.jpg'},
    ]

    for product in products:
        await message.answer(
            f'Название: {product["name"]} | Описание: {product["description"]} | Цена: {product["price"]}₽')
        await message.answer_photo(photo=open(product["image"], 'rb'))

    inline_kb = InlineKeyboardMarkup()
    for product in products:
        button = InlineKeyboardButton(text=product["name"], callback_data='product_buying')
        inline_kb.add(button)

    await message.answer('Выберите продукт для покупки:', reply_markup=inline_kb)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.answer()
    await call.message.answer('Вы успешно приобрели продукт!')


@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    inline_kb = InlineKeyboardMarkup()
    button_calories = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
    button_formulas = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
    inline_kb.add(button_calories, button_formulas)
    await message.answer('Выберите опцию:', reply_markup=inline_kb)

@dp.callback_query_handler(text ='formulas')
async def get_formulas(call):
    formula_message = (
            "Формула Миффлина-Сан Жеора:\n"
            "Для мужчин: BMR = 10 * вес + 6.25 * рост - 5 * возраст + 5\n"
            "Для женщин: BMR = 10 * вес + 6.25 * рост - 5 * возраст - 161"
        )
    await call.answer()
    await call.message.answer(formula_message)

@dp.callback_query_handler(text = 'calories')
async def set_age(call):
    await UserState.age.set()
    await call.answer()
    await call.message.answer('Введите свой возраст:')

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()

    age = int(data.get('age'))
    growth = int(data.get('growth'))
    weight = int(data.get('weight'))

    bmr = 10 * weight + 6.25 * growth - 5 * age - 161

    await message.answer(f'Ваша норма калорий: {bmr} ккал. ')
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



# from aiogram import Bot, Dispatcher, types
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.utils import executor
# import asyncio
#
# api = ''
# bot = Bot(token=api)
# dp = Dispatcher(bot, storage=MemoryStorage())
#
#
# class UserState(StatesGroup):
#     age = State()
#     growth = State()
#     weight = State()
#
#
# @dp.message_handler(commands=['start'])
# async def start_message(message: types.Message):
#     kb = ReplyKeyboardMarkup(resize_keyboard=True)
#     button_1 = KeyboardButton(text='Рассчитать')
#     button_2 = KeyboardButton(text='Информация')
#     button_3 = KeyboardButton(text='Купить')  # Новая кнопка "Купить"
#     kb.add(button_1, button_2, button_3)
#     await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=kb)
#
#
# @dp.message_handler(text='Купить')
# async def get_buying_list(message: types.Message):
#     products = [
#         {"name": "Product1", "description": "Описание 1", "price": 100},
#         {"name": "Product2", "description": "Описание 2", "price": 200},
#         {"name": "Product3", "description": "Описание 3", "price": 300},
#         {"name": "Product4", "description": "Описание 4", "price": 400},
#     ]
#
#     for product in products:
#         await message.answer(
#             f'Название: {product["name"]} | Описание: {product["description"]} | Цена: {product["price"]}₽')
#         # Здесь можно добавить код для отправки изображений, например:
#         # await message.answer_photo(photo='URL_картинки_продукта')
#
#     inline_kb = InlineKeyboardMarkup()
#     for product in products:
#         button = InlineKeyboardButton(text=product["name"], callback_data='product_buying')
#         inline_kb.add(button)
#
#     await message.answer('Выберите продукт для покупки:', reply_markup=inline_kb)
#
#
# @dp.callback_query_handler(text='product_buying')
# async def send_confirm_message(call: types.CallbackQuery):
#     await call.answer()
#     await call.message.answer("Вы успешно приобрели продукт!")
#
#
# # Остальной код из предыдущего задания...
#
# @dp.message_handler(text='Рассчитать')
# async def main_menu(message: types.Message):
#     inline_kb = InlineKeyboardMarkup()
#     button_calories = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
#     button_formulas = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
#     inline_kb.add(button_calories, button_formulas)
#     await message.answer('Выберите опцию:', reply_markup=inline_kb)
#
#
# @dp.callback_query_handler(text='formulas')
# async def get_formulas(call: types.CallbackQuery):
#     formula_message = (
#         "Формула Миффлина-Сан Жеора:\n"
#         "Для мужчин: BMR = 10 * вес + 6.25 * рост - 5 * возраст + 5\n"
#         "Для женщин: BMR = 10 * вес + 6.25 * рост - 5 * возраст - 161"
#     )
#     await call.answer()
#     await call.message.answer(formula_message)
#
#
# @dp.callback_query_handler(text='calories')
# async def set_age(call: types.CallbackQuery):
#     await UserState.age.set()
#     await call.answer()
#     await call.message.answer('Введите свой возраст:')
#
#
# @dp.message_handler(state=UserState.age)
# async def set_growth(message: types.Message, state: FSMContext):
#     await state.update_data(age=message.text)
#     await message.answer('Введите свой рост:')
#     await UserState.growth.set()
#
#
# @dp.message_handler(state=UserState.growth)
# async def set_weight(message: types.Message, state: FSMContext):
#     await state.update_data(growth=message.text)
#     await message.answer('Введите свой вес:')
#     await UserState.weight.set()
#
#
# @dp.message_handler(state=UserState.weight)
# async def send_calories(message: types.Message, state: FSMContext):
#     await state.update_data(weight=message.text)
#     data = await state
#
# > UniversusGPT | СhatGPT | Claude:
# .get_data()
#
# age = int(data.get('age'))
# growth = int(data.get('growth'))
# weight = int(data.get('weight'))
#
# bmr = 10 * weight + 6.25 * growth - 5 * age - 161
#
# await message.answer(f'Ваша норма калорий: {bmr} ккал.')
# await state.finish()
#
# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)
#
