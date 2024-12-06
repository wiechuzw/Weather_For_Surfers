import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import datetime
import toml

# Load configuration from TOML file
print("Loading configuration...")
try:
    config = toml.load('Config_file.toml')
except Exception as e:
    print(f"Error loading configuration: {e}")
    exit(1)

EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
SUPPORT_ADDRESS = config.get('support_address', [])

# File to store the last email date
LAST_EMAIL_FILE = os.path.join(os.getcwd(), 'last_email_date.txt')

# Validate environment variables
if not EMAIL_PASSWORD or not EMAIL_ADDRESS:
    raise ValueError("Environment variables EMAIL_PASSWORD or EMAIL_ADDRESS are not set")
else:
    print("Environment variables loaded successfully.")


def has_email_been_sent_today():
    """
    Checks if the email has already been sent today by reading the date from LAST_EMAIL_FILE.
    """
    print("Checking if email has been sent today...")
    if not os.path.exists(LAST_EMAIL_FILE):
        print(f"{LAST_EMAIL_FILE} does not exist.")
        return False
    with open(LAST_EMAIL_FILE, 'r') as f:
        last_email_date = f.read().strip()
    return last_email_date == datetime.date.today().strftime('%Y-%m-%d')


def update_last_email_date():
    """
    The function updates the last_email_date.txt file after sending the email
    """
    with open(LAST_EMAIL_FILE, 'w') as f:
        current_date = datetime.date.today().strftime('%Y-%m-%d')
        f.write(current_date)
    print(f"Plik last_email_date.txt zaktualizowany na: {current_date}")


def log_last_email_date():
    """
    Logs the content of the LAST_EMAIL_FILE if it exists.
    """
    if os.path.exists(LAST_EMAIL_FILE):
        with open(LAST_EMAIL_FILE, 'r') as f:
            print("Zawartość last_email_date.txt:", f.read())
    else:
        print("Plik last_email_date.txt nie istnieje.")


def send_error_email(program_name, error_message):
    """
    Sends an email to the support address if there is an error in the program.
    """
    print(f"Preparing to send error email for {program_name}...")
    subject = f"Error in {program_name}"
    body = f"An error occurred while running {program_name}:\n\n{error_message}"
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ", ".join(SUPPORT_ADDRESS)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            print("Connecting to email server...")
            server.set_debuglevel(1)  # Enable SMTP debug mode
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, SUPPORT_ADDRESS, msg.as_string())
        print(f"Error email sent for {program_name}")
    except Exception as e:
        print(f"Failed to send error email: {e}, Program Name: {program_name}, Error Message: {error_message}")


def run_program(command_with_args):
    """
    Executes a subprocess to run a program and returns its output and return code.
    """
    print(f"Running command: {' '.join(command_with_args)}")
    try:
        result = subprocess.run(command_with_args, check=True, capture_output=True, text=True)
        print(f"{command_with_args[0]} completed successfully")
        return result.stdout, result.returncode
    except subprocess.CalledProcessError as e:
        print(f"{command_with_args[0]} failed with error: {e.stderr}")
        if e.returncode != 1:
            send_error_email(command_with_args[0], e.stderr)
        return e.stderr, e.returncode


def main():
    """
    Main function to check weather conditions, generate a plot, and send email if conditions are met.
    """
    print("Starting main program...")

    try:
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

        # Log the current state of the last email date file
        log_last_email_date()

        # Send email if conditions are met and no email has been sent today
        if returncode == 0:
            if not has_email_been_sent_today():
                print("Conditions are good, sending email...")
                run_program(["python", "send_email.py", "good", weather_message])
                update_last_email_date()  # Update the date after sending the email
                log_last_email_date()  # Logujemy zawartość pliku po zaktualizowaniu
            else:
                print("Email has already been sent today. Skipping.")
        else:
            print("Conditions are not met, skipping email sending.")
    
    except Exception as e:
        print(f"An error occurred in main: {e}")


if __name__ == "__main__":
    main()
