import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types.bot_command import BotCommand
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram_forms import dispatcher
from core import settings
from core.logging_config import logger_1, logger_2
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
    try:
        await bot.set_my_commands(main_menu_commands)
        logger_1.info('Команды бота созданы')
    except Exception as e:
        logger_1.error(e)
        logger_2.error(e)


async def main():
    redis = Redis(host=settings.redis_host)
    logger_1.info('Бот запускается')
    storage = RedisStorage(redis=redis)
    try:
        await storage.create()
    except Exception as e:
        logger_1.error(e)
        logger_2.error(e)
    try:
        bot = Bot(settings.bot_token, parse_mode='HTML')
        logger_1.info('Бот запущен')
    except Exception as e:
        logger_1.error(e)
        logger_2.error(e)
    dp = Dispatcher(storage=storage)
    dp.message.middleware(ThrottlingMiddleware(settings.throttle_time_spin,
                                               settings.throttle_time_other))
    try:
        dp.startup.register(setup_bot_commands)
        logger_1.info('Команды бота установлены')
    except Exception as e:
        logger_1.error(e)
        logger_2.error(e)
    dp.callback_query.middleware(CallbackAnswerMiddleware())
    dispatcher.attach(dp)

    for router in routers:
        dp.include_router(router)

    try:
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types()
        )
        logger_1.info('Бот работает')
    except Exception as e:
        logger_1.error(e)
        logger_2.error(e)
    finally:
        await bot.session.close()
        logger_1.info('Бот остановлен')


if __name__ == '__main__':
    asyncio.run(main())
