import yara
import os
from loguru import logger

script_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_directory, "..", "app", "messages.txt")

# Load rules from a file
rules = yara.compile(filepath="mercadolibre.yara")

# Scan messages.txt in search of coincidences
matches = rules.match(file_path)

with open(file_path, 'r') as file:
    messages = file.readlines()

# Scan messages with rule
for message in messages:
    matches = rules.match(data=message)
    if matches:
        logger.info(f"MATCH in {message}"+'\n')
