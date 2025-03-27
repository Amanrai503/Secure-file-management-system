import os
from PyQt5.QtWidgets import QMessageBox
from cryptography.fernet import Fernet

def encrypt_file(input_file: str, encryption_key: bytes):
    cipher = Fernet(encryption_key)


    file_name, file_extension = os.path.splitext(input_file)

    # Read the original file
    with open(input_file, "rb") as file:
        file_data = file.read()


    data_with_extension = f"{file_extension}||".encode() + file_data

    # Encrypt the data
    encrypted_data = cipher.encrypt(data_with_extension)


    encrypted_file = file_name + ".crypt"
    with open(encrypted_file, "wb") as file:
        file.write(encrypted_data)

    os.remove(input_file)

    #print(f"✅ File encrypted successfully: {encrypted_file}")
    #print(f"🗑️ Original file deleted: {input_file}")



def decrypt_file(input_file: str, encryption_key: bytes):
    cipher = Fernet(encryption_key)

    # Read the encrypted file
    with open(input_file, "rb") as file:
        encrypted_data = file.read()


    decrypted_data = cipher.decrypt(encrypted_data)

    original_extension, file_data = decrypted_data.split(b'||', 1)
    original_extension = original_extension.decode()

    decrypted_file = input_file.replace(".crypt", "") + original_extension
    with open(decrypted_file, "wb") as file:
        file.write(file_data)


    os.remove(input_file)


import os
from PyQt5.QtWidgets import QMessageBox
from cryptography.fernet import Fernet

def encrypt_folder(folder_path: str, encryption_key: bytes, parent=None):
    cipher = Fernet(encryption_key)

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)

            file_name, file_extension = os.path.splitext(file)

            # Read file content
            with open(file_path, "rb") as f:
                file_data = f.read()

            # Add extension metadata before encryption
            data_with_extension = f"{file_extension}||".encode() + file_data

            # Encrypt file data
            encrypted_data = cipher.encrypt(data_with_extension)

            # Save encrypted file
            encrypted_file_path = os.path.join(root, file_name + ".crypt")
            with open(encrypted_file_path, "wb") as f:
                f.write(encrypted_data)

            os.remove(file_path)  # Delete original file

    # Show success message
    QMessageBox.information(parent, "Encryption Complete", f"All files in '{folder_path}' encrypted successfully!")


def decrypt_folder(folder_path: str, encryption_key: bytes, parent=None):
    cipher = Fernet(encryption_key)
    found_encrypted_files = False  # Flag to check if any encrypted files exist

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".crypt"):  # Only decrypt encrypted files
                found_encrypted_files = True
                file_path = os.path.join(root, file)

                # Read encrypted content
                with open(file_path, "rb") as f:
                    encrypted_data = f.read()

                # Decrypt data
                decrypted_data = cipher.decrypt(encrypted_data)

                # Extract original extension and file content
                original_extension, file_data = decrypted_data.split(b'||', 1)
                original_extension = original_extension.decode()

                # Restore original filename
                decrypted_file_path = file_path.replace(".crypt", "") + original_extension
                with open(decrypted_file_path, "wb") as f:
                    f.write(file_data)

                os.remove(file_path)  # Delete encrypted file

    # If no encrypted files were found, show a warning message
    if not found_encrypted_files:
        QMessageBox.warning(parent, "No Encrypted Files", f"No encrypted files found in '{folder_path}'.")
    else:
        QMessageBox.information(parent, "Decryption Complete", f"All files in '{folder_path}' decrypted successfully!")


#encrypt_folder("Drive\\New folder","xX-_uk9jjpnQ6Jv3bf1qWBRApIyTWMVJIYYpgh934Mc=")
#decrypt_folder("Drive\\New folder","xX-_uk9jjpnQ6Jv3bf1qWBRApIyTWMVJIYYpgh934Mc=")