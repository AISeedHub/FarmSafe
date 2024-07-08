#  Copyright (c) 2024. @Aiseed
#  Author: Andrew Lee

import time

from tasks import *

from email_service import EmailService

CHECKING_INTERVAL = 60 * 60  # every 30 minutes check the status of the sensor devices and cameras

import schedule

email_service = EmailService()

# every 30 minutes check the status of the sensor devices and cameras and send alert email if any device is offline
# schedule.every(10).seconds.do(send_alert_email, email_service)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
while True:
    print(datetime.now())
    send_alert_email(email_service)
    print('-' * 50)
    time.sleep(CHECKING_INTERVAL)
