import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256, Hash
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Creating a hash of the password with a random salt
def hash_new_password(password: str):
    salt = os.urandom(32)

    digest = Hash(SHA256())
    digest.update(salt)
    digest.update(password.encode())
    return salt, digest.finalize()

# Hashing password with the given salt
def hash_password(password: str, salt: bytes):
    digest = Hash(SHA256())
    digest.update(salt)
    digest.update(password.encode())
    return digest.finalize()

# Generating the key with the given password and salt
def derive_key(password: str, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=SHA256(),
        length=32,
        salt=salt,
        iterations=100000
    )
    return kdf.derive(password.encode())

# Encrypting the data
def encrypt_data(data: str, key: bytes):
    iv = os.urandom(16)
    cipher = Cipher(algorithm=algorithms.AES256(key), mode=modes.CFB(iv))
    encryptor = cipher.encryptor()
    encrypted = iv + encryptor.update(data.encode()) + encryptor.finalize()
    return encrypted

# Decrypting the data
def decrypt_data(encrypted_data: bytes, key: bytes):
    iv = encrypted_data[:16]
    cipher = Cipher(algorithm=algorithms.AES256(key), mode=modes.CFB(iv))
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(encrypted_data[16:]) + decryptor.finalize()
    return decrypted.decode()
