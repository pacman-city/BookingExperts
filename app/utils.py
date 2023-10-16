from datetime import datetime, timedelta

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
