from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
import smtplib
import os

to = ['blackhole.large@gmail.com', 'sayney1004@gmail.com']

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
msg['Subject'] = 'Beautiful Subject'
msg['From'] = 'aiseed.dev@gmail.com'
msg['To'] = to

# attach pictures and multiple attachments
img_data = open('image.jpg', 'rb').read()
msg.attach(MIMEImage(img_data, name=os.path.basename('image.jpg')))

msg.set_content('''
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" type="text/css" hs-webfonts="true" href="https://fonts.googleapis.com/css?family=Lato|Lato:i,b,bi">
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style type="text/css">
          h1{font-size:56px}
          h2{font-size:28px;font-weight:900}
          p{font-weight:100}
          td{vertical-align:top}
          #email{margin:auto;width:600px;background-color:#fff}
        </style>
    </head>
    <body bgcolor="#F5F8FA" style="width: 100%; font-family:Lato, sans-serif; font-size:18px;">
    <div id="email">
        <table role="presentation" width="100%">
            <tr>
                <td bgcolor="#00A4BD" align="center" style="color: white;">
                    <h1> AISEED Weekly report!</h1>
                </td>
        </table>
        <table role="presentation" border="0" cellpadding="0" cellspacing="10px" style="padding: 30px 30px 30px 60px;">
            <tr>
                <td>
                    <h2>Custom stylized email</h2>
                    <p>
                        You can add HTML/CSS code here to stylize your emails.
                    </p>
                </td>
            </tr>
        </table>
    </div>
    </body>
    </html>
''', subtype='html')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login('aiseed.dev@gmail.com', '')
    smtp.send_message(msg)

# smtp.sendmail(from_addr="aiseed.dev@gmail.com", to_addrs=to, msg=msg.as_string())
# smtp.quit()

print('Email sent successfully')
