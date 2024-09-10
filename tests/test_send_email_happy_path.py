import os 
import pytest

from unittest.mock import patch


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
    """
    Test that an email is sent successfully with correct inputs.
    """
    # Arrange
    subject = "Test Subject"
    body = "This is a test email body."
    attachment_path = None  # Happy path without attachment
    
    # Act
    send_email(subject, body, attachment_path)
    
    # Assert
    smtp_mock.assert_called_once_with('smtp.gmail.com', 587)