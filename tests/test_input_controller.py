import sys
import pytest
from unittest.mock import patch
sys.path.append("..")

from scraper.models.input_controller import InputController

def test_01_valid_credentials():
    # Simulates the user input
    with patch('builtins.input', side_effect=['john_doe', 'password123']):
        controller = InputController()
        credentials = controller.get_user_credentials()
        assert credentials is not None
        assert credentials['username'] == 'john_doe'
        assert credentials['password'] == 'password123'

def test_02_empty_credentials():
    with patch('builtins.input', side_effect=['', '']):
        controller = InputController()
        with pytest.raises(ValueError):
            controller.get_user_credentials()

def test_03_whitespace_username():
    with patch('builtins.input', side_effect=['', 'password123']):
        controller = InputController()
        with pytest.raises(ValueError):
            controller.get_user_credentials()

def test_04_whitespace_password():
    with patch('builtins.input', side_effect=['john_doe', '']):
        controller = InputController()
        with pytest.raises(ValueError):
            controller.get_user_credentials()