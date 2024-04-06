from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.for_navigate import homeworks_keyboard

from filters.type_of_chat import ChatTypeFilter

homework_router = Router()
homework_router.message.filter(ChatTypeFilter(["private"]))


@homework_router.message(or_f(Command("homeworks"), F.text.lower() == "homeworks"))
async def homeworks_cmd(message: types.Message):
    await message.answer("Яку команду виконати з дз?", reply_markup=homeworks_keyboard)


@homework_router.message(F.text == "view all homeworks")
async def all_homeworks_cmd(message: types.Message):
    await message.answer("check all")


class AddHomeWork(StatesGroup):
    topic = State()
    number = State()
    content = State()


@homework_router.message(StateFilter(None), F.text == "add new homeworks")
async def add_homeworks_cmd(message: types.Message, state: FSMContext):
    await message.answer("Введіть тему уроку: ", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddHomeWork.topic)


@homework_router.message(Command("↪️назад"))
@homework_router.message(F.text.casefold() == "↪️назад")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "Скасування дії.", reply_markup=homeworks_keyboard
    )


@homework_router.message(AddHomeWork.topic, F.text)
async def add_number_cmd(message: types.Message, state: FSMContext):
    await state.update_data(topic=message.text)
    await message.answer("Введіть номер уроку (1 чи 2): ")
    await state.set_state(AddHomeWork.number)


@homework_router.message(AddHomeWork.number, F.text)
async def add_content_cmd(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text)
    await message.answer("Введіть завдання: ")
    await state.set_state(AddHomeWork.content)


@homework_router.message(AddHomeWork.content, F.text)
async def add_content_cmd(message: types.Message, state: FSMContext):
    await state.update_data(content=message.text)
    await message.answer("Завдання додано", reply_markup=homeworks_keyboard)
    data = await state.get_data()
    await message.answer(str(data))
    await state.clear()

