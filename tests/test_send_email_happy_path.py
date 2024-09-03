"""
Test the send_email function from send_email module.

This test suite verifies the correct operation of the email sending function 
including the creation of email messages with attachments.

Methods:
    - `test_email_send_success`: Test that an email is sent successfully with correct inputs.
    - `test_email_with_attachment`: Test that an email is sent with the correct attachment.
    - `test_email_multiple_recipients`: Test that an email is sent to multiple recipients.
"""
import os
import shutil
import tempfile
import unittest
from unittest.mock import patch, mock_open


"""Environment variables set directly to avoid error during import"""
with patch.dict(os.environ, {
    'EMAIL_PASSWORD': 'test_password',
    'EMAIL_ADDRESS': 'test_address@example.com'
}):
    from send_email_old import send_email


class TestEmailSending(unittest.TestCase):
    def setUp(self):
        """Create a temporary directory and a test file to use as attachment."""
        self.test_dir = tempfile.mkdtemp()
        self.test_file_path = os.path.join(self.test_dir, 'test_attachment.txt')
        with open(self.test_file_path, 'w') as f:
            f.write('This is a test attachment')

    def tearDown(self):
        """Remove the temporary directory and its contents."""
        shutil.rmtree(self.test_dir)

    @patch('smtplib.SMTP')
    @patch.dict(os.environ, {'EMAIL_PASSWORD': 'test_password', 'EMAIL_ADDRESS': 'test_address@example.com'})
    def test_email_send_success(self, mock_smtp):
        """Test that an email is sent successfully with correct inputs."""
        mock_smtp_instance = mock_smtp.return_value
        mock_smtp_instance.sendmail.return_value = {}

        send_email(
            subject="Test Subject",
            body="This is a test email",
            attachment_path=self.test_file_path
        )

        """Assert that SMTP server was connected"""
        mock_smtp_instance.login.assert_called_with('test_address@example.com', 'test_password')
        mock_smtp_instance.sendmail.assert_called_once()

    @patch('smtplib.SMTP')
    @patch.dict(os.environ, {'EMAIL_PASSWORD': 'test_password', 'EMAIL_ADDRESS': 'test_address@example.com'})
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

        """Assert that email was sent with the correct attachment"""
        mock_smtp_instance.sendmail.assert_called_once()


    @patch('smtplib.SMTP')
    @patch.dict(os.environ, {'EMAIL_PASSWORD': 'test_password', 'EMAIL_ADDRESS': 'test_address@example.com'})
    def test_email_multiple_recipients(self, mock_smtp):
        """Test that an email is sent to multiple recipients."""
        mock_smtp_instance = mock_smtp.return_value
        mock_smtp_instance.sendmail.return_value = {}

        send_email(
            subject="Test Subject",
            body="This is a test email",
            attachment_path=self.test_file_path
        )

        """Assert that email was sent to multiple recipients"""
        mock_smtp_instance.sendmail.assert_called_once()
        args, kwargs = mock_smtp_instance.sendmail.call_args
        recipient_emails = args[1]
        self.assertIn("wiechuzw@gmail.com", recipient_emails)
        self.assertIn("l.cichowicz@wp.pl", recipient_emails)
        self.assertIn("piotrek21125@wp.pl", recipient_emails)


if __name__ == '__main__':
    unittest.main()
