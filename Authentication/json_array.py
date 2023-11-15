import json
import sys

def file_to_password_json(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return

    passwords = []

    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace and newline characters
        passwords.append(line)

    json_data = json.dumps({"password": passwords}, indent=4)

    with open('passwords.json', 'w') as output_file:
        output_file.write(json_data)

    print("Passwords have been converted to JSON and saved to 'passwords.json'.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
    else:
        input_file = sys.argv[1]
        file_to_password_json(input_file)
