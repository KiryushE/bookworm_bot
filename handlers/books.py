import asyncio
import json

import aiofiles
from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.formatting import as_marked_section, Underline, Bold, as_key_value
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.for_navigate import books_keyboard

from filters.type_of_chat import ChatTypeFilter

book_router = Router()
book_router.message.filter(ChatTypeFilter(["private"]))


async def read_file():
    async with aiofiles.open("./data.json", encoding="utf-8") as file:
        data = await file.read()
        json_data = json.loads(data)
    return json_data


async def write_file(data):
    async with aiofiles.open("./data.json", "w", encoding="utf-8") as file:
        await file.write(json.dumps(data, indent=4))


@book_router.message(or_f(Command("books"), F.text == "📚Книги"))
async def books_cmd(message: types.Message):
    await message.answer("<i><b>Яку дію ви хочете виконати?</b></i>", reply_markup=books_keyboard)


@book_router.message(or_f(Command("my_book"), F.text == "🗄Мій список книг"))
async def all_book_cmd(message: types.Message):
    books_list = await read_file()
    for i in await read_file():
        text = as_marked_section(
            Underline(Bold("Книги")),
            as_key_value("🖋Назва книги", i["title"]),
            as_key_value("🗒Номер сторінки", i["page"]),
            as_key_value("🏷Назва закладки", i["page_name"]),
            marker=""
        )
        builder = InlineKeyboardBuilder()
        builder.add(
            types.InlineKeyboardButton(text="Видалити книгу", callback_data=f"delete_{books_list.index(i)}")
        )

        await message.answer(text.as_html(), reply_markup=builder.as_markup())
        await asyncio.sleep(0.3)


@book_router.callback_query(F.data.split("_")[0] == "delete")
async def del_book(callback: types.CallbackQuery):
    book_id = callback.data.split("_")[-1]
    books_list = await read_file()
    books_list.pop(int(book_id))
    await write_file(books_list)
    await callback.message.answer("Книга видалена зі списку!")
    await callback.answer("Its ok, book has been deleted", show_alert=True)

class AddBook(StatesGroup):
    title = State()
    page = State()
    page_name = State()


@book_router.message(StateFilter(None), F.text == "📖Додати книгу")
async def add_title_cmd(message: types.Message,  state: FSMContext):
    await message.answer("<i><b>🖋Введіть назву книги, яку хочете додати</b></i>", reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddBook.title)


@book_router.message(Command("↪️назад"))
@book_router.message(F.text.casefold() == "↪️назад")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "<i><b>❌Скасування дії❌</b></i>", reply_markup=books_keyboard
    )


@book_router.message(AddBook.title, F.text)
async def add_number_cmd(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("<i><b>🗒Введіть сторінку для закладки:</b></i>")
    await state.set_state(AddBook.page)


@book_router.message(AddBook.page, F.text)
async def add_content_cmd(message: types.Message, state: FSMContext):
    await state.update_data(page=message.text)
    await message.answer("<i><b>🏷Введіть назву закладки:</b></i>")
    await state.set_state(AddBook.page_name)


@book_router.message(AddBook.page_name, F.text)
async def add_content_cmd(message: types.Message, state: FSMContext):
    await state.update_data(page_name=message.text)
    await message.answer("<i><b>✅Закладка до книги додана✅</b></i>", reply_markup=books_keyboard)
    data = await state.get_data()
    data_to_update = await read_file()
    data_to_update.append(data)
    await write_file(data_to_update)
    await message.answer(str(data))
    await state.clear()

