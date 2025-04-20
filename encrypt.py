import os
from PyQt5.QtWidgets import QMessageBox
from cryptography.fernet import Fernet



def encrypt_file(input_file: str, encryption_key: bytes, current_User_ID: str):
    cipher = Fernet(encryption_key)

    file_name, file_extension = os.path.splitext(input_file)

    # Read the original file
    with open(input_file, "rb") as file:
        file_data = file.read()

    # Add user ID and file extension metadata
    data_with_metadata = f"{current_User_ID}||{file_extension}".encode() + b'||' + file_data

    # Encrypt the data
    encrypted_data = cipher.encrypt(data_with_metadata)

    encrypted_file = file_name + ".crypt"
    with open(encrypted_file, "wb") as file:
        file.write(encrypted_data)

    os.remove(input_file)

def decrypt_file(input_file: str, encryption_key: bytes, current_User_ID: str, parent=None):
    cipher = Fernet(encryption_key)

    # Read the encrypted file
    with open(input_file, "rb") as file:
        encrypted_data = file.read()

    try:
        decrypted_data = cipher.decrypt(encrypted_data)
    except Exception as e:
        QMessageBox.critical(parent, "Access Denied", "🚫 You are not authorized to decrypt this file.")
        return

    parts = decrypted_data.split(b'||', 2)
    if len(parts) != 3:
        QMessageBox.critical(parent, "Invalid Format", "❌ Encrypted file format is invalid.")
        return

    file_user_id = parts[0].decode()
    original_extension = parts[1].decode()
    file_data = parts[2]

    if file_user_id != current_User_ID:
        QMessageBox.warning(parent, "Access Denied", "🚫 You are not authorized to decrypt this file.")
        return

    decrypted_file = input_file.replace(".crypt", "") + original_extension
    with open(decrypted_file, "wb") as file:
        file.write(file_data)

    os.remove(input_file)
    QMessageBox.information(parent, "Success", f"✅ File decrypted successfully: {decrypted_file}")



def encrypt_folder(folder_path: str, encryption_key: bytes, current_User_ID: str, parent=None):
    cipher = Fernet(encryption_key)

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_name, file_extension = os.path.splitext(file)

            try:
                with open(file_path, "rb") as f:
                    file_data = f.read()

                # Add metadata: userID and file extension
                metadata = f"{current_User_ID}||{file_extension}||".encode()
                data_to_encrypt = metadata + file_data

                encrypted_data = cipher.encrypt(data_to_encrypt)
                encrypted_file_path = os.path.join(root, file_name + ".crypt")

                with open(encrypted_file_path, "wb") as f:
                    f.write(encrypted_data)

                os.remove(file_path)

            except Exception as e:
                QMessageBox.critical(parent, "Encryption Error", f"Failed to encrypt {file_path}\nError: {str(e)}")
                return

    QMessageBox.information(parent, "Encryption Complete", f"All files in '{folder_path}' encrypted successfully!")


def decrypt_folder(folder_path: str, encryption_key: bytes, current_User_ID: str, parent=None):
    cipher = Fernet(encryption_key)
    found_encrypted_files = False

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".crypt"):
                found_encrypted_files = True
                file_path = os.path.join(root, file)

                try:
                    with open(file_path, "rb") as f:
                        encrypted_data = f.read()

                    decrypted_data = cipher.decrypt(encrypted_data)

                    # Extract stored UserID and extension
                    metadata, file_data = decrypted_data.split(b'||', 2)[0:2], decrypted_data.split(b'||', 2)[2]
                    stored_user_id = metadata[0].decode()
                    original_extension = metadata[1].decode()

                    if stored_user_id != current_User_ID:
                        QMessageBox.warning(parent, "Access Denied", f"You are not authorized to decrypt: {file}")
                        continue

                    decrypted_file_path = file_path.replace(".crypt", "") + original_extension
                    with open(decrypted_file_path, "wb") as f:
                        f.write(file_data)

                    os.remove(file_path)

                except Exception as e:
                    QMessageBox.critical(parent, "Decryption Error", f"Failed to decrypt {file_path}\nError: {str(e)}")
                    continue

    if not found_encrypted_files:
        QMessageBox.warning(parent, "No Encrypted Files", f"No encrypted files found in '{folder_path}'.")
    else:
        QMessageBox.information(parent, "Decryption Complete", f"All files in '{folder_path}' decrypted successfully!")


#encrypt_folder("Drive\\New folder","xX-_uk9jjpnQ6Jv3bf1qWBRApIyTWMVJIYYpgh934Mc=")
#decrypt_folder("Drive\\New folder","xX-_uk9jjpnQ6Jv3bf1qWBRApIyTWMVJIYYpgh934Mc=")