#  Copyright (c) 2024. @Aiseed
#  Author: Andrew Lee

import time

from tasks import *
import schedule

from email_service import EmailService

email_service = EmailService()

# send_weekly_report(email_service)

# Schedule the job to run every Friday at 8:00 AM
schedule.every().friday.at("08:00").do(send_weekly_report, email_service)
while True:
    schedule.run_pending()
    time.sleep(1)
