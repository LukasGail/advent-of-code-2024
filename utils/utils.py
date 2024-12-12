import os
import time
from cryptography.fernet import Fernet
import re


def load_data(file_name):
    input_path = os.path.join(os.path.dirname(__file__), f'../inputs/{file_name}')
    with open(input_path, 'r') as file:
        data = file.read()
    return data

def time_decorator(func):
    def wrapper(*args, **kwargs):
        # start_cpu = time.process_time()
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        # end_cpu = time.process_time()
        end_time = time.perf_counter()
        result_time = end_time - start_time
        print(f"{func.__name__} needed {result_time:.6f} seconds.")
        return result  # Func result
    return wrapper

# ============= Encryption/Decryption =============

def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file: # wb binary key
        key_file.write(key)


def load_key(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError("Key file not found.")
    return open(file_path, "rb").read()


def en_decrypt_file(file_path, key_file, encrypt: bool = True, override_file: bool = False, remove_extension: str = "", add_extension: str = ".enc"):
    new_path: str = file_path
    if str(file_path).endswith(remove_extension):
        new_path = str(file_path)[:len(file_path) - len(remove_extension)]
    new_path = new_path + add_extension
    if not override_file and os.path.exists(new_path):
        raise FileExistsError(f"File {new_path} already exists.")

    fernet = Fernet(key_file)
    with open(file_path, "rb") as file:
        data = file.read()

    en_decrypted_data = fernet.encrypt(data) if encrypt else fernet.decrypt(data)
    with open(new_path, "wb") as file:
        file.write(en_decrypted_data)


def en_decrypt_file_types(folder_path, key_path, encrypt: bool = True, override_file: bool = False, regex_file_match: str = r".+(\.txt)$", remove_extension: str = "", add_extension: str = ".enc"):
    keyfile = load_key(key_path)
    for file_name in os.listdir(folder_path):
        if re.match(regex_file_match, str(file_name)):
            file_path = os.path.join(folder_path, file_name)
            try:
                en_decrypt_file(file_path, keyfile, encrypt, override_file, remove_extension, add_extension)
                print(f"Encrypted: {file_name}" if encrypt else f"Decrypted: {file_name}")
            except FileExistsError as e:
                print(f"Skipped file {file_name}. {e}")



class ListNode:
    def __init__(self, value=None):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.length = 0
        self.head = None
        self.tail = None

    def append(self, value):
        new_node = ListNode(value)
        if self.length > 0:
            self.tail.next = new_node
            self.tail = new_node
        else:
            self.head = new_node
            self.tail = new_node
        self.length += 1