import smtplib
import boto3
import ssl
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

s3 = boto3.client('s3')
email_sender = 'hottestparty2022@gmail.com'
email_password = 'jqwrpvclnuzcdeah'
subject = 'WELCOME TO HOLIDAZE!'
body = """
Gracias por formar parte de este evento, adjunto encontrarás tus entradas.

Te recordamos no compartirlas con nadie.

Ubicación: https://maps.app.goo.gl/xkyooEKgAjRR5ECXA?g_st=ic
"""
def load_images(data):
    attachments  = []
    email_receiver = data[0]['email']
    for elem in data:
        response = s3.get_object(Bucket="thehottestpartytickets", Key=elem['s3File'])
        image = response['Body'].read()
        attachments.append({'file': image, 'name': elem['s3File']})

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = f'Hottest Events <{email_sender}>'
    msg['To'] = email_receiver

    text = MIMEText(body)
    msg.attach(text)
    for elem in attachments:
        image = MIMEImage(elem['file'], name=elem['name'])
        msg.attach(image)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, msg.as_string())