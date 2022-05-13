import hashlib
import os

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
    RSApublicKey = RSA.importKey(publicKey)
    OAEP_cipher = PKCS1_OAEP.new(RSApublicKey)
    encryptedFernet = OAEP_cipher.encrypt(fernet)
    return encryptedFernet


def decryptKeyForDb(privateKey, encryptedFernet):
    RSAprivateKey = RSA.importKey(privateKey)
    OAEP_cipher = PKCS1_OAEP.new(RSAprivateKey)
    decryptedMsg = OAEP_cipher.decrypt(encryptedFernet)
    return decryptedMsg


def encryptData(data, fernet):
    return fernet.encrypt(data)


def decryptData(encryptedData, key):
    fernet = Fernet(key)
    return fernet.decrypt(encryptedData)


def generateSalt():
    salt = os.urandom(32)
    return salt


def hashPassword(salt, password):
    key = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    return key
