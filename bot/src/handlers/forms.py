import os

from aiogram.types import Message, ReplyKeyboardRemove
from aiogram_forms import dispatcher
from aiogram_forms.forms import Form, FormsManager, fields
from dotenv import load_dotenv

from .constants import (INFO_ABOUT_USER, NAME_FIELD_TOO_SHORT_MESSAGE,
                        SUCCESSFUL_FILL_FORM_MESSAGE,
                        VOLUENTEERING_TYPE_QUESTION, VOLUNTEERING_TYPE)
from .validation import (validate_email_format, validate_phone_number_format,
                         validate_volunteering_type_field)

load_dotenv()


@dispatcher.register('registration-form')
class RegistrationForm(Form):
    name = fields.TextField(
        'Ваше имя',
        min_length=2,
        error_messages={'min_length': NAME_FIELD_TOO_SHORT_MESSAGE}
    )
    phone = fields.PhoneNumberField(
        'Телефон',
        share_contact=True,
        validators=[validate_phone_number_format]
    )
    email = fields.EmailField('E-mail', validators=[validate_email_format])
    volunteering_type = fields.ChoiceField(
        VOLUENTEERING_TYPE_QUESTION,
        choices=VOLUNTEERING_TYPE,
        validators=[validate_volunteering_type_field]
    )

    @classmethod
    async def callback(
        cls, message: Message, forms: FormsManager, **data
    ) -> None:

        registration_data = await forms.get_data('registration-form')
        volunteering_type = ''.join(
            [item[0] for item in VOLUNTEERING_TYPE
                if registration_data['volunteering_type'] in item]
        )

        await data['bot'].send_message(
            os.getenv('MANAGER_CHAT_ID'),
            INFO_ABOUT_USER.format(
                name=registration_data['name'],
                phone=registration_data['phone'],
                email=registration_data['email'],
                volunteering_type=volunteering_type
            )
        )
        await message.answer(
            text=SUCCESSFUL_FILL_FORM_MESSAGE.format(
                name=registration_data['name']
            ),
            reply_markup=ReplyKeyboardRemove()
        )
