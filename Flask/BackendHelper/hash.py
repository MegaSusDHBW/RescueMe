import hashlib
import os

def generateSalt():
    salt = os.urandom(32)
    return salt

def hashPassword(salt, password):
    key = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    return key