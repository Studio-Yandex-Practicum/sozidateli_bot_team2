import asyncio

from aiogram import Bot, Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram_forms import dispatcher
from core import settings
from handlers import routers
from middlewares.throttling import ThrottlingMiddleware


async def main():
    redis = Redis(host=settings.redis_host)
    storage = RedisStorage(redis=redis)
    bot = Bot(settings.bot_token, parse_mode='HTML')
    dp = Dispatcher(storage=storage)
    dp.message.middleware(
        ThrottlingMiddleware(
            settings.throttle_time_spin,
            settings.throttle_time_other
        )
    )
    dp.callback_query.middleware(CallbackAnswerMiddleware())
    dispatcher.attach(dp)

    for router in routers:
        dp.include_router(router)

    try:
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types()
        )
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
