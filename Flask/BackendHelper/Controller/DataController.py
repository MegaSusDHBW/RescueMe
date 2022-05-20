from datetime import datetime

import what3words
from flask import request, jsonify
from flask_login import login_required

from .token_required import token_required
from ..Location.hospital import get_hospital_query_result
from Models import EmergencyContact, User, HealthData, Allergies, Diseases, Vaccines
from Models.InitDatabase import db


class DataController:
    # proof if already existing

    '''
    Setter
    '''

    @staticmethod
    @token_required
    def setEmergencyContact(current_user):
        contact_json = request.get_json()
        try:
            firstname = contact_json["firstName"]
            lastname = contact_json["lastName"]
            birthdate = contact_json["birthDate"]
            phonenumber = contact_json["phoneNumber"]
            email = contact_json["email"]
            user_mail = current_user

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
    @token_required
    # Param current_user
    def setHealthData(current_user):
        healthdata_json = request.get_json()
        try:
            firstname = healthdata_json["firstName"]
            lastname = healthdata_json["lastName"]
            organDonorState = healthdata_json["organDonorState"]
            bloodGroup = healthdata_json["bloodGroup"]
            user_mail = healthdata_json["userMail"]
            birthdate_str = healthdata_json["birthDate"]
            birthdate = datetime.strptime(birthdate_str, "%d.%m.%Y")
            allergies = healthdata_json["allergies"]
            diseases = healthdata_json["diseases"]
            vaccines = healthdata_json["vaccines"]


            user = User.User.query.filter_by(email=user_mail).first()
            if user:
                if user.healthData is None:
                    new_healthdata = HealthData.HealthData(firstname=firstname, lastname=lastname,
                                                           organDonorState=organDonorState,
                                                           bloodGroup=bloodGroup, birthdate=birthdate, user_id=user.id)
                    db.session.add(new_healthdata)
                    db.session.commit()
                    user = User.User.query.filter_by(email=user_mail).first()
                    for allergy in allergies:
                        new_allergy = Allergies.Allergies(name=allergy['title'], health_id=user.healthData.id)
                        db.session.add(new_allergy)
                        db.session.commit()
                    for disease in diseases:
                        new_disease = Diseases.Diseases(name=disease['title'], health_id=user.healthData.id)
                        db.session.add(new_disease)
                        db.session.commit()
                    for vaccine in vaccines:
                        new_vaccine = Vaccines.Vaccines(name=vaccine['title'], health_id=user.healthData.id)
                        db.session.add(new_vaccine)
                        db.session.commit()
                    db.session.commit()
                else:
                    user_id = User.User.query.filter_by(email=user_mail).first()
                    user_id = user_id.id

                    db.session.query(HealthData.HealthData).filter(
                        HealthData.HealthData.id == user_id).update(
                        {
                            HealthData.HealthData.firstname: firstname,
                            HealthData.HealthData.lastname: lastname,
                            HealthData.HealthData.organDonorState: organDonorState,
                            HealthData.HealthData.bloodGroup: bloodGroup,
                            HealthData.HealthData.birthdate: birthdate
                        },
                        synchronize_session=False)
                    db.session.commit()

                    healthdata_id = HealthData.HealthData.query.filter_by(id=user_id).first()

                    allergies_db = Allergies.Allergies.query.filter_by(health_id=healthdata_id.id).all()
                    diseases_db = Diseases.Diseases.query.filter_by(health_id=healthdata_id.id).all()
                    vaccines_db = Vaccines.Vaccines.query.filter_by(health_id=healthdata_id.id).all()
                    for entry in allergies_db:
                        db.session.delete(entry)
                    for entry in diseases_db:
                            db.session.delete(entry)
                    for entry in vaccines_db:
                            db.session.delete(entry)
                    db.session.commit()

                    for allergy in allergies:
                        new_allergy = Allergies.Allergies(name=allergy['title'], health_id=healthdata_id.id)
                        db.session.add(new_allergy)
                        db.session.commit()
                    for disease in diseases:
                        new_disease = Diseases.Diseases(name=disease['title'], health_id=user.healthData.id)
                        db.session.add(new_disease)
                        db.session.commit()
                    for vaccine in vaccines:
                        new_vaccine = Vaccines.Vaccines(name=vaccine['title'], health_id=user.healthData.id)
                        db.session.add(new_vaccine)
                        db.session.commit()
                    db.session.commit()

            else:
                return jsonify(response="User nicht vorhanden"), 404

            return jsonify(response="Gesundheitsdaten erhalten"), 200
        except:
            return jsonify(response="Fehler beim Anlegen der Gesundheitsdaten"), 404

    '''Getter'''

    @staticmethod
    @token_required
    def getGeodata(current_user):
        try:
            #y = 45
            #x = 45
            json_data = request.get_json()
            y = json_data["coords"]["longitude"]
            x = json_data["coords"]["latitude"]

            print("X: " + str(x))
            print("Y:" + str(y))

            geocoder = what3words.Geocoder("U7LVW2RA")

            res = geocoder.convert_to_3wa(what3words.Coordinates(x, y))
            print(res["words"])

            return jsonify(words=res["words"]), 200
        except:
            return jsonify(words="Fehler beim Umwandeln der Koordinaten in What3Words"), 404

    @staticmethod
    @token_required
    def getHospitals(current_user):
        try:
            #y = 8.691005
            #x = 48.445664
            json_data = request.get_json()
            y = json_data["coords"]["longitude"]
            x = json_data["coords"]["latitude"]

            hospital_json = get_hospital_query_result(x, y)

            return hospital_json, 200
        except:
            return jsonify(words="Fehler beim Umwandeln der Koordinaten in Google API")

    @staticmethod
    @token_required
    # current_user
    def getHealthData(current_user):
        user_email = current_user

        user_data = db.session.query(User.User).filter(User.User.email == user_email).first()

        healthDataJSON = {}
        if user_data is not None:
            if not user_data.healthData:
                healthDataJSON.update({"firstname": ""})
                healthDataJSON.update({"lastname": ""})
                healthDataJSON.update({"organDonorState": ""})
                healthDataJSON.update({"bloodgroup": ""})
                healthDataJSON.update({"birthdate": ""})
                healthDataJSON.update({"allergies": []})
                healthDataJSON.update({"diseases": []})
                healthDataJSON.update({"vaccines": []})
            else:
                healthDataJSON.update({"firstname": user_data.healthData.firstname})
                healthDataJSON.update({"lastname": user_data.healthData.lastname})
                healthDataJSON.update({"organDonorState": user_data.healthData.organDonorState})
                healthDataJSON.update({"bloodgroup": user_data.healthData.bloodGroup})
                healthDataJSON.update({"birthdate": datetime.strftime(user_data.healthData.birthdate, "%d.%m.%Y")})

                allergies_list = []
                diseases_list = []
                vaccines_list = []
                for allergy in user_data.healthData.allergies:
                    allergies_list.append({"title": allergy.name})
                for disease in user_data.healthData.diseases:
                    diseases_list.append({"title": disease.name})
                for vaccine in user_data.healthData.vaccines:
                    vaccines_list.append({"title": vaccine.name})
                healthDataJSON.update({"allergies": allergies_list})
                healthDataJSON.update({"diseases": diseases_list})
                healthDataJSON.update({"vaccines": vaccines_list})

        else:
            print("GET HEALTHDATA User nicht gefunden")

        return jsonify(healthDataJSON), 200

    @staticmethod
    @token_required
    def getEmergencyContact(current_user):
        user_email = current_user,

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
