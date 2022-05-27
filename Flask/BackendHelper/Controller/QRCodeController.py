import os
import json
import pickle

from flask import request, send_file,jsonify
from flask_cors import cross_origin

import jwt

from Flask.BackendHelper.Controller.token import token_required, param_required
from Flask.BackendHelper.Cryptography.CryptoHelper import decryptData, generateFernet, encryptData
from Flask.BackendHelper.QR.QRCodeHelper import generateDictForQRCode, createQRCode
from Flask.BackendHelper.mail.mailhandler import sendEmergencyMail

from Models import User, FernetKeys, FernetData
from Models.InitDatabase import db


class QRCodeController:

    @staticmethod
    @cross_origin()
    @param_required
    # Param current_user
    def generateQRCode(current_user):
        """fernetQuery = db.session.query(GlobalFernet.GlobalFernet).first()

        globalFernet = fernetQuery.fernet
        globalFernet = pickle.loads(globalFernet)"""

        '''f#get jwt from request args
        token = None
        token = request.args.get('jwt')
        if not token:
            return jsonify({'message': 'a valid token is missing'}), 401
        try:
            data = jwt.decode(token, os.getenv('secret_key'), algorithms=['HS256'])
            user = User.User.query.filter_by(email=data['email']).first()
            if user:
                current_user = data['email']
            else:
                return jsonify({'message': 'Token seems to have non existent User'}), 401
        except Exception as e:
            return jsonify({'message': 'token is invalid', 'error': str(e)}), 401'''


        with open('../globalFernetFile.json', 'r') as openfile:
            # Reading from json file
            json_object = json.load(openfile)
        print(json_object["fernet"])
        globalFernet = pickle.loads(json_object["fernet"].encode("iso8859_16"))

        user_mail = current_user
        date = request.args.get('date')

        try:
            fernetKey = db.session.query(FernetKeys.FernetKeys).filter_by(email=user_mail).first()
            if fernetKey is not None:
                decryptedFernet = decryptData(fernet=globalFernet,
                                              encryptedData=fernetKey.fernet)

                user_info = db.session.query(User.User).filter(User.User.email == user_mail).first()

                data = createQRCode(generateDictForQRCode(user_info), pickle.loads(decryptedFernet))

                exists = db.session.query(FernetData.FernetData).filter_by(data=data).first()
                if exists is None:
                    newFernetData = FernetData.FernetData(data=data, fernet=fernetKey.fernet)
                    db.session.add(newFernetData)
                    db.session.commit()

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
    #@token_required
    def readQRCode():
        #user_email = current_user
        user_data = request.json['input']

        # globalFernet
        with open('../globalFernetFile.json', 'r') as openfile:
            # Reading from json file
            json_object = json.load(openfile)
        print(json_object["fernet"])
        globalFernet = pickle.loads(json_object["fernet"].encode("iso8859_16"))

        test = db.session.query(FernetData.FernetData).all()
        #print(test)
        # LocalFernet
        result = db.session.query(FernetData.FernetData).filter(FernetData.FernetData.data == user_data.encode()).first()
        if result:
            localFernet = result.fernet

            decryptedFernet = decryptData(fernet=globalFernet,
                                          encryptedData=localFernet)

            fernet = pickle.loads(decryptedFernet)

            # Data
            decryptedData = decryptData(fernet=fernet,
                                        encryptedData=user_data.encode('utf-8'))

            email_query = db.session.query(FernetKeys.FernetKeys).filter(
                FernetKeys.FernetKeys.fernet == result.fernet).first()
            email = email_query.email
            user = db.session.query(User.User).filter(User.User.email == email).first()
            sendEmergencyMail(user.emergencyContact.email, user.emergencyContact.firstname,
                              user.emergencyContact.lastname, user.healthData.firstname, user.healthData.lastname)

            return decryptedData.decode('utf-8')
        else:
            print("Kein passenden Eintrag in der DB gefunden")
