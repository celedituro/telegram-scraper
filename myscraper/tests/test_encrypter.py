import pytest

from ..models.encrypter import Encrypter
from ..models.exceptions import InvalidPassword
    
def test_01_invalid_password_exception():
    encrypter = Encrypter()
    non_string_password = 12345
    with pytest.raises(InvalidPassword):
        encrypter.encrypt_password(non_string_password)
    
def test_02_encrypt_password():
    encrypter = Encrypter()
    original_password = "mypassword"
    encrypted_password = encrypter.encrypt_password(original_password)
    assert encrypted_password != original_password
    assert encrypter.check_password(original_password, encrypted_password)

def test_03_incorrect_password_check():
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
    
def test_05_different_encrypted_passwords():
    encrypter = Encrypter()
    password1 = "mypassword1"
    password2 = "mypassword2"
    encrypted_password1 = encrypter.encrypt_password(password1)
    encrypted_password2 = encrypter.encrypt_password(password2)
    assert encrypted_password1 != encrypted_password2

    

    