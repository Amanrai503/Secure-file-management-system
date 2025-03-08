from cryptography.fernet import Fernet

# Load the encryption key
with open("secret.key", "rb") as key_file:
    key = key_file.read()

cipher = Fernet(key)
def decrypt_file(filename):
    """Decrypt a file if you have the secret key."""
    with open(filename, "rb") as file:
        encrypted_data = file.read()  # Read encrypted file

    decrypted_data = cipher.decrypt(encrypted_data)  # Decrypt content

    with open(filename[:-4], "wb") as file:  # Remove ".enc"
        file.write(decrypted_data)

    print(f"Decrypted: {filename} → {filename[:-4]}")

# Example usage
decrypt_file("dummy.txt.enc")
