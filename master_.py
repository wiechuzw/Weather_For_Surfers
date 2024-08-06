import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
SUPPORT_ADDRESS = ["wieslaw.ziewiecki@gmail.com", "l.cichowicz@wp.pl", "piotrek21125@wp.pl"]

if EMAIL_PASSWORD is None or EMAIL_ADDRESS is None:
    raise ValueError("Zmienne środowiskowe EMAIL_PASSWORD lub EMAIL_ADDRESS nie zostały ustawione")

def send_error_email(program_name, error_message):
    subject = f"Error in {program_name}"
    body = f"An error occurred while running {program_name}:\n\n{error_message}"
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ", ".join(SUPPORT_ADDRESS)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, SUPPORT_ADDRESS, text)
        server.quit()
        print(f"Error email sent for {program_name}")
    except Exception as e:
        print(f"Failed to send error email: {e}")

def run_program(program_name, script_name):
    try:
        result = subprocess.run(["python", script_name], check=True, capture_output=True, text=True)
        print(f"{program_name} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"{program_name} failed with error: {e.stderr}")
        send_error_email(program_name, e.stderr)
        raise

def main():
    try:
        run_program("Data Loading", "data_loading.py")
        run_program("Data Plotting", "data_plot.py")
        run_program("Send Email", "send_email.py")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Execution stopped due to an error")

if __name__ == '__main__':
    main()