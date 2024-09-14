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


def test_email_missing_subject_or_body(smtp_mock):
    """Test that the function fails when subject or body is missing."""
    
    subject = None
    body = "This is a test email body."
    attachment_path = None
    
    with pytest.raises(ValueError, match="Subject and body are required"):
        send_email(subject, body, attachment_path)
    
    subject = "Test Subject"
    body = None
    
    with pytest.raises(ValueError, match="Subject and body are required"):
        send_email(subject, body, attachment_path)
    

def test_smtp_connection_failure(smtp_mock):
    """Test that an error is raised when the SMTP connection fails."""
    
    """Simulating an exception during a call"""
    smtp_mock.side_effect = Exception("SMTP connection error")
    
    subject = "Test Subject"
    body = "This is a test email body."
    attachment_path = None
    
    with pytest.raises(Exception, match="SMTP connection error"):
        send_email(subject, body, attachment_path) 


@patch('builtins.open', side_effect=FileNotFoundError)
def test_attachment_file_not_found(mock_open, smtp_mock):
    """Test that an error is raised when the attachment file is not found."""
    
    subject = "Test Subject"
    body = "This is a test email body."
    attachment_path = "non_existent_file.txt"
    
    with pytest.raises(FileNotFoundError):
        send_email(subject, body, attachment_path)
    
    smtp_mock.assert_not_called()
    
   
    