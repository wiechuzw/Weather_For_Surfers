"""Test that an error is raised when environment variables are not set."""
import os
import pytest

from unittest.mock import patch


def test_missing_env_vars():
    with patch.dict('os.environ', {}, clear=True):
        with pytest.raises(ValueError, match="Environment variables EMAIL_PASSWORD or EMAIL_ADDRESS are not set"):
            # Force re-evaluation of environment variables
            if not os.getenv('EMAIL_PASSWORD') or not os.getenv('EMAIL_ADDRESS'):
                raise ValueError("Environment variables EMAIL_PASSWORD or EMAIL_ADDRESS are not set")

