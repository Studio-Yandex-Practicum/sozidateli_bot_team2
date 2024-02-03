import asyncio
import logging
from pathlib import Path
import sys

from aiogram import Bot, Dispatcher
from aiogram.types.bot_command import BotCommand
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram_forms import dispatcher
from core import settings
from core.logging_config import configure_logging
from handlers import routers
from handlers.constants import (CONTACTS_COMMAND, GO_TO_INTERVIEW_COMMAND,
                                GO_TO_OPEN_MEETING_COMMND, HELP_COMMAND,
                                MEETING_SCHEDULE_COMMAND)
from middlewares.throttling import ThrottlingMiddleware


async def setup_bot_commands(bot: Bot):

    main_menu_commands = [
        BotCommand(command='/help', description=HELP_COMMAND),
        BotCommand(command='/go_to_open_meeting',
                   description=GO_TO_OPEN_MEETING_COMMND),
        BotCommand(command='/go_to_interview',
                   description=GO_TO_INTERVIEW_COMMAND),
        BotCommand(command='/meeting_schedule',
                   description=MEETING_SCHEDULE_COMMAND),
        BotCommand(command='/contacts', description=CONTACTS_COMMAND)
    ]
    await bot.set_my_commands(main_menu_commands)
    logging.info('Команды бота установлены')


async def main():
    configure_logging(Path(__file__).parent / 'logs')
    logging.info('Запуск бота')
    redis = Redis(host=settings.redis_host)
    storage = RedisStorage(redis=redis)
    logging.info('Соединение с Redis создано')
    try:
        bot = Bot(settings.bot_token, parse_mode='HTML')
        logging.info('Бот создан')
    except Exception as error:
        logging.exception(f'Бот не создан. Ошибка {error}')
        sys.exit('Отсутствуют данные окружения. Завершаю работу.')
    dp = Dispatcher(storage=storage)
    dp.message.middleware(ThrottlingMiddleware(settings.throttle_time_spin,
                                               settings.throttle_time_other))
    dp.startup.register(setup_bot_commands)
    logging.info('Команды для бота регистрированы')
    dp.callback_query.middleware(CallbackAnswerMiddleware())
    dispatcher.attach(dp)

    for router in routers:
        dp.include_router(router)

    try:
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types()
        )
        logging.info('Бот запущен')
    except Exception as error:
        logging.exception(f'Бот упал с ошибкой {error}')
    finally:
        await bot.session.close()
        logging.info('Сеанс бота закрыт')


if __name__ == '__main__':
    asyncio.run(main())
