import json
import pickle

from flask import request, send_file
from flask_cors import cross_origin

from Flask.BackendHelper.Controller.token_required import token_required
from Flask.BackendHelper.Cryptography.CryptoHelper import decryptData, generateFernet, encryptData
from Flask.BackendHelper.QR.QRCodeHelper import generateDictForQRCode, createQRCode

from Models import User, FernetKeys
from Models.InitDatabase import db


class QRCodeController:

    @staticmethod
    @cross_origin()
    @token_required
    def generateQRCode(current_user):
        f"""ernetQuery = db.session.query(GlobalFernet.GlobalFernet).first()

        globalFernet = fernetQuery.fernet
        globalFernet = pickle.loads(globalFernet)"""
        with open('../globalFernetFile.json', 'r') as openfile:
            # Reading from json file
            json_object = json.load(openfile)
        print(json_object["fernet"])
        globalFernet = pickle.loads(json_object["fernet"].encode("iso8859_16"))

        user_mail = request.args.get('email')
        date = request.args.get('date')

        try:
            fernetKey = db.session.query(FernetKeys.FernetKeys).filter_by(email=user_mail).first()
            if fernetKey is not None:
                decryptedFernet = decryptData(fernet=globalFernet,
                                              encryptedData=fernetKey.fernet)

                user_info = db.session.query(User.User).filter(User.User.email == user_mail).first()

                createQRCode(generateDictForQRCode(user_info), pickle.loads(decryptedFernet))

                return send_file('../static/img/qrcode.png', mimetype='image/png'), 200
            else:
                localFernet = generateFernet()

                localFernet = pickle.dumps(localFernet)
                fernet_encrypted = encryptData(fernet=globalFernet,
                                               data=localFernet)

                new_fernet = FernetKeys.FernetKeys(email=user_mail, fernet=fernet_encrypted)
                db.session.add(new_fernet)
                db.session.commit()

                return send_file('../static/img/dino.png', mimetype='image/png'), 200

        except Exception as e:
            print(e)
            return send_file('../static/img/dino.png', mimetype='image/png'), 200

    @staticmethod
    @token_required
    def readQRCode(current_user):
        user_email = request.args.get('email')
        user_data = request.args.get('input')

        # globalFernet
        with open('../globalFernetFile.json', 'r') as openfile:
            # Reading from json file
            json_object = json.load(openfile)
        print(json_object["fernet"])
        globalFernet = pickle.loads(json_object["fernet"].encode("iso8859_16"))

        # LocalFernet
        result = db.session.query(FernetKeys.FernetKeys).filter(FernetKeys.FernetKeys.email == user_email).first()
        localFernet = result.fernet

        decryptedFernet = decryptData(fernet=globalFernet,
                                      encryptedData=localFernet)

        fernet = pickle.loads(decryptedFernet)

        # Data
        decryptedData = decryptData(fernet=fernet,
                                    encryptedData=user_data)

        return decryptedData
