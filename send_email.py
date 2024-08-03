import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


email_password = os.getenv('EMAIL_PASSWORD')
email_address = os.getenv('EMAIL_ADDRESS')


if email_password is None or email_address is None:
    raise ValueError("Zmienne środowiskowe EMAIL_PASSWORD lub EMAIL_ADDRESS nie zostały ustawione")


def send_email(subject, body, attachment_path):
    '''
    The function creates an email message with a given subject and content, and then sends it from a previously defined sender's address to multiple recipients. The message also includes an attachment with weather information.
    '''
    receiver_emails = ["wiechuzw@gmail.com"]#, "l.cichowicz@wp.pl", "piotrek21125@wp.pl"]
    password = email_password

    # Create an email message
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = ", ".join(receiver_emails)
    msg['Subject'] = subject

    # Adding message content
    msg.attach(MIMEText(body, 'plain'))

    # Adding the attachment
    with open(attachment_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={attachment_path}')
        msg.attach(part)

    # Connecting to the SMTP server and sending the message
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_address, password)
        text = msg.as_string()
        server.sendmail(email_address, receiver_emails, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Error occurred while sending the email: {e}")


send_email("Weather_For_Surfers", "Good weather is coming, check the forecasting below:", 'weather_plot.png')