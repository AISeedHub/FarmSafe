#  Copyright (c) 2024. @Aiseed
#  Author: Andrew Lee
from db.repository import *
from render_HTML import *

TIME_INTERVAL = 60 * 30  # How long the device is considered offline
START_TIME = 6
END_TIME = 19

import pytz

TIMEZONE = pytz.timezone('Asia/Seoul')


def get_user_emails():
    user = get_all_users()
    emails = [d['email'] for d in user]
    return emails


def report_make_up(farm_id, farm_name):
    sensor_device_data = get_latest_sensor_data(farm_id)
    edge_device_data = get_latest_edge_data(farm_id)

    return generate_report(farm_name, sensor_device_data, edge_device_data)


def send_weekly_report(email_service):
    list_farm = get_all_farms()
    for farm in list_farm:
        email_content = report_make_up(farm['farm_id'], farm['farm_name'])
        email_service.send_email(content=email_content.replace('\n', ''),
                                 subject='AISeed Weekly Report',
                                 to=get_user_emails())


def check_sensor_status(farm_id):
    # check if the sensor device is working or not by getting the latest data and comparing with current time
    sensor_device_data = get_latest_sensor_data(farm_id)
    offline_devices = []

    current_time = datetime.now(TIMEZONE).replace(tzinfo=None)

    for device_name in sensor_device_data:
        last_response = sensor_device_data.get(device_name).get('Datetime')
        # if the gap of time between last response and current time is more than 1 hour, device is considered offline
        if (current_time - last_response).seconds > TIME_INTERVAL:
            # convert datetime to string
            offline_devices.append({device_name: last_response.strftime("%Y-%m-%d %H:%M:%S")})
    return offline_devices


def check_camera_status(farm_id):
    # check if the camera is working or not by getting the latest data and comparing with current time
    edge_device_data = get_latest_edge_data(farm_id)
    offline_cameras = []
    current_time = datetime.now(TIMEZONE).replace(tzinfo=None)

    # Schedule the camera to work only in the day time
    if current_time.hour < START_TIME or current_time.hour > END_TIME:
        return offline_cameras

    for camera_name in edge_device_data:
        last_response = edge_device_data.get(camera_name).get('LastResponse')
        # if the gap of time between last response and current time is more than 1 hour, camera is considered offline
        if (current_time - last_response).seconds > TIME_INTERVAL:
            offline_cameras.append({camera_name: last_response.strftime("%Y-%m-%d %H:%M:%S")})
    return offline_cameras


def send_alert_email(email_service):
    admin_email = get_admin_email()
    list_farm = get_all_farms()
    for farm in list_farm:
        offline_sensor_devices = check_sensor_status(farm['farm_id'])
        offline_cameras = check_camera_status(farm['farm_id'])
        if offline_sensor_devices or offline_cameras:
            email_content = f"""
            <h2>Alert: Device Offline</h2>
            <h3>Farm: {farm['farm_name']}</h3>
            <p> <i>Time detected: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} </i></p>
            """
            if len(offline_sensor_devices) > 0:
                email_content += f"<p>Offline Sensor Devices: {offline_sensor_devices}</p>"
            if offline_cameras:
                email_content += f"<p>Offline Cameras: {offline_cameras}</p>"

            # report_content = report_make_up(farm['farm_id'], farm['farm_name'])
            # # send the report all current sensor to admin
            # email_service.send_email(content=report_content.replace('\n', ''),
            #                          subject='AISeed Report',
            #                          to=admin_email)

            email_service.send_email(content=email_content.replace('\n', ''),
                                     subject='AISeed Alert: Device Offline',
                                     to=admin_email)
