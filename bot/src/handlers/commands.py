import locale

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from aiogram_forms.forms import FormsManager
from schemas import assistance
from schemas import users as schemas_users
from services import meetings, users

from .constants import (CONTACTS_INFO, HELLO_MESSAGE, HELP_INFO,
                        INFO_ABOUT_MEETING, MAKE_AN_APPOINTMENT,
                        MEETING_INVITATION_MESSAGE, REFUSE_MEETING,
                        START_VOLUNTEERING_INFO)
from .forms import RegistrationForInterviewForm  # noqa
from .forms import RegistrationForMeetingForm  # noqa

router = Router()
locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"  # Note: do not use "de_DE" as it doesn't work
)


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
    message: Message, forms: FormsManager
) -> None:
    await forms.show('registration-for-interview-form')


@router.message(Command(commands=['help']))
async def command_help(message: Message) -> None:
    await message.answer(HELP_INFO)


@router.message(Command(commands=['contacts']))
async def command_contacts(message: Message) -> None:
    await message.answer(CONTACTS_INFO)


@router.message(Command(commands=['meeting_schedule']))
async def command_meeting_schedule(message: Message) -> None:
    user_service = users.UserService()
    user = schemas_users.UserCreate(
        name="Name1",
        phone='+79637344989',
        email='julia1@mail.com',
        meeting_id=3,
        assistance_segment=assistance.AssistanceSegment.not_decide
    )
    print(user)
    await user_service.create_user(user)

    meeting_service = meetings.MeetingService()
    all_meetings = await meeting_service.get_meetings()
    print_meetings = []
    for meeting in all_meetings:
        if meeting.is_open:
            print_meetings.append(meeting.date)
    print_meetings.sort()
    for date in print_meetings:
        await message.answer(
            INFO_ABOUT_MEETING.format(date=date.strftime("%d-%m-%Y в %H.%S"))
        )
