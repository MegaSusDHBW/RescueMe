import qrcode
from PIL import Image


# https://geekyhumans.com/de/generieren-von-qr-codes-und-barcodes-in-python/
def generateQRCode(encryptedJSON):
    data = encryptedJSON.decode("utf-8")
    qr = qrcode.make(data)

    try:
        #qr.save('BackendHelper/QR/qrcode.png')
        return qr
    except:
        #qr.save('Flask/BackendHelper/QR/qrcode.png')
        print("Fehler beim QR-Code-Erzeugen")