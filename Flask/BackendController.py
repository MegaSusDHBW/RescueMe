import json

import what3words as what3words
from flask import render_template, Flask

from Flask.BackendHelper.QRCode import generateQRCode
from Flask.BackendHelper.crypt import generateKeypair, encryptData, decryptData


app = Flask(__name__,template_folder='../templates')

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/encrypt")
def encrypt():
    data = '{"name": "Hans", "alter": 50}'
    data = json.dumps(data).encode('utf-8')

    fernet = generateKeypair()
    encryptedJSON = encryptData(data, fernet)
    print(encryptedJSON)

    generateQRCode(encryptedJSON)
    return encryptedJSON

@app.route("/decrypt")
def decrypt():
    encryptedJSON = b'gAAAAABiYsjMXQL5n4ubzAYdf82PRcBXVTT2cfrPGvMUvt4y-Grv3vM4gXh8x7JhpLEIf2A6oCcNFGZ_RwTHKgoQ4hxTqXx72fHctYbBA0wrIZwoHEVCOJvtvraaJx8sclq2jSV79h7F'

    with open('BackendHelper/Keys/filekey.key', 'rb') as filekey:
        key = filekey.read()

    decryptedJSON = decryptData(encryptedJSON, key)
    data = json.loads(decryptedJSON)
    print(data)
    return 'Decryption success'

@app.route("/getGeodata")
def getGeodata():
    # public
    geocoder = what3words.Geocoder("what3words-api-key")

    # eigener Server
    #geocoder = what3words.Geocoder("what3words-api-key", end_point='http://localhost:8080/v3')

    X = 51.484463
    Y = -0.195405

    res = geocoder.convert_to_3wa(what3words.Coordinates(X, Y))
    print(res)

    #Um Worte in Koordinaten umzuwandeln
    #res = geocoder.convert_to_coordinates('prom.cape.pump')
    #print(res)


if __name__ == "__main__":
    app.run()