import logging
from logging import Logger
from datetime import datetime

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

import filters
import services


user_router: Router = Router()
logger: Logger = logging.getLogger(__name__)


@user_router.message(CommandStart())
async def star_event(message: Message):
    await message.answer(
        "Привет👋 Я могу помочь найти праздник по дате\n"
        "Введи дату в формате ДД.ММ.ГГГГ"
    )


@user_router.message(filters.IsDateFilter())
async def get_holiday_date(message: Message): # Ограничиваем до 5 матчей
    selected_date: datetime = datetime.strptime(message.text, "%d.%m.%Y")
    year: int = selected_date.year
    month: int = selected_date.month
    day: int = selected_date.day

    params: dict[str: int] = {
        "year": year,
        "country": "ru"
    }
    response: dict = services.fetch_holidays(params)

    holidays: dict[str: str] = response.get("response", {}).get("holidays", [])

    holidays_in_selected_date: list[str] = [
        f"""🎉{holiday["name"]} - {holiday["date"]["datetime"]["day"]}.{holiday["date"]["datetime"]["month"]}.{holiday["date"]["datetime"]["year"]}🎉"""
        for holiday in holidays
        if holiday["date"]["datetime"]["day"] == day and holiday["date"]["datetime"]["month"] == month
    ]

    if holidays_in_selected_date:
        await message.answer(f"В эту дату {message.text} найдено {len(holidays_in_selected_date)} праздников")
        await message.answer(*holidays_in_selected_date)
    else:
        await message.answer(f"В эту дату {message.text} праздников не найдено")


@user_router.message()
async def error_event(message: Message):
    await message.answer("Упс... Что-то пошло не так(\nПопробуйте снова😭")
