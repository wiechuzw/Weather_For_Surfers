import os 
import pytest

from unittest.mock import patch, call


"""Environment variables set directly to avoid error during import"""
with patch.dict(os.environ, {
    'EMAIL_PASSWORD': 'test_password',
    'EMAIL_ADDRESS': 'test_address@example.com'
}):
    from send_email import send_email


@pytest.fixture
def smtp_mock(mocker):
    return mocker.patch('smtplib.SMTP')

def test_email_send_success(smtp_mock):
    """Test that an email is sent successfully with correct inputs."""
    
    # Arrange
    subject = "Test Subject"
    body = "This is a test email body."
    attachment_path = None  # Happy path without attachment
    
    # Act
    send_email(subject, body, attachment_path)
    
    # Assert
    smtp_mock.assert_called_once_with('smtp.gmail.com', 587)


def test_multiple_emails_send(smtp_mock):
    """Test that multiple emails are sent successfully."""
    
    # Arrange
    emails = [
        {"subject": "Test Subject 1", "body": "This is the first test email body.", "attachment_path": None},
        {"subject": "Test Subject 2", "body": "This is the second test email body.", "attachment_path": None},
        {"subject": "Test Subject 3", "body": "This is the third test email body.", "attachment_path": None}
    ]

    # Act
    for email in emails:
        send_email(email['subject'], email['body'], email['attachment_path'])

    # Assert
    """Check that SMTP was called the correct number of times"""
    assert smtp_mock.call_count == len(emails)
    """Check all calls were with the correct parameters"""
    smtp_mock.assert_has_calls([call('smtp.gmail.com', 587)] * len(emails))