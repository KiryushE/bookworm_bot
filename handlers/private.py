from aiogram import types, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, or_f
from aiogram.types import ReplyKeyboardRemove
from filters.type_of_chat import ChatTypeFilter
from keyboards.for_navigate import keyboard
from aiogram.utils.formatting import as_marked_section, Bold, TextLink

private_router = Router()
private_router.message.filter((ChatTypeFilter(["private"])))


@private_router.message(or_f(CommandStart(), F.text == "↪️Назад"))
async def start_cmd(message: types.Message):
    await message.answer("""<b>Cписок команд:</b>
<i>1. 💡Запустити бота - /start
2. 🗄Cписок книг - /my_book
3. 🔗Посилання - /links
4. 📄Інформація про бота - /about</i>""", reply_markup=keyboard.as_markup(
            resize_keyboard=True,
            input_field_placeholder="Виберіть команду"
    ))


@private_router.message(or_f(Command("about"), F.text == "📄Інформація про бота"))
async def option_cmd(message: types.Message):
    await message.answer("info about <b><u>bot</u></b>")


@private_router.message(or_f(Command("links"), F.text == "🔗Посилання"))
async def option_cmd(message: types.Message):
    text = as_marked_section(
        Bold("Active links"),
        TextLink("Автор бота", url="https://t.me/k0nn4"),
        TextLink("Група з ботом", url="https://t.me/+-P_ukdQI6Pg1YjU6"),
        marker="⚡️"
    )
    await message.answer(text.as_html())


# @private_router.message((F.text.lower() == "розклад") | (F.text.contains("schedule")))
# @private_router.message(Command("schedule"))
# async def option_cmd(message: types.Message):
#     await message.answer("our current schedule")
