import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from constants import ADMIN_MAIL


def send_email(subject=None, recipients=None, html_content=None):
    message = Mail(
        from_email=ADMIN_MAIL,
        to_emails=recipients,
        subject=subject,
        html_content=html_content)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        print(sg)
        print(os.environ.get('SENDGRID_API_KEY'))
        print(ADMIN_MAIL)
        print(recipients)
        print(html_content)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)

        return response.status_code
    except Exception as e:
        print(e.message)
        return e.message
