import smtplib
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import *


import config


def send_email(subject, body, filename):

    try:
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = config.EMAIL_ADDRESS
        msg['To'] = ', '.join(config.recipients)

        msg.attach(MIMEText(body, 'plain'))

        attachment = open(filename, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= " + filename)

        msg.attach(part)
        text = msg.as_string()

        server = smtplib.SMTP('smtp.gmail.com: 587') # gmail server
        print("trying to establish a connection with the mail server...")
        server.ehlo()
        print("starting private session...")
        server.starttls() # establishes an encrypted session
        server.login(config.EMAIL_ADDRESS, config.PASSWORD)
        # message = 'Subject: {}\n\n{}'.format(subject, the_body)
        server.sendmail(config.EMAIL_ADDRESS, config.recipients, text)
        server.quit()
        print("Email successfully has been sent")


    except:
        print("Email failed to send")