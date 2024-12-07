import os

file_name = "TICKET_BOOK.json"

try:
    # Check if the file exists
    if os.path.exists(file_name):
        os.remove(file_name)
        print(f"File '{file_name}' has been deleted.")
    else:
        print(f"File '{file_name}' does not exist.")
except Exception as e:
    print(f"An error occurred: {e}")
