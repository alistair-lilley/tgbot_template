"""Commands
Registers commands via decorator
ONLY for registering commands and such
"""
from __future__ import annotations

import logging

from dotenv import dotenv_values

from aiogram import Bot, Router, Dispatcher
from aiogram import F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.types.error_event import ErrorEvent

LOGGER = logging.getLogger(__file__)

config = dotenv_values(".env")

DEBUGGING = True if config["DEBUGGING"].lower() == "true" else False
TOKEN = config["TOKEN"]
MEEEEEEEE = config["ME"]

tgbot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
router = Router()
dispatcher = Dispatcher()
dispatcher.include_router(router)


if not DEBUGGING:

    @router.error(F.update.message.as_("message"))
    async def error(event: ErrorEvent, message: Message) -> None:
        """Catches all errors"""
        LOGGER.critical(
            "An error occurred from this message: %s",
            message.text
        )
        LOGGER.critical("error was this: %s", str(event.exception))


@router.message()
async def catchall(message: Message):
    """Catches all other messages for the pre-command checks"""
    LOGGER.info("Ignored message (%s)", message.text)

