"""
Encrypts and decrypts the site passwords stored in the credentials table. It 
uses a single server-side Fernet key, loaded from the ENCRYPTION_KEY. 
"""
import os

# Fernet does the actual scrambling/unscrambling
from cryptography.fernet import Fernet, InvalidToken  



# Builds a Fernet object using our secret key. 
def _get_fernet():
    # reads the key from .env
    key = os.environ.get("ENCRYPTION_KEY")  

    # Turns the key from text into bytes.
    return Fernet(key.encode())



# Encrypts the site password that is in plaintext for storage in the database. 
def encrypt_password(plaintext: str):
    return _get_fernet().encrypt(plaintext.encode()) 



# Decrypts the stored password back to plaintext
def decrypt_password(ciphertext: bytes):
    try:
        return _get_fernet().decrypt(ciphertext).decode()
    except InvalidToken:
        # if it FAILS (wrong key, or the data got corrupted), don't crash the
        # whole app - instead raise our own clearer error message
        raise ValueError("ERROR: Decryption failed. Wrong key or corrupted data")