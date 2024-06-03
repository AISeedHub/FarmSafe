from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
import smtplib
import os

from db.get_data import *
from render_HTTP import generate_html


def get_customer_emails():
    data = get_all_users()
    emails = [d['email'] for d in data]
    return emails


def report_make_up(farm_id, farm_name):
    device_data = get_latest_sensor_data(farm_id)
    camera_data = None
    sensor_data = {}
    """
    device_data = {
        'device1': cursor1,
        'device2': cursor2,
        ...
    }
    """
    for device in device_data:
        sensor_data[device] = device_data[device].next()  # get the first element of the cursor

    return generate_html(farm_name, sensor_data, camera_data)


# smtp = smtplib.SMTP('smtp.gmail.com', 587)
# smtp.ehlo()
# smtp.starttls()
# smtp.login('aiseed.dev@gmail.com', password='')
# # ukyt ghoc yvvu nbpv
#
# msg = MIMEMultipart()
# msg['Subject'] = 'Hello'
# msg.attach(MIMEText('Hello, this is a test email from AISEED', 'plain'))
#

msg = EmailMessage()
msg['Subject'] = 'Smart Farming Report'
msg['From'] = 'aiseed.dev@gmail.com'
msg['To'] = get_customer_emails()


# # attach pictures and multiple attachments
# img_data = open('image.jpg', 'rb').read()
# msg.attach(MIMEImage(img_data, name=os.path.basename('image.jpg')))

def send_email(email_content):
    msg.set_content(email_content, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('aiseed.dev@gmail.com', 'ukyt ghoc yvvu nbpv')
        smtp.send_message(msg)

    print('Email sent successfully')


list_farm = get_all_farms()
for farm in list_farm:
    email_content = report_make_up(farm['farm_id'], farm['farm_name'])
    send_email(email_content.replace('\n', ''))
