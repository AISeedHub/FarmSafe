#  Copyright (c) 2024. @Aiseed
#  Author: Andrew Lee
from db.repository import *
from render_HTML import *


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


def send_daily_report(email_service):
    list_farm = get_all_farms()
    for farm in list_farm:
        email_content = report_make_up(farm['farm_id'], farm['farm_name'])
        email_service.send_email(content=email_content.replace('\n', ''),
                                 subject='AISeed Daily Report',
                                 to=get_user_emails())


# Send alert email to admin when device is offline: Camera is down or sensor device is not sending data
def send_alert_email(email_service):
    admin_email = get_admin_email()
    # check if the camera is down
    # check if the sensor device is not sending data
    email_service.send_email(content='Camera is down or sensor device is not sending data',
                             subject='Alert: Device is offline',
                             to=admin_email)
