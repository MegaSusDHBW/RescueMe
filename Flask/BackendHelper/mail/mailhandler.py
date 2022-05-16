import yagmail
import os
from dotenv import load_dotenv

load_dotenv()
# Yagmail -> Magic Wrapper around smtplib's SMTP connection and allows messages to be sent
helpdesk = yagmail.SMTP(os.getenv('mail'), os.getenv('password'), host='smtp.strato.de', port=465, timeout=120)


def send_mail(to, subject, body):
    # Send Mail to the given recipient
    helpdesk.send(to, subject, body)

# Welcome Mail to a new user containing his/her username
def welcome_mail(to, Name):
    # Send Welcome Mail to the given recipient
    subject = "Herzlich Willkommen bei RescueMe! :)"
    body = """\
    <html>
      <head></head>
      <body>
        <p>Herzlich Willkommen {}<br>
           Es freut uns Sie bei RescueMe begrüßen zu dürfen!<br>
           Hier ist ihr  <a href="https://puginarug.com/">Registrierungslink</a>!
        </p>
      </body>
    </html>
    """.format(Name)
    send_mail(to, subject, body)


# Password Reset Mail to a specific user containing a new password
def pw_reset_mail(to, url):
    subject = "RescueMe Passwort zurücksetzen! :O"
    body = """\
    <html>
      <head></head>
      <body>
        <p>Hallo,<br>
           Vielen Dank für ihre Anfrage.<br>
           Um zurückzusetzen, hier klicken: <a href="{}">Link zum Passwort ändern</a><br>
        </p>
      </body>
    </html>
    """.format(url)
    send_mail(to, subject, body)