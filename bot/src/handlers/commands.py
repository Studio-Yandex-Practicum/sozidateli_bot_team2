from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from aiogram_forms.forms import FormsManager

from .constants import (CONTACTS_INFO, HELLO_MESSAGE, HELP_INFO,
                        MAKE_AN_APPOINTMENT, MEETING_INVITATION_MESSAGE,
                        REFUSE_MEETING, START_VOLUNTEERING_INFO)
from .forms import RegistrationForInterviewForm  # noqa
from .forms import RegistrationForMeetingForm  # noqa

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        HELLO_MESSAGE.format(full_name=message.from_user.full_name)
    )

    buttons = [
        [
            KeyboardButton(text=MAKE_AN_APPOINTMENT),
            KeyboardButton(text=REFUSE_MEETING)
        ]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    await message.answer(START_VOLUNTEERING_INFO)
    await message.answer(MEETING_INVITATION_MESSAGE, reply_markup=keyboard)


@router.message(Command(commands=['go_to_open_meeting']))
@router.message(F.text == MAKE_AN_APPOINTMENT)
async def show_metting_form(
    message: Message, forms: FormsManager
) -> None:
    await forms.show('registration-for-meeting-form')


@router.message(Command(commands=['go_to_interview']))
@router.message(F.text == REFUSE_MEETING)
async def show_interview_form(
    message: Message, bot: Bot, forms: FormsManager
) -> None:
    await forms.show('registration-for-interview-form')


@router.message(Command(commands=['help']))
async def command_help(message: Message) -> None:
    await message.answer(HELP_INFO)


@router.message(Command(commands=['contacts']))
async def command_contacts(message: Message) -> None:
    await message.answer(CONTACTS_INFO)
