#  Copyright (c) 2024. @Aiseed
#  Author: Andrew Lee
from email.message import EmailMessage
import smtplib
from datetime import datetime
import yaml


class EmailService:
    # The email streams run independently:
    # 1. Send daily report to customers
    # 2. Send alert email to admin when the sensor data exceeds the threshold
    # 3. Send alert email to admin when device is offline: Camera is down or sensor device is not sending data

    def __init__(self):
        """
        Initialize the email service
        """
        pass

    def __read_config(self):
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)
            self.service_email = config['email']
            self.service_password = config['password']

    def send_email(self, content, subject, to):
        """
        Send email to the specified recipients
        :param content: email content
        :param subject: email subject
        :param to: recipients
        """
        self.__read_config()
        self.msg = EmailMessage()
        self.msg['from'] = self.service_email
        self.msg.set_content(content, subtype='html')
        self.msg['Subject'] = subject
        self.msg['To'] = to

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.service_email, self.service_password)
            smtp.send_message(self.msg)

        print('Email sent successfully at ', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
