from cryptography.fernet import Fernet
import hashlib
import base64

KEY_FILE = "key.key"

def generate_key():
    return Fernet.generate_key()

def write_key(key):
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)

def load_key(master_pwd):
    try:
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
            hashed_pwd = hashlib.sha256(master_pwd.encode()).digest()
            return hashlib.pbkdf2_hmac('sha256', hashed_pwd, key, 100000)
    except FileNotFoundError:
        key = generate_key()
        write_key(key)
        return load_key(master_pwd)

def initialize_key(master_pwd):
    return load_key(master_pwd)

print("Welcome to PasswordMgr 25")
master_pwd = input("Masterpassword: ")
key = initialize_key(master_pwd)

try:
    
    key = base64.urlsafe_b64encode(key)
    Fernet(key)
except ValueError as e:
    print("There's a problem with the key:", e)
    print("Make sure the key is correctly generated and stored.")
    exit(1)

fer = Fernet(key)

def show():
    with open('wachtwoorden.txt', 'r') as f:
        for line in f.readlines():
            servicename, data = line.strip().split("|")
            username, password = data.split(",")
            print("Servicename:", servicename, "| Username:", username, "| Password:",
                  fer.decrypt(password.encode()).decode())

def add():
    servicename = input('Servicename: ')
    username = input('Username: ')
    pwd = input('Password: ')
    
    with open('passwds.txt', 'a') as f:
        f.write(servicename + "|" + username + "," + fer.encrypt(pwd.encode()).decode() + "\n")

while True:
    mode = input("Add a new password 'a', show passwords 's' or press 'q' to exit (a/s/q: ").lower()
    if mode == "q":
        print("Thank you for using PasswordMgr 25 1.1.0")
        break
    
    if mode == "s":
        show()
    elif mode == "a":
        add()
    else:
        print("No command found!")
        continue
