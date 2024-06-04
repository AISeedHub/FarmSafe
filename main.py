from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
import smtplib
from datetime import datetime
import yaml

from db.get_data import *
from render_HTML import generate_html
import schedule
import time


def get_customer_emails():
    user = get_all_users()
    emails = [d['email'] for d in user]
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


# read the email and password from a file config.yaml
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)
    email = config['email']
    password = config['password']
msg = EmailMessage()
msg['Subject'] = 'Smart Farming Report'
msg['From'] = email
msg['To'] = get_customer_emails()


# # attach pictures and multiple attachments
# img_data = open('image.jpg', 'rb').read()
# msg.attach(MIMEImage(img_data, name=os.path.basename('image.jpg')))

def send_email(content):
    msg.set_content(content, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email, password)
        smtp.send_message(msg)

    print('Email sent successfully at ', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


def send_daily_report():
    list_farm = get_all_farms()
    for farm in list_farm:
        email_content = report_make_up(farm['farm_id'], farm['farm_name'])
        send_email(email_content.replace('\n', ''))


# Schedule the job to run every day at 7:00 AM
schedule.every().day.at("07:00").do(send_daily_report)
# send_daily_report()
while True:
    schedule.run_pending()
    time.sleep(1)
