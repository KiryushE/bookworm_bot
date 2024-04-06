from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# keyboard = types.ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             types.KeyboardButton(text="optionals"),
#             types.KeyboardButton(text="schedule")
#         ],
#         [
#             types.KeyboardButton(text="links"),
#             types.KeyboardButton(text="homeworks")
#         ],
#         [
#             types.KeyboardButton(text="about")
#         ]
#     ],
#     resize_keyboard=True,
#     input_field_placeholder="Choose your command"
# )

keyboard = ReplyKeyboardBuilder()
keyboard.add(
    types.KeyboardButton(text="📚Книги"),
    types.KeyboardButton(text="🔗Посилання"),
    types.KeyboardButton(text="📄Інформація про бота")
)
keyboard.adjust(3, 2)


books_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="🗄Мій список книг")
        ],
        [
            types.KeyboardButton(text="📖Додати книгу")
        ],
        [
            types.KeyboardButton(text="↪️Назад")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Виберіть одну з команд"
)


cancel_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="Назад")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Для повернення натисніть кнопку"
)
