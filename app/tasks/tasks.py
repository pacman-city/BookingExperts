import smtplib
from email.message import EmailMessage
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from app.config import settings
from app.tasks.celery import celery


@celery.task
def process_pic(path: str):
    im_path = Path(path)
    im = Image.open(im_path)
    for width in [1000, 500]:
        height = int(im.height * (width / im.width))
        resized_img = im.resize((width, height))
        resized_img.save(f"app/static/images/resized_{width}_{im_path.stem}.webp", format="WebP", quality=95)


@celery.task
def send_booking_confirmation_email(booking: dict, email_to: EmailStr):
    email = EmailMessage()
    email["Subject"] = "Подтверждение бронирования"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to
    email.set_content(
        f"""
            <h1>Подтвердите бронирование</h1>
            Вы забронировали отель с {booking["date_from"]} по {booking["date_to"]}
        """,
        subtype="html"
    )

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(email)
