VOLUNTEERING_TYPE = (
    ('Детям в больницах', 'children in hospital'),
    ('Детям в детских домах', 'children in orphanages'),
    ('Семьям с детьми-инвалидами', 'disabled children'),
    ('Могу автоволонтерить', 'auto-volunteer'),
    ('Еще не определился', 'not decide')
)

VOLUENTEERING_TYPE_QUESTION = 'Кому вы хотите помогать?'

START_FILL_METTING_FORM_MESSAEGE = ('Пользователь @{username} начал заполнять '
                                    'анкету для посещения открытой встречи!')

START_FILL_INTERVIEW_FORM_MESSAEGE = ('Пользователь @{username} начал '
                                      'заполнять анкету для прохождения '
                                      'собеседования!')

INFO_ABOUT_USER = ('Анкета волонтера:\n'
                   'Имя: {name}\n'
                   'Номер телефона: {phone}\n'
                   'Email: {email}\n'
                   'Хочет помогать: {volunteering_type}')

SUCCESSFUL_FILL_FORM_MESSAGE = ('{name}, Вы успешно прошли регистрацию! Будем '
                                'с нетерпением Вас ждать! А пока предлагаем '
                                'познакомиться получше с организацией и '
                                'нашими проектами в нашем Telegram канале '
                                '@sozidatelispb и на сайте '
                                'https://sozidateli.spb.ru/.')

HELLO_MESSAGE = ('Привет, {full_name}!\n'
                 '«Созидатели» — это команда отзывчивых людей. '
                 'Мы работаем для социализации и повышения качества '
                 'жизни детей-сирот, семей, воспитывающих '
                 'детей-инвалидов и семей в трудной жизненной ситуации.')

START_VOLUNTEERING_INFO = ('Чтобы стать волонтером, необходимо пройти '
                           'собеседование (обязательно) и посетить открытую '
                           'встречу (по желанию).')

INTERVIEW_INVITATION = ('Если вы твердо решили стать добровольцем, '
                        'заполните, пожалуйста, форму регистрации ниже и '
                        'координатор волонтеров свяжется с Вами для '
                        'согласования времени собеседования.')

MAKE_AN_APPOINTMENT = 'Записаться на встречу'

REFUSE_MEETING = 'Не хочу на встречу'

MEETING_INVITATION_MESSAGE = ('Хотите сначала познакомиться с нами на '
                              'Открытой встрече?')

NAME_FIELD_TOO_SHORT_MESSAGE = 'Поле должно содержать минимум 2 символа!'

INVALID_EMAIL_MESSAGE = 'Укажите действительный адрес электронной почты!'

INVALID_PHONE_NUMBER_MESSAGE = 'Укажите действительный номер телефона!'

INVALID_VOLUNTEERING_TYPE_MESSAGE = 'Выберите направление из предложенных!'

CONTACTS_INFO = ('Мы находимся в Санкт-Петербурге, Перекупной пер., д. 9.\n\n'
                 'Телефон координатора волонтеров: +7 (951) 686-35-35.\n\n'
                 'Email: info@sozidateli.spb.ru\n\n'
                 'Cайт: https://sozidateli.spb.ru/\n\n'
                 'Telegram канал: https://t.me/sozidatelispb')

HELP_INFO = ('Вы можете управлять ботом с помощью следующих команд:\n\n'
             '/go_to_open_mitting - заполнить форму регистрации на открытую '
             'встречу\n'
             '/go_to_interview - заполнить форму регистрации на '
             'собеседование\n'
             '/meeting_schedule - посмотреть расписание встреч\n'
             '/contacts - наши контакты\n'
             '/help - информация о возможностях бота')


GO_TO_OPEN_MITTING_COMMND = 'форма регистрации на открытую встречу'
GO_TO_INTERVIEW_COMMAND = 'форма регистрации на собеседование'
METTING_SCHEDULE_COMMAND = 'расписание открытых встреч'
CONTACTS_COMMAND = 'контакты'
HELP_COMMAND = 'справка по работе бота'
