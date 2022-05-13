import json

import qrcode

from Flask.BackendHelper.Cryptography.CryptoHelper import encryptData


def generateDictForQRCode(user_info):
    qrcode_dict = {}
    qrcode_dict.update({"email": user_info.email})
    qrcode_dict.update({"firstname": user_info.healthData.firstname})
    qrcode_dict.update({"lastname": user_info.healthData.lastname})
    qrcode_dict.update({"organDonorState": user_info.healthData.organDonorState})
    qrcode_dict.update({"bloodGroup": user_info.healthData.bloodGroup})
    qrcode_dict.update({"emergencyEmail": user_info.emergencyContact.email})
    qrcode_dict.update({"emergencyFirstname": user_info.emergencyContact.firstname})
    qrcode_dict.update({"emergencyLastname": user_info.emergencyContact.lastname})
    qrcode_dict.update({"emergencyBirthday": user_info.emergencyContact.birthdate})
    qrcode_dict.update({"emergencyPhone": user_info.emergencyContact.phonenumber})

    return qrcode_dict


def createQRCode(qrcode_dict, fernet):
    data = json.dumps(qrcode_dict).encode('utf-8')

    # daten mit fernet verschlüsseln
    encryptedJSON = encryptData(data, fernet)
    print(encryptedJSON)

    # bytes in string umwandeln
    encryptedJSON = encryptedJSON.decode('utf-8')
    qr = qrcode.make(encryptedJSON)

    try:
        qr.save('../static/img/qrcode.png')
    except:
        # qr.save('Flask/BackendHelper/QR/qrcode.png')
        print("Fehler beim QR-Code-Erzeugen")