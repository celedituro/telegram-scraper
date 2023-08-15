import base64
from datetime import datetime
from unittest.mock import Mock
from telethon.tl.types import MessageMediaPhoto, MessageMediaWebPage
import sys
sys.path.append("..")

from scraper.models.parser import MessageParser
from api.models.data_models import MessageType

def test_01_get_photo_content():
    parser = MessageParser()
    photo_bytes = b'example_photo_bytes'
    
    photo_media = MessageMediaPhoto(photo=Mock(sizes=[Mock(bytes=photo_bytes)]))
    expected_result = base64.b64encode(photo_bytes).decode('utf-8')
    result = parser.get_photo_content(photo_media)
    assert result == expected_result

def test_02_get_webpage_content():
    parser = MessageParser()
    url = 'https://example.com'
    
    webpage_media = MessageMediaWebPage(webpage=Mock(url=url))
    result = parser.get_webpage_content(webpage_media)
    assert result == url
    
def test_03_get_message_date():
     parser = MessageParser()
     test_date = datetime(2023, 8, 11, 15, 30)
    
     expected_result = '2023-08-11'
     result = parser.get_message_date(test_date, '%Y-%m-%d')
     assert result == expected_result
    
def test_04_get_message_type_text():
     parser = MessageParser()
     message = Mock(message="Example text message", media=None)
     
     expected_result = MessageType.text
     result = parser.get_message_type(message)
     assert result == expected_result
    
def test_05_get_message_type_photo():
    parser = MessageParser()
    photo_bytes = b'example_photo_bytes'

    photo_media = MessageMediaPhoto(photo=Mock(sizes=[Mock(bytes=photo_bytes)]))
    message = Mock(media=photo_media, message=None)

    expected_result = MessageType.photo
    result = parser.get_message_type(message)
    assert result == expected_result

def test_06_get_message_type_webpage():
    parser = MessageParser()
    url = 'https://example.com'
    
    webpage_media = MessageMediaWebPage(webpage=Mock(url=url))
    message = Mock(message=None, media=webpage_media)
    expected_result = MessageType.link
    
    result = parser.get_message_type(message)
    assert result == expected_result

def test_07_parse_message_text():
    parser = MessageParser()
    
    message = Mock(
        id=1,
        peer_id=Mock(channel_id=2),
        message="Example text message",
        date=datetime(2023, 8, 11, 15, 30),
        media=None
    )
    
    expected_result = {
        "id": 1,
        "channel_id": 2,
        "content": "Example text message",
        "date": "2023-08-11",
        "message_type": MessageType.text
    }
    
    result = parser.parse_message(message)
    assert result == expected_result
    
def test_08_parse_message_link():
    parser = MessageParser()
    
    webpage_media = MessageMediaWebPage(webpage=Mock(url="https://example.com"))    
    message = Mock(
        id=1,
        peer_id=Mock(channel_id=2),
        message=None,
        date=datetime(2023, 8, 11, 15, 30),
        media=webpage_media
    )
    
    expected_result = {
        "id": 1,
        "channel_id": 2,
        "content": "https://example.com",
        "date": "2023-08-11",
        "message_type": MessageType.link
    }
    
    result = parser.parse_message(message)
    assert result == expected_result

def test_09_parse_message_photo():
    parser = MessageParser()
    
    photo_media = MessageMediaPhoto(photo=Mock(sizes=[Mock(bytes=b'example_photo_bytes')]))
    mock_message = Mock(
        id=1,
        peer_id=Mock(channel_id=2),
        message=None,
        date=datetime(2023, 8, 11, 15, 30),
        media=photo_media
    )
    
    expected_result = {
        "id": 1,
        "channel_id": 2,
        "content": base64.b64encode(b'example_photo_bytes').decode('utf-8'),
        "date": "2023-08-11",
        "message_type": MessageType.photo
    }
    result = parser.parse_message(mock_message)
    assert result == expected_result


