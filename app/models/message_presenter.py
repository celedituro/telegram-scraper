class MessagePresenter:
    
    """
    Presents a message.
    
    Args:
        message: dictionary.
        
    Returns:
        A json object.
    """
    def present_message(self, message):
        new_message = {
            "id": message[0],
            "channel_id": message[1],
            "content": message[2],
            "date": message[3],
            "message_type": message[4]
        }
        return new_message

    """
    Presents a list of messages.
    
    Args:
        messages: list of dictionaries.
        
    Returns:
        A list of json objects.
    """
    def present_all_messages(self, messages):
        new_messages = []
        for message in messages:
            new_message = {
                "id": message[0],
                "channel_id": message[1],
                "content": message[2],
                "date": message[3],
                "message_type": message[4]
            }
            new_messages.append(new_message)
        return new_messages
    
    """
    Presents a list of link messages.
    
    Args:
        messages: list of dictionaries.
        
    Returns:
        A list of json objects.
    """
    def present_link_messages(self, link_messages):
        new_link_messages = []
        for message in link_messages:
            new_link_message = {
                "id": message[0],
                "channel_id": message[1],
                "content": message[2],
                "date": message[3]
            }
            new_link_messages.append(new_link_message)
        return new_link_messages