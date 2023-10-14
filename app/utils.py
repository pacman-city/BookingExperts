from app.exceptions import BookingDateMaxException, BookingDateMinException


def validate_date(date_from, date_to):
    if (date_to - date_from).days > 60:
        raise BookingDateMaxException
    if (date_to - date_from).days < 1:
        raise BookingDateMinException
