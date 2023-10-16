from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self, detail=None):
        super().__init__(status_code=self.status_code, detail=detail or self.detail)


class IncorrectCredentialsException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class UserExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь с таким email уже существует"


class TokenAbsentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истек"


class TokenInvalidException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class BookingNoneAvailableException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Нет свободных номеров"


class BookingDateException(BookingException):
    """detail: required"""
    status_code = status.HTTP_400_BAD_REQUEST


class BookingUnknownException(BookingException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось забронировать номер ввиду неизвестной ошибки"


class NotFoundException(BookingException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Not Found"
