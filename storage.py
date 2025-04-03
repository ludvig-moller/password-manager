import os
import json
import base64

from encryption import *

def create_password_manager(name: str, password: str):
    salt, hashed_password = hash_new_password(password)

    data = {
        "hashed_password": hashed_password.hex(),
        "salt": salt.hex(),
        "passwords": {}
    }
    data_bytes = base64.b64encode(json.dumps(data).encode())

    with open(os.getcwd() + f"/data/{name}.dat", "wb") as f:
        f.write(data_bytes)

def get_password_manager_key(name: str, input_password: str):
    with open(os.getcwd() + f"/data/{name}.dat", "rb") as f:
        data_bytes = f.read()
        data = json.loads(base64.b64decode(data_bytes).decode())

    salt = bytes.fromhex(data["salt"])
    hashed_password = bytes.fromhex(data["hashed_password"])
    hashed_input_password = hash_password(input_password, salt)

    if hashed_password != hashed_input_password:
        return False
    
    key = derive_key(input_password, salt)
    return key

def delete_password_manager(name: str):
    os.remove(os.getcwd() + f"/data/{name}.dat")

def get_passwords(manager_name: str, key: bytes):
    with open(os.getcwd() + f"/data/{manager_name}.dat", "r") as f:
        data_bytes = f.read()
        data = json.loads(base64.b64decode(data_bytes).decode())
    
    password_data = data["passwords"]
    for password_id in password_data.keys():
        encrypted_site = bytes.fromhex(password_data[password_id]["site"])
        decrypted_site = decrypt_data(encrypted_site, key)
        password_data[password_id]["site"] = decrypted_site

        encrypted_email = bytes.fromhex(password_data[password_id]["email"])
        decrypted_email = decrypt_data(encrypted_email, key)
        password_data[password_id]["email"] = decrypted_email

        encrypted_password = bytes.fromhex(password_data[password_id]["password"])
        decrypted_password = decrypt_data(encrypted_password, key)
        password_data[password_id]["password"] = decrypted_password
    return password_data

def add_password(manager_name: str, key: bytes, site: str, email: str, password: str):
    encrypted_site = encrypt_data(site, key)
    encrypted_email = encrypt_data(email, key)
    encrypted_password = encrypt_data(password, key)

    new_data = {
        "site": encrypted_site.hex(),
        "email": encrypted_email.hex(),
        "password": encrypted_password.hex()
    }

    with open(os.getcwd() + f"/data/{manager_name}.dat", "rb") as f:
        data_bytes = f.read()
        data = json.loads(base64.b64decode(data_bytes).decode())

    if len(data["passwords"]) == 0:
            id = 0
    else:
            id = int(max(data["passwords"].keys()))+1
    data["passwords"][id] = new_data
    
    with open(os.getcwd() + f"/data/{manager_name}.dat", "wb") as f:
        data_bytes = base64.b64encode(json.dumps(data).encode())
        f.seek(0)
        f.write(data_bytes)

def delete_password(manager_name: str, password_id: int):
    with open(os.getcwd() + f"/data/{manager_name}.dat", "rb") as f:
        data_bytes = f.read()
        data = json.loads(base64.b64decode(data_bytes).decode())
    
    del data["passwords"][password_id]

    with open(os.getcwd() + f"/data/{manager_name}.dat", "wb") as f:
        data_bytes = base64.b64encode(json.dumps(data).encode())
        f.seek(0)
        f.write(data_bytes)

def edit_password(manager_name: str, key: bytes, password_id: int, site: str = None, email: str = None, password: str = None):
    with open(os.getcwd() + f"/data/{manager_name}.dat", "rb") as f:
        data_bytes = f.read()
        data = json.loads(base64.b64decode(data_bytes).decode())
    
    password_data = data["passwords"][password_id]

    if site != None:
        encrypted_site = encrypt_data(site, key)
        password_data["site"] = encrypted_site.hex()
    if password != None:
        encrypted_password = encrypt_data(password, key)
        password_data["password"] = encrypted_password.hex()
    if email != None:
        encrypted_email = encrypt_data(email, key)
        password_data["email"] = encrypted_email.hex()
        
    data["passwords"][password_id] = password_data

    with open(os.getcwd() + f"/data/{manager_name}.dat", "wb") as f:
        data_bytes = base64.b64encode(json.dumps(data).encode())
        f.seek(0)
        f.write(data_bytes)

def get_password_manager_names():
    password_manager_files = os.listdir(os.getcwd() + "/data")
    password_manager_names = []

    if len(password_manager_files) >= 1:
        for file in password_manager_files:
            password_manager_names.append(file.replace(".dat", ""))
    return password_manager_names

def import_password_manager(filepath):
    try:
        filename = filepath.split("/")[-1]

        with open(filepath, "rb") as f:
            file_data = f.read()
        
        with open(os.getcwd() + f"/data/{filename}", "wb") as f:
            f.write(file_data)
        return True
    except:
        return False

def export_password_manager(name, dirpath):
    try:
        with open(os.getcwd() + f"/data/{name}.dat", "rb") as f:
            file_data = f.read()
        
        with open(dirpath + f"/{name}.dat", "wb") as f:
            f.write(file_data)
        return True
    except:
        return False
