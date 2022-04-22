import json

import what3words as what3words
from flask import render_template, Flask

from Flask.BackendHelper.QRCode import generateQRCode
from Flask.BackendHelper.crypt import generateKeypair, encryptData, decryptData



app = Flask(__name__)

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

@app.route("/decrypt")
def decrypt():
    encryptedJSON = ""

    with open('Flask/BackendHelper/Keys/filekey.key', 'rb') as filekey:
        key = filekey.read()

    decryptedJSON = decryptData(encryptedJSON, key)
    data = json.loads(decryptedJSON)
    print(data)

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