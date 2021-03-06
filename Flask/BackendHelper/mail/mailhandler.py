import random
import time

import yagmail
import os
from dotenv import load_dotenv

load_dotenv()
# Yagmail -> Magic Wrapper around smtplib's SMTP connection and allows messages to be sent
# Could be moved into send_mail Fucntion if new Authentication is required over Time
helpdesk = yagmail.SMTP(os.getenv('mail'), os.getenv('password'), host='smtp.strato.de', port=465, timeout=120)


def send_mail(recipient, subject, body, attachments=None):
    # Send Mail to the given recipient
    # Format for Attachments:
    # Single: attachments='Desktop/File 1/image1.png' (Path as String)
    # Multiple: attachments=['Desktop/File 1/image1.png','Desktop/File 1/gantt2.png'] (List with Paths as Strings)
    try:
        helpdesk.send(to=recipient, subject=subject, contents=body, attachments=attachments,
                      bcc='helpdesk@rescue-my-balls.de')
    except Exception as e:
        print('Sending Mail has thrown a Error: {}'.format(e))
        return False


# Welcome Mail to a new user containing his/her username
def welcome_mail(to, name):
    # Send Welcome Mail to the given recipient
    code = random.randrange(100000, 1000000)
    subject = "Herzlich Willkommen bei RescueMe! :)"
    body = """\
    <html>
      <head></head>
      <body>
        <p>Herzlich Willkommen, {}<br>
           Es freut uns, Sie bei RescueMe begrüßen zu dürfen!<br>
           <br />
           Sie möchten sich als Ersthelfer verifizieren lassen?<br>
           Bitte melden Sie sich bei einem unserer Support-Mitarbeiter unter <b>+49 171 2303908</b>
           und halten Sie Ihren Verifizierungscode bereit!<br>
           Ihr Verifizierungscode lautet: <b>{}</b><br>
           Wir freuen uns, Sie bald auf unserer Plattform willkommen heißen zu können!
        </p>
      </body>
    </html>
    """.format(name, code)
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
           Um zurückzusetzen, hier klicken: <a href={}>Link zum Passwort ändern</a><br>
        </p>
      </body>
    </html>
    """.format(url)
    send_mail(to, subject, body)


def sendEmergencyMail(to, firstnameEmergency, lastnameEmergency, firstname, lastname, accidentplace=None, hospital=None):
    subject = "Ihr Angehöriger hatte einen NOTFALL!"
    body = """\
        <html>
          <head></head>
          <body>
            <p>Hallo {} {},<br>
               {} {} hatte einen Notfall!<br>
               Unfallort: {}<br>
               Krankenhaus: {}<br>
            </p>
          </body>
        </html>
        """.format(firstnameEmergency, lastnameEmergency, firstname, lastname, accidentplace, hospital)
    send_mail(to, subject, body)


def mail_changed(to, new_mail):
    subject = "Ihre Mail wurde geändert!"
    body = """\
        <html>
          <head></head>
          <body>
            <p>Hallo,<br>
               Ihr Mail bei RescueMe wurde zu {} geändert!<br>
            </p>
          </body>
        </html>
        """.format(new_mail)
    send_mail(to, subject, body)
