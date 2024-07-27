import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from send_email_add import FROM_PASSWORD
from weather_graphs import print_graph

def send_email(subject, body):
    '''
    The function creates an email message with a given subject and content, and then sends it from a previously defined sender's address to multiple recipients. The message also includes weather information. This information is taken from the file: .weather_graphs.py. Uses Gmail SMTP server to sending messages.
    '''
    sender_email = "wieslaw.ziewiecki@gmail.com"
    receiver_emails = ["wiechuzw@gmail.com"]#, "l.cichowicz@wp.pl", "piotrek21125@wp.pl"]
    password = FROM_PASSWORD  

    # Create an email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(receiver_emails)
    msg['Subject'] = subject

    # Adding message content
    msg.attach(MIMEText(body, 'plain'))

    # Adding data from the print_graph function to the message content
    weather_info = print_graph()  
    msg.attach(MIMEText(weather_info, 'plain'))

    # Connecting to the SMTP server and sending the message
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_emails, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Error occurred while sending the email: {e}")

# Send_email function with additional information
send_email("Weather_For_Surfers", "Good weather is coming, check the forecasting below:  ")
