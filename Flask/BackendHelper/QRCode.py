import json

import qrcode
from PIL import Image


# https://geekyhumans.com/de/generieren-von-qr-codes-und-barcodes-in-python/
from Flask.BackendHelper.crypt import generateKeypair, encryptData


def generateQRCode(dict, publickey):
    fernet = generateKeypair(publickey)
    data = json.dumps(dict).encode('utf-8')

    encryptedJSON = encryptData(data, fernet)

    qr = qrcode.make(encryptedJSON)

    try:
        qr.save('BackendHelper/QR/qrcode.png')
    except:
        #qr.save('Flask/BackendHelper/QR/qrcode.png')
        print("Fehler beim QR-Code-Erzeugen")