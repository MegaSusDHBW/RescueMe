import what3words
from flask import request, jsonify
from flask_login import login_required

from ..Location.hospital import get_hospital_query_result
from Models import EmergencyContact, User, HealthData
from Models.InitDatabase import db


class DataController:
    # proof if already existing

    '''
    Setter
    '''

    @staticmethod
    def setEmergencyContact():
        contact_json = request.get_json()
        try:
            firstname = contact_json["firstName"]
            lastname = contact_json["lastName"]
            birthdate = contact_json["birthDate"]
            phonenumber = contact_json["phoneNumber"]
            email = contact_json["email"]
            user_mail = contact_json["userMail"]

            user = User.User.query.filter_by(email=user_mail).first()
            if user:
                if user.emergencyContact is None:
                    new_emergencycontact = EmergencyContact.EmergencyContact(firstname=firstname, lastname=lastname,
                                                                             birthdate=birthdate,
                                                                             phonenumber=phonenumber, email=email,
                                                                             user_id=user.id)
                    db.session.add(new_emergencycontact)
                    db.session.commit()
                else:
                    user_id = User.User.query.filter_by(email=user_mail).first()
                    user_id = user_id.emergencyContact.id

                    db.session.query(EmergencyContact.EmergencyContact).filter(
                        EmergencyContact.EmergencyContact.id == user_id).update(
                        {
                            EmergencyContact.EmergencyContact.email: email,
                            EmergencyContact.EmergencyContact.firstname: firstname,
                            EmergencyContact.EmergencyContact.lastname: lastname,
                            EmergencyContact.EmergencyContact.phonenumber: phonenumber,
                            EmergencyContact.EmergencyContact.birthdate: birthdate
                        })
                    db.session.commit()
            else:
                return jsonify(response="User nicht vorhanden"), 404

            return jsonify(response="Notfallkontakt angelegt"), 200
        except Exception as e:
            print(e)
            return jsonify(response="Fehler beim Anlegen des Notfallkontakts"), 404

    @staticmethod
    def setHealthData():
        healthdata_json = request.get_json()
        try:
            firstname = healthdata_json["firstName"]
            lastname = healthdata_json["lastName"]
            organDonorState = healthdata_json["organDonorState"]
            bloodGroup = healthdata_json["bloodGroup"]
            user_mail = healthdata_json["userMail"]

            user = User.User.query.filter_by(email=user_mail).first()
            if user:
                if user.healthData is None:
                    new_healthdata = HealthData.HealthData(firstname=firstname, lastname=lastname,
                                                           organDonorState=organDonorState,
                                                           bloodGroup=bloodGroup, user_id=user.id)
                    db.session.add(new_healthdata)
                    db.session.commit()
                else:
                    user_id = User.User.query.filter_by(email=user_mail).first()
                    user_id = user_id.emergencyContact.id

                    db.session.query(HealthData.HealthData).filter(
                        HealthData.HealthData.id == user_id).update(
                        {
                            HealthData.HealthData.firstname: firstname,
                            HealthData.HealthData.lastname: lastname,
                            HealthData.HealthData.organDonorState: organDonorState,
                            HealthData.HealthData.bloodGroup: bloodGroup
                        },
                        synchronize_session=False)
                    db.session.commit()
            else:
                return jsonify(response="User nicht vorhanden"), 404

            return jsonify(response="Gesundheitsdaten erhalten"), 200
        except:
            return jsonify(response="Fehler beim Anlegen der Gesundheitsdaten"), 404

    '''Getter'''

    @staticmethod
    def getGeodata():
        try:
            json_data = request.get_json()
            Y = json_data["coords"]["longitude"]
            X = json_data["coords"]["latitude"]

            print("X: " + str(X))
            print("Y:" + str(Y))

            geocoder = what3words.Geocoder("U7LVW2RA")

            res = geocoder.convert_to_3wa(what3words.Coordinates(X, Y))
            print(res["words"])

            return jsonify(words=res["words"]), 200
        except:
            return jsonify(words="Fehler beim Umwandeln der Koordinaten in What3Words"), 404

    @staticmethod
    def getHospitals():
        try:
            json_data = request.get_json()
            Y = json_data["coords"]["longitude"]
            X = json_data["coords"]["latitude"]

            hospital_json = get_hospital_query_result(X, Y)

            return hospital_json, 200
        except:
            return jsonify(words="Fehler beim Umwandeln der Koordinaten in Google API")

    @staticmethod
    def getHealthData():
        user_email = request.args.get("email")

        user_data = db.session.query(User.User).filter(User.User.email == user_email).first()

        healthDataJSON = {}
        if user_data is not None:
            if not user_data.healthData:
                healthDataJSON.update({"firstname": ""})
                healthDataJSON.update({"lastname": ""})
                healthDataJSON.update({"organDonorState": ""})
                healthDataJSON.update({"bloodgroup": ""})
            else:
                healthDataJSON.update({"firstname": user_data.healthData.firstname})
                healthDataJSON.update({"lastname": user_data.healthData.lastname})
                healthDataJSON.update({"organDonorState": user_data.healthData.organDonorState})
                healthDataJSON.update({"bloodgroup": user_data.healthData.bloodGroup})
        else:
            print("GET HEALTHDATA User nicht gefunden")

        return jsonify(healthDataJSON), 200

    @staticmethod
    def getEmergencyContact():
        user_email = request.args.get("email")

        user_data = db.session.query(User.User).filter(User.User.email == user_email).first()

        emergencyContactJSON = {}
        if user_data is not None:
            if not user_data.emergencyContact:
                emergencyContactJSON.update({"emergencyEmail": ""})
                emergencyContactJSON.update({"emergencyFirstname": ""})
                emergencyContactJSON.update({"emergencyLastname": ""})
                emergencyContactJSON.update({"emergencyBirthday": ""})
                emergencyContactJSON.update({"emergencyPhone": ""})
            else:
                emergencyContactJSON.update({"emergencyEmail": user_data.emergencyContact.email})
                emergencyContactJSON.update({"emergencyFirstname": user_data.emergencyContact.firstname})
                emergencyContactJSON.update({"emergencyLastname": user_data.emergencyContact.lastname})
                emergencyContactJSON.update({"emergencyBirthday": user_data.emergencyContact.birthdate})
                emergencyContactJSON.update({"emergencyPhone": user_data.emergencyContact.phonenumber})
        else:
            print("GET EMERGENCYCONTACT User nicht gefunden")
        return jsonify(emergencyContactJSON), 200
