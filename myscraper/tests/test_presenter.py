from ..models.presenter import Presenter
from datetime import datetime
from ..models.message import Message, MessageType

def test_01_present_message():
    presenter = Presenter()
    message = Message(id=1, channel_id=123, content="Hello, world!", date="2023-08-08", message_type=MessageType.text)
    
    presented_message = presenter.present_message(message)
    assert presented_message["id"] == 1
    assert presented_message["channel_id"] == 123
    assert presented_message["content"] == "Hello, world!"
    assert presented_message["date"] == "2023-08-08"
    assert presented_message["type"] == "text"

def test_02_present_all_messages():
    presenter = Presenter()
    messages = [
        (1, 123, "Message 1", "2023-08-08", "text"),
        (2, 456, "Message 2", "2023-08-09", "photo")
    ]
    presented_messages = presenter.present_all_messages(messages)

    assert len(presented_messages) == 2
    assert presented_messages[0]["id"] == 1
    assert presented_messages[0]["channel_id"] == 123
    assert presented_messages[0]["content"] == "Message 1"
    assert presented_messages[0]["date"] == "2023-08-08"
    assert presented_messages[0]["type"] == "text"
    assert presented_messages[1]["id"] == 2
    assert presented_messages[1]["channel_id"] == 456
    assert presented_messages[1]["content"] == "Message 2"
    assert presented_messages[1]["date"] == "2023-08-09"
    assert presented_messages[1]["type"] == "photo"
    
def test_03_present_link_messages():
    presenter = Presenter()
    link_messages = [
        (1, 123, "https://example.com", "2023-08-08", "link"),
        (2, 456, "https://another-example.com", "2023-08-09", "link")
    ]
    presented_link_messages = presenter.present_link_messages(link_messages)

    assert len(presented_link_messages) == 2
    assert presented_link_messages[0]["id"] == 1
    assert presented_link_messages[0]["channel_id"] == 123
    assert presented_link_messages[0]["content"] == "https://example.com"
    assert presented_link_messages[0]["date"] == "2023-08-08"

def test_04_present_empty_all_messages():
    presenter = Presenter()
    messages = []
    presented_messages = presenter.present_all_messages(messages)

    assert len(presented_messages) == 0

def test_05_present_empty_link_messages():
    presenter = Presenter()
    messages = []
    presented_messages = presenter.present_link_messages(messages)

    assert len(presented_messages) == 0