from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from aiogram_forms.forms import FormsManager
from core import settings

from .constants import (CONTACTS_INFO, HELLO_MESSAGE, HELP_INFO,
                        INTERVIEW_INVITATION, MAKE_AN_APPOINTMENT,
                        MEETING_INVITATION_MESSAGE, REFUSE_MEETING,
                        START_FILL_INTERVIEW_FORM_MESSAEGE,
                        START_FILL_METTING_FORM_MESSAEGE,
                        START_VOLUNTEERING_INFO)
from .forms import RegistrationForm, RegistrationForm1  # noqa

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


@router.message(Command(commands=['go_to_open_mitting']))
@router.message(F.text == MAKE_AN_APPOINTMENT)
async def show_metting_form(
    message: Message, bot: Bot, forms: FormsManager
) -> None:
    await bot.send_message(
        settings.manager_chat_id,
        START_FILL_METTING_FORM_MESSAEGE.format(
            username=message.from_user.username
        )
    )
    await forms.show('registration-form')


@router.message(Command(commands=['registration-form']))
async def show_settings(message: Message, forms: FormsManager):
    settings: dict = await forms.get_data('registration-form')
    print(settings)
    # for s in settings:
    #    print(settings[s])


@router.message(Command(commands=['go_to_interview']))
@router.message(F.text == REFUSE_MEETING)
async def show_interview_form(
    message: Message, bot: Bot, forms: FormsManager
) -> None:
    await message.answer(INTERVIEW_INVITATION)
    await bot.send_message(
        settings.manager_chat_id,
        START_FILL_INTERVIEW_FORM_MESSAEGE.format(
            username=message.from_user.username
        )
    )
    await forms.show('registration-form1')


@router.message(Command(commands=['help']))
async def command_help(message: Message) -> None:
    await message.answer(HELP_INFO)


@router.message(Command(commands=['contacts']))
async def command_contacts(message: Message) -> None:
    await message.answer(CONTACTS_INFO)
