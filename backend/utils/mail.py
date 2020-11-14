from flask_mail import Message, Mail

mail = Mail()


def send_email(recipient, subject, message):
    msg = Message(
        subject=subject,
        recipients=[recipient],
        body=message
    )
    mail.send(msg)
