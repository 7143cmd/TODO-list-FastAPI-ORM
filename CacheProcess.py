from cryptography.fernet import Fernet


def load_cipher():
    with open("key.key", 'rb') as f:
        key = f.read()
    return Fernet(key)

def encrypt_password(plain_password):
    f = load_cipher()
    return f.encrypt(plain_password.encode()).decode()

def decode_password(encrypted_password):
    f = load_cipher()
    return f.decrypt(encrypted_password.encode()).decode()

# print(main('007'))