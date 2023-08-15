import pytest
import sys
sys.path.append("..")

from api.models.encrypter import Encrypter
from api.exceptions.user_exceptions import InvalidPassword
    
def test_01_encrypt_invalid_password():
    encrypter = Encrypter()
    non_string_password = 12345
    with pytest.raises(InvalidPassword):
        encrypter.encrypt_password(non_string_password)
    
def test_02_encrypt_correct_password():
    encrypter = Encrypter()
    original_password = "mypassword"
    encrypted_password = encrypter.encrypt_password(original_password)
    
    assert encrypted_password != original_password
    assert isinstance(encrypted_password, bytes)
    assert len(encrypted_password) > 0
    
def test_03_check_incorrect_password():
    encrypter = Encrypter()
    original_password = "mypassword"
    encrypted_password = encrypter.encrypt_password(original_password)
    
    assert not encrypter.check_password("wrongpassword", encrypted_password)

def test_04_check_password_not_encrypted():
    encrypter = Encrypter()
    plain_password = '123453636'
    
    with pytest.raises(TypeError) as exc_info:
            encrypter.check_password(plain_password, '123453636')
            
    assert str(exc_info.value) == "Strings must be encoded before checking"
    
def test_05_check_other_encrypted_password():
    encrypter = Encrypter()
    password1 = "mypassword1"
    password2 = "mypassword2"
    encrypted_password1 = encrypter.encrypt_password(password1)
    encrypted_password2 = encrypter.encrypt_password(password2)
    
    assert not encrypter.check_password(password1, encrypted_password2)
    assert not encrypter.check_password(password2, encrypted_password1)

def test_06_check_correct_password():
    encrypter = Encrypter()
    original_password = "mypassword"
    encrypted_password = encrypter.encrypt_password(original_password)

def test_07_encrypt_empty_password():
    encrypter = Encrypter()
    empty_password = ""
    hashed_password = encrypter.encrypt_password(empty_password)
    
    assert hashed_password != empty_password
    assert isinstance(hashed_password, bytes)
    assert len(hashed_password) > 0

def test_08_encrypt_large_password():
    encrypter = Encrypter()
    long_password = "a" * 100
    encrypted_long = encrypter.encrypt_password(long_password)
    
    assert encrypted_long != long_password
    assert isinstance(encrypted_long, bytes)
    assert len(encrypted_long) > 0

def test_09_encrypt_password_with_special_characters():
    encrypter = Encrypter()
    original_password = "$my%password&"
    encrypted_password = encrypter.encrypt_password(original_password)
    
    assert encrypted_password != original_password
    assert isinstance(encrypted_password, bytes)
    assert len(encrypted_password) > 0
    
def test_10_encrypt_none_password():
    encrypter = Encrypter()
    original_password = None
    
    with pytest.raises(InvalidPassword):
        encrypter.encrypt_password(original_password)
