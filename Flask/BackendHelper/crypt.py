import rsa
from cryptography.fernet import Fernet


def generateKeypair(publickey):
    # key generation
    key = Fernet.generate_key()

    # KEY in db ablegen
    dbKey = encryptKeyForDb(publickey, str(key))

    # KEY local ablagen -> Temporär erstmal
    try:
        with open('BackendHelper/Keys/filekey.key', 'wb') as filekey:
            filekey.write(key)
    except:
        with open('Flask/BackendHelper/Keys/filekey.key', 'wb') as filekey:
            filekey.write(key)

    fernet = Fernet(key)
    return fernet


def encryptKeyForDb(publickey, key):
    return rsa.encrypt(key.encode(),
                       publickey)


def decryptKeyForDb(privatekey, encryptedKey):
    return rsa.decrypt(encryptedKey, privatekey).decode()


def encryptData(data, fernet):
    return fernet.encrypt(data)


def decryptData(encryptedData, key):
    fernet = Fernet(key)
    return fernet.decrypt(encryptedData)
