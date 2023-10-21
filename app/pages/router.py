from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.booking.router import get_bookings
from app.hotel.router import get_available_hotels, get_hotel_by_id
from app.room.router import get_rooms_by_time
from app.user.dependencies import verify_jwt
from app.utils import decline_by_cases, format_price, get_logo_url, get_month_days

router = APIRouter(prefix="", tags=["Фронтенд"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request, is_authenticated=Depends(verify_jwt)):
    return templates.TemplateResponse(
        "auth/login.html",
        {
            "request": request,
            "logo_url": get_logo_url(),
            "is_authenticated": is_authenticated,
        }
    )


@router.get("/register", response_class=HTMLResponse)
async def get_register_page(request: Request, is_authenticated=Depends(verify_jwt)):
    return templates.TemplateResponse(
        "auth/register.html",
        {
            "request": request,
            "logo_url": get_logo_url(),
            "is_authenticated": is_authenticated
        }
    )


@router.get("/", response_class=HTMLResponse)
async def redirect_to_hotels_page():
    return RedirectResponse(get_logo_url())


@router.get("/hotels", response_class=HTMLResponse)
async def get_hotels_page(
        request: Request,
        location: str = Query(None, description="Например: алтай"),
        date_from: str = Query(None, description=f"Min: {datetime.now().date()}"),
        date_to: str = Query(None, description=f"Например: {(datetime.now() + timedelta(days=1)).date()}, max: 365 дней"),
        is_authenticated=Depends(verify_jwt)
):
    date_now = datetime.now().date()
    date_max = date_now + timedelta(days=365)
    try:
        if not (date_from and date_to):
            raise ValueError

        date_from = date.fromisoformat(date_from)
        date_to = date.fromisoformat(date_to)
        if (date_from < date_now
                or date_to <= date_from
                or date_max < date_to):
            raise ValueError
    except ValueError:
        return RedirectResponse(
            f'hotels?date_from={date_now}&date_to={date_now + timedelta(days=1)}{f"&location={location}" if location else ""}')

    hotels = await get_available_hotels(
        max_days=365,
        location=location,
        date_from=date_from,
        date_to=date_to
    )
    return templates.TemplateResponse(
        "hotels/hotels.html",
        {
            "request": request,
            "location": location or "",
            "date_from": date_from.strftime("%Y-%m-%d"),
            "date_to": date_to.strftime("%Y-%m-%d"),
            "hotels": hotels,
            "is_authenticated": is_authenticated,
            "logo_url": get_logo_url(),
            **get_month_days(date_now)
        },
    )


@router.get("/bookings", response_class=HTMLResponse)
async def get_bookings_page(
        request: Request,
        bookings=Depends(get_bookings),
        is_authenticated=Depends(verify_jwt)
):
    return templates.TemplateResponse(
        "bookings/bookings.html",
        {
            "request": request,
            "bookings": bookings,
            "logo_url": get_logo_url(),
            "format_price": format_price,
            "decline_by_cases": decline_by_cases,
            "is_authenticated": is_authenticated,
        }
    )


@router.get("/hotels/{hotel_id}/rooms", response_class=HTMLResponse)
async def get_rooms_page(
        request: Request,
        date_from: date,
        date_to: date,
        rooms=Depends(get_rooms_by_time),
        hotel=Depends(get_hotel_by_id),
        is_authenticated=Depends(verify_jwt)
):
    date_now = datetime.now().date()
    return templates.TemplateResponse(
        "rooms/rooms.html",
        {
            "request": request,
            "hotel": hotel,
            "rooms": rooms,
            "date_from": date_from,
            "date_to": date_to,
            "logo_url": get_logo_url(),
            "booking_length": (date_to - date_from).days,
            "format_price": format_price,
            "decline_by_cases": decline_by_cases,
            "is_authenticated": is_authenticated
        }
    )
