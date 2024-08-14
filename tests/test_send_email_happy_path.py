"""
This test suite helps ensure that your email-sending function operates as expected in various normal scenarios.
"""
import os
import shutil
import tempfile
import unittest
from unittest.mock import MagicMock, mock_open, patch

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from dotenv import load_dotenv

# Importing the send_email function from the correct module
from send_email import send_email


class TestEmailSending(unittest.TestCase):
    """
    Test the send_email function from email_sender module.

    This test suite verifies the correct operation of the email sending function 
    including the creation of email messages with subjects, bodies, and attachments.

    Methods:
        - `test_email_send_success`: Test that an email is sent successfully with correct inputs.
        - `test_email_with_attachment`: Test that an email is sent with the correct attachment.
        - `test_email_subject_and_body`: Test that an email is sent with the correct subject and body.
        - `test_email_multiple_recipients`: Test that an email is sent to multiple recipients.
    """

    def setUp(self):
        """Create a temporary directory and a test file to use as attachment."""
        self.test_dir = tempfile.mkdtemp()
        self.test_file_path = os.path.join(self.test_dir, 'test_attachment.txt')
        with open(self.test_file_path, 'w') as f:
            f.write('This is a test attachment')
        
        # Load environment variables from .env file
        load_dotenv('email.env')
        
        # Set environment variables from the .env file
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.email_address = os.getenv('EMAIL_ADDRESS')

    def tearDown(self):
        """Remove the temporary directory and its contents."""
        shutil.rmtree(self.test_dir)

    @patch('send_email.smtplib.SMTP')
    def test_email_send_success(self, mock_smtp):
        """Test that an email is sent successfully with correct inputs."""
        mock_smtp_instance = mock_smtp.return_value
        mock_smtp_instance.sendmail.return_value = {}

        send_email(
            subject="Test Subject",
            body="This is a test email",
            attachment_path=self.test_file_path
        )

        # Assert that SMTP server was connected
        mock_smtp_instance.login.assert_called_with(self.email_address, self.email_password)
        mock_smtp_instance.sendmail.assert_called_once()

    @patch('send_email.smtplib.SMTP')
    def test_email_with_attachment(self, mock_smtp):
        """Test that an email is sent with the correct attachment."""
        mock_smtp_instance = mock_smtp.return_value
        mock_smtp_instance.sendmail.return_value = {}

        with patch('builtins.open', mock_open(read_data='test attachment content')) as mock_file:
            send_email(
                subject="Test Subject",
                body="This is a test email",
                attachment_path=self.test_file_path
            )
            mock_file.assert_called_with(self.test_file_path, 'rb')

        # Assert that email was sent with the correct attachment
        mock_smtp_instance.sendmail.assert_called_once()

    @patch('send_email.smtplib.SMTP')
    def test_email_subject_and_body(self, mock_smtp):
        """Test that an email is sent with the correct subject and body."""
        mock_smtp_instance = mock_smtp.return_value
        mock_smtp_instance.sendmail.return_value = {}

        subject = "Weather_For_Surfers"
        body = "Good weather is coming, check the forecasting below:"
        send_email(
            subject=subject,
            body=body,
            attachment_path=self.test_file_path
        )

        # Retrieve the MIMEText object that was passed to sendmail
        args, _ = mock_smtp_instance.sendmail.call_args
        msg = args[2]

        # Extract message to parse the actual email content
        msg_obj = MIMEMultipart()
        msg_obj.set_payload(msg)

        # Assert that subject and body are correct
        self.assertIn(subject, msg_obj['Subject'])
        self.assertIn(body, msg_obj.get_payload()[0].get_payload())

    @patch('send_email.smtplib.SMTP')
    def test_email_multiple_recipients(self, mock_smtp):
        """Test that an email is sent to multiple recipients."""
        mock_smtp_instance = mock_smtp.return_value
        mock_smtp_instance.sendmail.return_value = {}

        send_email(
            subject="Test Subject",
            body="This is a test email",
            attachment_path=self.test_file_path
        )

        # Assert that email was sent to multiple recipients
        mock_smtp_instance.sendmail.assert_called_once()
        _, args = mock_smtp_instance.sendmail.call_args
        recipient_emails = args[1]
        self.assertIn("wiechuzw@gmail.com", recipient_emails)
        self.assertIn("l.cichowicz@wp.pl", recipient_emails)
        self.assertIn("piotrek21125@wp.pl", recipient_emails)


if __name__ == '__main__':
    unittest.main()
