from pathlib import Path

import uvicorn
from fastapi import FastAPI, BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List

from scr.conf.config import config

class EmailSchema(BaseModel):
    email: EmailStr

conf = ConnectionConfig(
    MAIL_USERNAME=config.MAIL_USERNAME,
    MAIL_PASSWORD=config.MAIL_PASSWORD,
    MAIL_FROM=config.MAIL_USERNAME,
    MAIL_PORT=config.MAIL_PORT,
    MAIL_SERVER=config.MAIL_SERVER,
    MAIL_FROM_NAME="Test Systems",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'scr/templates',
)
# conf = ConnectionConfig(
#     MAIL_USERNAME="test9095945@meta.ua",
#     MAIL_PASSWORD="Q1w2e3r4",
#     MAIL_FROM="test9095945@meta.ua",
#     MAIL_PORT=465,
#     MAIL_SERVER="smtp.meta.ua",
#     MAIL_FROM_NAME="Example email",
#     MAIL_STARTTLS=False,
#     MAIL_SSL_TLS=True,
#     USE_CREDENTIALS=True,
#     VALIDATE_CERTS=True,
#     TEMPLATE_FOLDER=Path(__file__).parent / 'scr/templates',
# )

app = FastAPI()


@app.post("/send-email")
async def send_in_background(background_tasks: BackgroundTasks, body: EmailSchema):
    message = MessageSchema(
        subject="Fastapi mail module",
        recipients=[body.email],
        template_body={"fullname": "Billy Jones"},
        subtype=MessageType.html
    )

    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message, message, template_name="example_email.html")

    return {"message": "email has been sent"}


if __name__ == '__main__':
    uvicorn.run('smail:app', port=8000, reload=True)
