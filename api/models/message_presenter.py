class MessagePresenter:
    """
    A class responsible for presenting and formatting Telegram messages.

    Methods:
        present_message(message): Creates a presentation-ready message dictionary.
        present_all_messages(messages): Creates a list of presentation-ready message dictionaries.
        present_link_messages(link_messages): Creates a list of presentation-ready link message dictionaries.
    """

    def present_message(self, message):
        """
        Creates a presentation-ready message dictionary.

        Args:
            message (tuple): A tuple containing message information.

        Returns:
            dict: A dictionary with message information in a structured format.
        """
        new_message = {
            "id": message[0],
            "channel_id": message[1],
            "content": message[2],
            "date": message[3],
            "message_type": message[4]
        }
        return new_message

    def present_all_messages(self, messages):
        """
        Creates a list of presentation-ready message dictionaries.

        Args:
            messages (list): A list of tuples containing message information.

        Returns:
            list: A list of dictionaries with message information in a structured format.
        """
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
    
    def present_link_messages(self, link_messages):
        """
        Creates a list of presentation-ready link message dictionaries.

        Args:
            link_messages (list): A list of tuples containing link message information.

        Returns:
            list: A list of dictionaries with link message information in a structured format.
        """
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