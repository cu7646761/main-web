from flask_mail import Message

from app import mail


def send_email(subject=None, recipients=None, text_body=None, html_body=None):
    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

# @async_func
# def send_async_email(app, msg):
#     with app.app_context():
#         mail.send(msg)
