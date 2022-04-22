from cryptography.fernet import Fernet


def generateKeypair():
    # key generation
    key = Fernet.generate_key()

    #KEY in db ablegen



    #KEY local ablagen -> Temporär erstmal
    with open('Flask/BackendHelper/Keys/filekey.key', 'wb') as filekey:
        filekey.write(key)

    fernet = Fernet(key)
    return fernet


def encryptData(data, fernet):
    return fernet.encrypt(data)


def decryptData(encryptedData, key):
    fernet = Fernet(key)
    return fernet.decrypt(encryptedData)
