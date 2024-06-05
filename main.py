from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
import smtplib
from datetime import datetime

from db.get_data import *
from render_HTML import generate_report
import schedule
import time

from email_service import EmailService

email_service = EmailService()


def get_user_emails():
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

    return generate_report(farm_name, sensor_data, camera_data)


# # attach pictures and multiple attachments
# img_data = open('image.jpg', 'rb').read()
# msg.attach(MIMEImage(img_data, name=os.path.basename('image.jpg')))


def send_daily_report():
    list_farm = get_all_farms()
    for farm in list_farm:
        email_content = report_make_up(farm['farm_id'], farm['farm_name'])
        email_service.send_email(content=email_content.replace('\n', ''),
                                 subject='AISeed Daily Report',
                                 to=get_user_emails())


# Schedule the job to run every day at 7:00 AM
# schedule.every().day.at("07:00").do(send_daily_report)
send_daily_report()
# while True:
#     schedule.run_pending()
#     time.sleep(1)
