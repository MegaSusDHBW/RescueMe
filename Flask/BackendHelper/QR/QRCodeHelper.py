import json
import zlib
from base64 import b64encode, b64decode
import qrcode
from PIL import Image

from Flask.BackendHelper.Cryptography.CryptoHelper import encryptData

import zlib, json, base64

def generateDictForQRCode(user_info):
    qrcode_dict = {}
    if user_info:
        qrcode_dict.update({"email": user_info.email})
    if user_info.healthData:
        qrcode_dict.update({"firstname": user_info.healthData.firstname})
        qrcode_dict.update({"lastname": user_info.healthData.lastname})
        qrcode_dict.update({"organDonorState": user_info.healthData.organDonorState})
        qrcode_dict.update({"bloodGroup": user_info.healthData.bloodGroup})
        qrcode_dict.update({"birthDate": str(user_info.healthData.birthdate)})
    if user_info.emergencyContact:
        qrcode_dict.update({"emergencyEmail": user_info.emergencyContact.email})
        qrcode_dict.update({"emergencyFirstname": user_info.emergencyContact.firstname})
        qrcode_dict.update({"emergencyLastname": user_info.emergencyContact.lastname})
        qrcode_dict.update({"emergencyBirthday": str(user_info.emergencyContact.birthdate)})
        qrcode_dict.update({"emergencyPhone": user_info.emergencyContact.phonenumber})
    if user_info.healthData.allergies:
        allergies = []
        for a in user_info.healthData.allergies:
            allergies.append({"title": a.name})
        qrcode_dict.update({"allergies": allergies})
    if user_info.healthData.diseases:
        diseases = []
        for d in user_info.healthData.diseases:
            diseases.append({"title": d.name})
        qrcode_dict.update({"diseases": diseases})
    if user_info.healthData.vaccines:
        vaccines = []
        for v in user_info.healthData.vaccines:
            vaccines.append({"title": v.name})
        qrcode_dict.update({"vaccines": vaccines})

    return qrcode_dict


def createQRCode(qrcode_dict, fernet):
    data = json.dumps(qrcode_dict).encode('utf-8')
    data = zlib.compress(data)
    data = b64encode(data)
    # daten mit fernet verschlüsseln
    encryptedJSON = encryptData(data, fernet)

    #print(encryptedJSON)

    # bytes in string umwandeln
    encryptedJSON = encryptedJSON.decode('utf-8')
    #print(encryptedJSON)
    qr = qrcode.QRCode(box_size=100, border=1, error_correction=qrcode.constants.ERROR_CORRECT_L, version=1)
    qr.add_data(encryptedJSON)
    logo = Image.open('../static/img/logo-qr.png')

    img = qr.make_image()
    pos = ((img.size[0] - logo.size[0]) // 2,
           (img.size[1] - logo.size[1]) // 2)
    img = qr.make_image()
    img.paste(logo, pos)

    try:
        img.save('../static/img/qrcode.png', 'png', optimize=True)
        return encryptedJSON
    except:
        print("Fehler beim QR-Code-Erzeugen")
