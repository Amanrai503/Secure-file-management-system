from cryptography.fernet import Fernet

# Load the encryption key
with open("secret.key", "rb") as key_file:
    key = key_file.read()

cipher = Fernet(key)

def encrypt_file(filename):
    """Encrypt a file so no one can access it."""
    with open(filename, "rb") as file:
        file_data = file.read()  # Read file content

    encrypted_data = cipher.encrypt(file_data)  # Encrypt the content

    with open(filename + ".enc", "wb") as file:
        file.write(encrypted_data)  # Save encrypted file

    print(f"Encrypted: {filename} → {filename}.enc")

# Example usage
encrypt_file("dummy.txt")
