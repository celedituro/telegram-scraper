class Presenter:
    def present_message(self, message):
        return {
            "id": message.id,
            "channel_id": message.channel_id,
            "content": message.content,
            "date": message.date,
            "message_type": message.message_type
        }

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