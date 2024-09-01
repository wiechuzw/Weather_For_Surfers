import os
import smtplib
import toml
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import sys

# Load configuration from TOML file
config = toml.load('Config_file.toml')
receiver_emails = config['receiver_emails']

# Retrieve email credentials from environment variables
email_password = os.getenv('EMAIL_PASSWORD')
email_address = os.getenv('EMAIL_ADDRESS')

if not email_password or not email_address:
    raise ValueError("Environment variables EMAIL_PASSWORD or EMAIL_ADDRESS are not set")

def send_email(subject, body, attachment_path):
    """
    Create and send an email with the specified subject, body, and attachment.
    """
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = ", ".join(receiver_emails)
    msg['Subject'] = subject
    
    # Attach the body text
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach the file
    if attachment_path:
        try:
            with open(attachment_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
                msg.attach(part)
        except IOError as e:
            print(f"Error opening attachment file: {e}")
            return
    
    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(email_address, email_password)
            server.sendmail(email_address, receiver_emails, msg.as_string())
        print("Email sent successfully")
    except Exception as e:
        print(f"Error occurred while sending the email: {e}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("No weather message provided")
        sys.exit(1)

    weather_message = sys.argv[1]
    send_email("Weather_For_Surfers", weather_message, 'weather_plot.png')