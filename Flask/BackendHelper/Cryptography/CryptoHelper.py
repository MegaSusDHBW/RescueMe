import hashlib
import os
import pickle

import rsa
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from cryptography.fernet import Fernet


def generateFernet():
    # key generation
    key = Fernet.generate_key()

    # TODO KEY in db ablegen, dafür publickey ->
    # dbKey = encryptKeyForDb(publickey, str(key))

    # KEY local ablagen -> Temporär erstmal
    # try:
    with open('BackendHelper/Keys/filekey.key', 'wb') as filekey:
        filekey.write(key)
    #   except:
    #    with open('Flask/BackendHelper/Keys/filekey.key', 'wb') as filekey:
    #        filekey.write(key)

    fernet = Fernet(key)
    return fernet


def encryptKeyForDb(publicKey, fernet):
    encMessage = rsa.encrypt(fernet.encode(),
                             publicKey)
    return encMessage


def decryptKeyForDb(privateKey, encryptedFernet):
    decMessage = rsa.decrypt(encryptedFernet, privateKey).decode()
    return decMessage


def encryptData(data, fernet):
    return fernet.encrypt(data)


def decryptData(encryptedData, fernet):
    return fernet.decrypt(encryptedData)


def generateSalt():
    salt = os.urandom(32)
    return salt


def hashPassword(salt, password):
    key = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    return key
