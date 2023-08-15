from loguru import logger
import time

class FileSaver:
    """
    A class for saving messages to a file.
    """
    
    def save_messages(self, messages):
        """
        Saves messages to a file.
        
        Args:
            messages (list): List of messages to be saved.
        
        Notes:
            This function writes the content of each message in the list to a file named 'messages.txt'.
            Each message's content is written on a new line.
        """
        try:
            with open('messages.txt', 'w', encoding='utf-8') as file:
                for message in messages:
                    file.write(message["content"] + '\n')
                    time.sleep(1)
            logger.info("[FILE SAVER]: messages saved")
        except Exception as e:
            logger.error(f"[FILE SAVER]: {e}")
            raise Exception(e)
