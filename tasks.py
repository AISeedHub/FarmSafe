#  Copyright (c) 2024. @Aiseed
#  Author: Andrew Lee
from db.repository import *
from render_HTML import *

TIME_INTERVAL = 60 * 30  # How long the device is considered offline
# Schedule the camera to work only in the day time
START_TIME = 7  # 7 AM in the morning
END_TIME = 19  # 7 PM in the evening


def get_user_emails():
    user = get_all_users()
    emails = [d['email'] for d in user]
    return emails


def get_developer_email():
    emails = []
    user = get_all_users()
    for u in user:
        if u['role'] == 'developer':
            emails.append(u['email'])
    return emails


def get_admin_email():
    emails = []
    user = get_all_users()
    for u in user:
        if u['role'] == 'admin':
            emails.append(u['email'])
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
        print("Sent email to all users about the weekly report at farm: ", farm['farm_name'], " at ", datetime.now())


def check_sensor_status(farm_id):
    # check if the sensor device is working or not by getting the latest data and comparing with current time
    sensor_device_data = get_latest_sensor_data(farm_id)
    offline_devices = []

    current_time = datetime.now()

    for device_name in sensor_device_data:
        last_response = sensor_device_data.get(device_name).get('Datetime')
        # if the gap of time between last response and current time is more than 1 hour, device is considered offline
        print(f"-check_sensor_status at {farm_id} waiting: ", (current_time - last_response).seconds // 60, " minutes")
        if (current_time - last_response).seconds > TIME_INTERVAL:
            print("!!Device offline: ", device_name, " from farm: ", farm_id, " last response: ", last_response,
                  " current time: ", current_time)
            print("Time difference: ", (current_time - last_response).seconds)
            # convert datetime to string
            offline_devices.append({"Name: ": device_name,
                                    "Farm": farm_id,
                                    "LastResponse": last_response.strftime("%Y-%m-%d %H:%M:%S")})
    return offline_devices


def check_camera_status(farm_id):
    # check if the camera is working or not by getting the latest data and comparing with current time
    edge_device_data = get_latest_edge_data(farm_id)
    offline_cameras = []
    current_time = datetime.now()

    # Schedule the camera to work only in the day time
    if current_time.hour < START_TIME or current_time.hour > END_TIME:
        return offline_cameras

    for camera_name in edge_device_data:
        last_response = edge_device_data.get(camera_name).get('LastResponse')
        print(f"-check_camera_status at {farm_id} waiting: ", (current_time - last_response).seconds // 60, " minutes")
        # if the gap of time between last response and current time is more than 1 hour, camera is considered offline
        if (current_time - last_response).seconds > TIME_INTERVAL:
            print("!!Camera offline: ", camera_name, " from farm: ", farm_id, " last response: ", last_response,
                  " current time: ", current_time)
            offline_cameras.append({"Name: ": camera_name,
                                    "Farm": farm_id,
                                    "IP": edge_device_data.get(camera_name).get('IP'),
                                    "LastResponse": last_response.strftime("%Y-%m-%d %H:%M:%S"),
                                    })
    return offline_cameras


def send_alert_email(email_service):
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
                                     to=get_admin_email())
            print("Sent email to admin about offline devices at farm: ", farm['farm_name'], " at ", datetime.now())
