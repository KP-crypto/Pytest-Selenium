from redmail import EmailSender
from smtplib import SMTP_SSL

email = EmailSender(
    host= 'mail.panasonic.aero',
    port = 587,
    cls_smtp= SMTP_SSL,
    use_starttls= False
)

email.send(
    subject= 'hello',
    sender= 'automation@panasonic.aero',
    receivers= ['ketan.puranik@panasonic.aero'],
    text = 'Hello from SMTP'
)


