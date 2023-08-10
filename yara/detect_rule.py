import yara
import os

script_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_directory, "..", "app", "messages.txt")

# Load rules from a file
rules = yara.compile(filepath="detect_mercadolibre.yara")

# Scan messages.txt in search of coincidences
matches = rules.match(file_path)

with open(file_path, 'r') as file:
    messages = file.readlines()

# Scan messages with rule
for message in messages:
    matches = rules.match(data=message)
    if matches:
        print(f"MATCH in {message}"+'\n')
