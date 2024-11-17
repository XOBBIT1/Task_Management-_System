import smtplib

from fastapi import HTTPException
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader
from app.repositories.users import UsersRepository, pwd_context
from app.schemas.users import EmailSchema, ResetPasswordsSchema
import secrets
import json

from app.settings import config_settings
from datetime import datetime, timedelta

from app.settings.config_settings import logger


async def open_html(user_email: str, user_name: str, user_code: str, action: bool):
    environment = Environment(loader=FileSystemLoader("app/static/templates"))
    try:
        if action:
            html_template = environment.get_template("change.html")
        else:
            html_template = environment.get_template("reset.html")
        data = {
            "user_email": user_email,
            "user_name": user_name,
            "user_code": user_code,
        }
        rendered = html_template.render(**data)
        return rendered

    except IOError:
        logger.info("The template file doesn't found")


async def send_mail(email: str, content: str):
    try:
        msg = EmailMessage()
        msg["Subject"] = "Registration"
        msg["From"] = config_settings.email_host_user
        msg["To"] = email
        msg.add_alternative(content, subtype="html")
        with smtplib.SMTP_SSL(config_settings.email_host, 465) as smtp:
            smtp.login(config_settings.email_host_user, config_settings.email_host_password)
            smtp.send_message(msg)
        logger.info(f"Email successfully send: TO: {email}")
    except Exception:
        # TODO ask and update status code
        raise HTTPException(status_code=409)


async def append_to_json_file(file_name, expire_date, _id, secure_number):
    try:
        with open(file_name, "r") as file:
            data = dict(json.load(file))

        data[secure_number] = [expire_date, _id]
        with open(file_name, "w") as file:
            json.dump(data, file)
    except FileNotFoundError:
        data_test = []
        with open(file_name, "w") as file:
            json.dump(data_test, file)


async def forgot_password(email: EmailSchema):
    secure_number = secrets.randbelow(1000000)
    secure_number_str = f"{secure_number:06}"

    user = await UsersRepository().get_user_by_email(email=email.email)
    if user is None:
        raise HTTPException(status_code=404, detail="No such user with chosen email.")

    expire_date = datetime.now() + timedelta(minutes=30)
    await append_to_json_file(
        "reset_passwords.json",
        str(expire_date),
        str(user.id),
        secure_number_str,
    )

    user_first_name = user.name
    await send_mail(
        email=email.email,
        content=f"{await open_html(str(user.email), user_first_name, secure_number_str, email.is_change)}",
    )


async def read_secure_number(file_name, secure_number):
    with open(file_name, "r") as file:
        data = json.load(file)

    if secure_number not in data:
        raise HTTPException(status_code=409, detail="Invalid secure number.")

    expire_date, _id = data[secure_number]
    if datetime.now() > datetime.fromisoformat(expire_date):
        raise HTTPException(status_code=409, detail="Secure number has expired.")
    return int(_id)


async def reset_password_service(data: ResetPasswordsSchema):
    _id = await read_secure_number(
        "reset_passwords.json", secure_number=data.secure_code
    )
    user = await UsersRepository().get_user_by_id(user_id=_id)
    user.password = pwd_context.hash(data.password)
    await UsersRepository().update_user(_id, user)
