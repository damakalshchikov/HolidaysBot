import asyncio
import logging
from logging import Logger

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

import handlers
import load_data

logger: Logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] #%(levelname)-8s %(filename)s:"
           "%(lineno)d - %(name)s - %(message)s"
)


async def main(bot_token: str) -> None:
    logger.info("Запуск бота")

    bot: Bot = Bot(token=bot_token, properties=DefaultBotProperties(parse_mode="HTML"))
    dp: Dispatcher = Dispatcher()

    dp.include_router(handlers.user_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main(load_data.tg_bot.token))
    except KeyboardInterrupt:
        logger.warning("Бот аварийно выключился")
    except Exception as exc:
        logger.exception(exc)
        raise exc
    finally:
        logger.info("Бот остановлен")
else:
    logger.warning("Запускай main.py")