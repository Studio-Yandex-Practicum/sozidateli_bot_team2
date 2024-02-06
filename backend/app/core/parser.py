import datetime as dt
import re
from http import HTTPStatus

import httpx
from lxml import html

from app.core.constants import DATE_FORMAT, URL, MONTH, DATE_PATTERN


async def parser_date() -> None | dt.datetime:
    """Парсер даты с сайта."""
    async with httpx.AsyncClient() as client:
        response = await client.get(URL)
        if response.status_code != HTTPStatus.OK:
            return None
        tree = html.fromstring(response.text)
        text = tree.xpath(
            "//div[@class='e-con-inner']"
            "//p[@class='has-black-color has-white-background-color "
            "has-text-color has-background']//strong",
        )
        try:
            date_text = re.findall(DATE_PATTERN, text[0].text)[0].split()
        except IndexError:
            return None
        if len(date_text) > 3:
            date = (f'{date_text[0]} {MONTH[date_text[1]]} '
                    f'{dt.datetime.now().year} '
                    f'{date_text[-1].replace(".", ":")}:00')
            return dt.datetime.strptime(date, DATE_FORMAT)
        return None
