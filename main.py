from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage

from tasks import *
import schedule

from email_service import EmailService

email_service = EmailService()

# The email streams run independently:
# 1. Send daily report to customers
# 2. Send alert email to admin when the sensor data exceeds the threshold
# 3. Send alert email to admin when device is offline: Camera is down or sensor device is not sending data


# Schedule the job to run every day at 7:00 AM
# schedule.every().day.at("07:00").do(send_daily_report)
send_daily_report(email_service)
# while True:
#     schedule.run_pending()
#     time.sleep(1)
