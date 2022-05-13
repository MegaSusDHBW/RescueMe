import json
import os
import pickle

from flask import request, send_file

from Flask.BackendHelper.Cryptography.CryptoHelper import decryptData, generateFernet, encryptKeyForDb, decryptKeyForDb
from Flask.BackendHelper.QR.QRCodeHelper import generateDictForQRCode, createQRCode
from Models import User, FernetKeys
from Models.InitDatabase import db


class QRCodeController:
    @staticmethod
    def generateQRCode():
        user_mail = request.args.get('email')
        date = request.args.get('date')

        try:
            fernet = generateFernet()
            fernet_encrypted = encryptKeyForDb(publicKey=os.getenv("PUBLICKEY").encode("utf-8"), fernet=pickle.dumps(fernet))

            new_fernet = FernetKeys.FernetKeys(email=user_mail, fernet=fernet_encrypted)
            db.session.add(new_fernet)
            db.session.commit()

            result = db.session.query(User.User).filter(User.User.email == user_mail).all()
            user_info = result[0]
            createQRCode(generateDictForQRCode(user_info), fernet)

            print(generateDictForQRCode(user_info))
            return send_file('../static/img/qrcode.png', mimetype='image/png'), 200
        except Exception as e:
            print(e)
            return send_file('../static/img/dino.png', mimetype='image/png'), 200

    @staticmethod
    def readQRCode():
        user_email = request.args.get('email')
        INPUT = request.args.get('input')

        result = db.session.query(FernetKeys.FernetKeys).filter(FernetKeys.FernetKeys.email == user_email).all()
        user_info = result[0]



        fernet = user_info.fernet
        fernet_rsa_decrypted = decryptKeyForDb(os.getenv('PRIVATEKEY').encode("utf-8"), fernet)
        fernet_decrypted = pickle.loads(fernet_rsa_decrypted)
        print(fernet_decrypted)



        decryptedJSON = decryptData(INPUT, fernet_decrypted)
        data = json.loads(decryptedJSON)
        print(data)

        return 'Decryption success'

        # encryptedJSON = b'gAAAAABias2I9qSxvMH8eg7WT6f3-xrDLgMxIY5yhIQkUU0sy1v_R7-HDa_LdcBGd4v1Tkx27hBnDuwFuGYwjAvtTDSnQDujKiQ_n4GzDexjz08qZGKkBbqz9DFROmZzbBlFtOf1hNvK'

        # with open('BackendHelper/Keys/filekey.key', 'rb') as filekey:
        #    key = filekey.read()

