import json

# Read the JSON file
with open('words.json', 'r') as json_file:
    data = json.load(json_file)

# Extract words from the "data" key
words = data["data"]

# Write words to a new Python file
with open('words.py', 'w') as python_file:
    python_file.write('words = [\n')
    for word in words:
        python_file.write(f'    "{word}",\n')
    python_file.write(']\n')
