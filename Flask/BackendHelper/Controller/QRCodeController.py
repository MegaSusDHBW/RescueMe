import pickle

from flask import request, send_file
from flask_login import login_required

from Flask.BackendHelper.Cryptography.CryptoHelper import decryptData, generateFernet, encryptData
from Flask.BackendHelper.QR.QRCodeHelper import generateDictForQRCode, createQRCode
from Models import User, FernetKeys, GlobalFernet
from Models.InitDatabase import db


class QRCodeController:

    @staticmethod
    @login_required
    def generateQRCode():
        fernetQuery = db.session.query(GlobalFernet.GlobalFernet).first()
        fernetQuery = fernetQuery

        globalFernet = fernetQuery.fernet
        globalFernet = pickle.loads(globalFernet)

        user_mail = request.args.get('email')
        date = request.args.get('date')

        try:
            if db.session.query(FernetKeys.FernetKeys.email).filter_by(email=user_mail).first() is not None:
                fernetQuery = db.session.query(FernetKeys.FernetKeys).filter(
                    FernetKeys.FernetKeys.email == user_mail).all()
                fernetQuery = fernetQuery[0]

                fernetLocal = fernetQuery.fernet
                decryptedFernet = decryptData(fernet=globalFernet,
                                              encryptedData=fernetLocal)

                result = db.session.query(User.User).filter(User.User.email == user_mail).all()
                user_info = result[0]
                createQRCode(generateDictForQRCode(user_info), pickle.loads(decryptedFernet))

                return send_file('../static/img/qrcode.png', mimetype='image/png'), 200
            else:
                localFernet = generateFernet()

                result = db.session.query(User.User).filter(User.User.email == user_mail).all()
                user_info = result[0]
                createQRCode(generateDictForQRCode(user_info), localFernet)

                localFernet = pickle.dumps(localFernet)
                fernet_encrypted = encryptData(fernet=globalFernet,
                                               data=localFernet)

                new_fernet = FernetKeys.FernetKeys(email=user_mail, fernet=fernet_encrypted)
                db.session.add(new_fernet)
                db.session.commit()

                ####
                decryptedFernet = decryptData(fernet=globalFernet,
                                              encryptedData=fernet_encrypted)

                decryptedFernet = pickle.loads(decryptedFernet)
                ####

                print(generateDictForQRCode(user_info))
                return send_file('../static/img/qrcode.png', mimetype='image/png'), 200
        except Exception as e:
            print(e)
            return send_file('../static/img/dino.png', mimetype='image/png'), 200

    @staticmethod
    @login_required
    def readQRCode():
        user_email = request.args.get('email')
        user_data = request.args.get('input')

        # globalFernet
        fernetQuery = db.session.query(GlobalFernet.GlobalFernet).first()
        fernetQuery = fernetQuery
        globalFernet = fernetQuery.fernet
        globalFernet = pickle.loads(globalFernet)

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
