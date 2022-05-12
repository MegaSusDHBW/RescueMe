import json

from Flask.BackendHelper.QRCode import generateQRCode
from Flask.BackendHelper.crypt import generateKeypair, encryptData, decryptData

#Testdaten
data = '{"name": "Hans", "alter": 50}'

#Umwandeln von Json in bytes
data = json.dumps(data).encode('utf-8')

#fernet mit key erzeugen
#key ablegen
fernet = generateKeypair("bla")
encryptedJSON = encryptData(data, fernet)
print(encryptedJSON)

#QRCode erzeugen
generateQRCode(encryptedJSON, "pa")

#key holen
with open('Flask/BackendHelper/Keys/filekey.key', 'rb') as filekey:
    key = filekey.read()

#daten entschlüsseln
decryptedJSON = decryptData(encryptedJSON, key)
data = json.loads(decryptedJSON)
print(data)
#

#whats3word