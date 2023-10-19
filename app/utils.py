from datetime import datetime, timedelta
from typing import Annotated

from annotated_types import MinLen

from app.exceptions import BookingDateException


def validate_date(date_from, date_to, max_days):
    date_now = datetime.now().date()

    if date_from and date_from < date_now:
        raise BookingDateException(detail=f"date_from - должен быть больше, чем: {date_now}")

    if date_from and date_to:
        if (date_to - date_from).days > max_days:
            raise BookingDateException(detail=f"Невозможно забронировать отель сроком более {max_days} дней")
        if (date_to - date_from).days < 1:
            raise BookingDateException(detail="Невозможно забронировать отель сроком менее одного дня")


def get_month_days(date_from):
    return list(map(lambda i: (date_from + timedelta(days=i)).strftime("%Y-%m-%d"), range(366)))


def format_price(number: int):
    """Returns formatted price: 1000 -> 1 000"""
    return f"{number:,}".replace(",", " ")


def decline_by_cases(number: Annotated[int, MinLen(1)], vocabulary: list[str]):
    """
        Returns inclined word.
        vocabulary = ["ночь", "ночи", "ночей"]
        number: 1 2 3 ...
        result: ночь, ночи ночи ...
    """
    while True:
        if number == 1:
            return vocabulary[0]
        if 2 <= number <= 4:
            return vocabulary[1]
        if 5 <= number <= 20:
            return vocabulary[2]
        number = int(str(number)[-1])
