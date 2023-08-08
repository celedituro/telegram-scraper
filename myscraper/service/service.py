from datetime import datetime
    
class MessageService:
    def __init__(self, database, parser, presenter):
        self.database = database
        self.parser = parser
        self.presenter = presenter

    async def add_message(self, message):
        parsed_date = self.parser.parse_date(message.date)
        await self.database.insert_message(message.id, message.channel_id, message.content, parsed_date, message.message_type.name)
        return self.presenter.present_message(message)

    def get_all_messages(self):
        messages = self.database.get_all_messages()
        return self.presenter.present_all_messages(messages)

    def get_link_messages(self):
        link_messages = self.database.get_link_messages()
        return self.presenter.present_link_messages(link_messages)


