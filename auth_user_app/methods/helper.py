from django.core.mail import send_mail
from config import settings
from threading import Thread
import re

# O‘zbekiston telefon raqamlari uchun regex (998 bilan boshlanadi)
REGEX_PHONE = r"^998([235789]{2}|(9[013-57-9]))\d{7}$"

# Email uchun regex
REGEX_EMAIL = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

# Telefon raqamini tekshiruvchi funksiya
def is_valid_phone(phone: str) -> bool:
    return re.match(REGEX_PHONE, phone) is not None

# Emailni tekshiruvchi funksiya
def is_valid_email(email: str) -> bool:
    return re.match(REGEX_EMAIL, email) is not None


def send_to_mail(address, message):
    email_message = f"Hello, {address}.\n\nThis is your code: {message}"
    subject = "Confirmation Code"
    send_mail(subject, email_message, settings.EMAIL_HOST_USER, [address], fail_silently=False)


def send_with_thread(addresses, message):
    if isinstance(addresses, str):
        addresses = [addresses]

    for address in addresses:
        if is_valid_email(address):
            thread = Thread(target=send_to_mail, args=(address, message), daemon=True)
            thread.start()
        elif is_valid_phone(address):
            print(f"{address} ga '{message}' yuborildi!")
        else:
            print(f"{address} noto'g'ri manzil!")