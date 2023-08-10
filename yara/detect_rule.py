import yara

# Load rules from a file
rules = yara.compile(filepath="detect_mercadolibre.yara")

# Scan messages.txt in search of coincidences
matches = rules.match(filepath="messages.txt")

# Read messages file
with open('messages.txt', 'r') as file:
    messages = file.readlines()

# Scan messages with rule
for message in messages:
    matches = rules.match(data=message)
    if matches:
        print(f"MATCH in {message}"+'\n')
