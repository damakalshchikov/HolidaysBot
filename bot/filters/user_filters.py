import re

from aiogram.filters import BaseFilter
from aiogram.types import Message

import services


class IsDateFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        pattern: str = r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(19|20)\d{2}$"

        if services.is_valid_date(message.text):
            return bool(re.match(pattern, message.text))
        return False