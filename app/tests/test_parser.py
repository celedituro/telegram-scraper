import base64
from datetime import datetime
from unittest.mock import Mock
from telethon.tl.types import MessageMediaPhoto, MessageMediaWebPage

from ..models.parser import MessageParser
from ..models.message import MessageType

def test_01_get_photo_content():
    parser = MessageParser()
    photo_bytes = b'example_photo_bytes'
    
    expected_result = base64.b64encode(photo_bytes).decode('utf-8')
    result = parser.get_photo_content(photo_bytes)
    assert result == expected_result

def test_02_get_message_date():
    parser = MessageParser()
    test_date = datetime(2023, 8, 11, 15, 30)
    
    expected_result = '2023-08-11'
    result = parser.get_message_date(test_date, '%Y-%m-%d')
    assert result == expected_result
    
def test_03_get_message_type_text():
    parser = MessageParser()
    message = Mock(message="Example text message", media=None)
    
    expected_result = MessageType.text
    result = parser.get_message_type(message)
    assert result == expected_result
    
def test_04_get_message_type_text_with_special_character():
    parser = MessageParser()
    message = Mock(message="Ex!m%lee?t&/$ge", media=None)
    
    expected_result = MessageType.text
    result = parser.get_message_type(message)
    assert result == expected_result

def test_05_get_message_type_photo():
    parser = MessageParser()

    mock_photo_media = Mock()
    mock_photo_media.__class__ = MessageMediaPhoto
    mock_message = Mock(media=mock_photo_media, message=None)

    expected_result = MessageType.photo
    result = parser.get_message_type(mock_message)
    assert result == expected_result

def test_06_get_message_type_webpage():
    parser = MessageParser()
    
    webpage_media = Mock(webpage=Mock(url="https://example.com"))
    webpage_media.__class__ = MessageMediaWebPage
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
    
    webpage_media = Mock(webpage=Mock(url="https://example.com"))
    webpage_media.__class__ = MessageMediaWebPage
    
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
    
    mock_photo_size = Mock(bytes=b'example_photo_bytes')
    mock_photo = Mock(sizes=[mock_photo_size])
    mock_media = Mock(photo=mock_photo)
    mock_media.__class__ = MessageMediaPhoto

    mock_message = Mock(
        id=1,
        peer_id=Mock(channel_id=2),
        message=None,
        date=datetime(2023, 8, 11, 15, 30),
        media=mock_media
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

def test_10_parse_message_unicode():
    parser = MessageParser()
    
    unicode_message = Mock(
        id=1,
        peer_id=Mock(channel_id=2),
        message="¡Hola, mundo! 😃",
        date=datetime(2023, 8, 11, 15, 30),
        media=None
    )
    expected_result_unicode = {
        "id": 1,
        "channel_id": 2,
        "content": "¡Hola, mundo! 😃",
        "date": "2023-08-11",
        "message_type": MessageType.text
    }
    
    result_unicode = parser.parse_message(unicode_message)
    assert result_unicode == expected_result_unicode
    
def test_11_parse_message_emojis():
    parser = MessageParser()

    emoji_message = Mock(
        id=2,
        peer_id=Mock(channel_id=3),
        message="🚀 ¡Vamos a despegar! 🌕",
        date=datetime(2023, 8, 11, 16, 30),
        media=None
    )
    expected_result_emoji = {
        "id": 2,
        "channel_id": 3,
        "content": "🚀 ¡Vamos a despegar! 🌕",
        "date": "2023-08-11",
        "message_type": MessageType.text
    }
    
    result_emoji = parser.parse_message(emoji_message)
    assert result_emoji == expected_result_emoji

def test_12_do_not_parse_message_service_message():
    parser = MessageParser()
    
    service_message = Mock(
        id=3,
        peer_id=Mock(channel_id=4),
        message=None,
        date=datetime(2023, 8, 11, 17, 30),
        media=None,
    )
    
    result_service_message = parser.parse_message(service_message)
    assert result_service_message is None
    
def test_13_get_message_date_formats():
    parser = MessageParser()

    date_format_1 = '2023-08-11 15:30:45'
    date_1 = datetime.strptime(date_format_1, '%Y-%m-%d %H:%M:%S')
    result_1 = parser.get_message_date(date_1, '%Y-%m-%d %H:%M:%S')
    assert result_1 == date_format_1

    date_format_2 = '2023/08/11 15:30'
    date_2 = datetime.strptime(date_format_2, '%Y/%m/%d %H:%M')
    result_2 = parser.get_message_date(date_2, '%Y/%m/%d %H:%M')
    assert result_2 == date_format_2

def test_14_parse_message_photo_with_more_sizes():
    parser = MessageParser()
    
    mock_photo_size1 = Mock(bytes=b'example_photo_bytes')
    mock_photo_size2 = Mock(bytes=b'other')
    mock_photo = Mock(sizes=[mock_photo_size1, mock_photo_size2])
    mock_media = Mock(photo=mock_photo)
    mock_media.__class__ = MessageMediaPhoto

    mock_message = Mock(
        id=1,
        peer_id=Mock(channel_id=2),
        message=None,
        date=datetime(2023, 8, 11, 15, 30),
        media=mock_media
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
    
def test_15_get_message_content_webpage_with_large_url():
    parser = MessageParser()

    long_url = 'https://example.com/' + 'a' * 100
    mock_webpage_media_long = Mock(webpage=Mock(url=long_url))
    mock_webpage_media_long.__class__ = MessageMediaWebPage
    mock_message_long = Mock(message=None, media=mock_webpage_media_long)
    result_long = parser.get_message_content(mock_message_long)
    assert result_long == long_url

def test_16_get_message_content_webpage_with_url_with_params():
    parser = MessageParser()
    
    url_with_params = 'https://example.com/page?param1=value1&param2=value2'
    mock_webpage_media_params = Mock(webpage=Mock(url=url_with_params))
    mock_webpage_media_params.__class__ = MessageMediaWebPage
    mock_message_params = Mock(message=None, media=mock_webpage_media_params)
    result_params = parser.get_message_content(mock_message_params)
    assert result_params == url_with_params
    
def test_17_get_message_content_long_text():
    parser = MessageParser()

    long_text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. ' + 'a' * 1000
    mock_message_long_text = Mock(message=long_text, media=None)
    result_long_text = parser.get_message_content(mock_message_long_text)
    assert result_long_text == long_text



