# import subprocess
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# import os
# import toml

# # Load configuration from TOML file
# config = toml.load('Config_file.toml')
# EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
# EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
# SUPPORT_ADDRESS = config['support_address']

# # Validate environment variables
# if not EMAIL_PASSWORD or not EMAIL_ADDRESS:
#     raise ValueError("Environment variables EMAIL_PASSWORD or EMAIL_ADDRESS are not set")

# def send_error_email(program_name, error_message):
#     subject = f"Error in {program_name}"
#     body = f"An error occurred while running {program_name}:\n\n{error_message}"
    
#     msg = MIMEMultipart()
#     msg['From'] = EMAIL_ADDRESS
#     msg['To'] = ", ".join(SUPPORT_ADDRESS)
#     msg['Subject'] = subject
#     msg.attach(MIMEText(body, 'plain'))
    
#     try:
#         with smtplib.SMTP('smtp.gmail.com', 587) as server:
#             server.set_debuglevel(1)  # Enable SMTP debug mode
#             server.starttls()
#             server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
#             server.sendmail(EMAIL_ADDRESS, SUPPORT_ADDRESS, msg.as_string())
#         print(f"Error email sent for {program_name}")
#     except Exception as e:
#         print(f"Failed to send error email: {e}")

# def run_program(command_with_args):
#     try:
#         result = subprocess.run(command_with_args, check=True, capture_output=True, text=True)
#         print(f"{command_with_args[0]} completed successfully")
#         return result.stdout, result.returncode
#     except subprocess.CalledProcessError as e:
#         print(f"{command_with_args[0]} failed with error: {e.stderr}")
#         # Only send email if error code is other than 1
#         if e.returncode != 1:
#             send_error_email(command_with_args[0], e.stderr)
#         return e.stderr, e.returncode

# def main():
#     print("Running weather conditions check...")
#     stdout, returncode = run_program(["python", "checking_conditions.py"])

#     print(f"Output from checking_conditions.py:\n{stdout}")
#     print(f"Return code from checking_conditions.py: {returncode}")
    
#     if "It looks like the wind is coming -> tomorrow" in stdout:
#         weather_message = "It looks like the wind is coming -> tomorrow"
#     elif "After tomorrow cool wind will be expected" in stdout:
#         weather_message = "After tomorrow cool wind will be expected"
#     else:
#         weather_message = "Weather conditions worse than required"

#     if returncode == 0:
#         print("Conditions are good, sending email...")
#         run_program(["python", "send_email.py", "good", weather_message])
#     else:
#         print("Conditions are not met, skipping email sending.")

# if __name__ == '__main__':
#     main()

import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import toml

# Load configuration from TOML file
config = toml.load('Config_file.toml')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
SUPPORT_ADDRESS = config['support_address']

# Validate environment variables
if not EMAIL_PASSWORD or not EMAIL_ADDRESS:
    raise ValueError("Environment variables EMAIL_PASSWORD or EMAIL_ADDRESS are not set")

def send_error_email(program_name, error_message):
    subject = f"Error in {program_name}"
    body = f"An error occurred while running {program_name}:\n\n{error_message}"
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ", ".join(SUPPORT_ADDRESS)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.set_debuglevel(1)  # Enable SMTP debug mode
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, SUPPORT_ADDRESS, msg.as_string())
        print(f"Error email sent for {program_name}")
    except Exception as e:
        print(f"Failed to send error email: {e}")

def run_program(command_with_args):
    try:
        result = subprocess.run(command_with_args, check=True, capture_output=True, text=True)
        print(f"{command_with_args[0]} completed successfully")
        return result.stdout, result.returncode
    except subprocess.CalledProcessError as e:
        print(f"{command_with_args[0]} failed with error: {e.stderr}")
        # Only send email if error code is other than 1
        if e.returncode != 1:
            send_error_email(command_with_args[0], e.stderr)
        return e.stderr, e.returncode

def main():
    print("Running weather conditions check...")
    stdout, returncode = run_program(["python", "checking_conditions.py"])

    print(f"Output from checking_conditions.py:\n{stdout}")
    print(f"Return code from checking_conditions.py: {returncode}")
    
    # Run data_plot.py to generate the weather plot
    print("Generating weather plot...")
    plot_stdout, plot_returncode = run_program(["python", "data_plot.py"])
    
    if plot_returncode != 0:
        print(f"Error while generating weather plot: {plot_stdout}")
        return  # Exit if plot generation failed

    print("Weather plot generated successfully.")
    
    if "It looks like the wind is coming -> tomorrow" in stdout:
        weather_message = "It looks like the wind is coming -> tomorrow"
    elif "After tomorrow cool wind will be expected" in stdout:
        weather_message = "After tomorrow cool wind will be expected"
    else:
        weather_message = "Weather conditions worse than required"

    if returncode == 0:
        print("Conditions are good, sending email...")
        run_program(["python", "send_email.py", "good", weather_message])
    else:
        print("Conditions are not met, skipping email sending.")

if __name__ == '__main__':
    main()