import json
import string, os, random
import datetime
from fastapi_mail import FastMail
import jwt
from bson import json_util
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.hash import bcrypt
from starlette import status
from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse

from configs.configurations import MONGODB_URL, MONGODB_DB_NAME, SUBJECT, ISS
from user.user_model import UserInDB, login, UpdatePasswd, DataUploadModel


async def signUpFun(user: UserInDB):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("Users")
    row = await collection.find_one({"username": user.username})
    if row:
        return {"message": "userExists"}
    else:
        usr = {'username': user.username, 'role': user.role,  'firstName': user.firstName,
               'lastName': user.lastName, 'securityQuestion':user.securityQuestion, 'securityAnswer':user.securityAnswer,
               'password': bcrypt.hash(user.password)}

        dbuser = UserInDB(**usr)
        collection.insert_one(dbuser.dict())

    return {"message": "userCreated"}


async def loginFun(user: login):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("Users")
    row = await collection.find_one({"username": user.username})
    if row:
        mpassword = row['password']
        if bcrypt.verify(user.password, mpassword):
            token = jwt.encode(
                {'user': user.username, 'scope': row['role'], 'iss': ISS,
                 'sub': SUBJECT,
                 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)},
                'SECRET_KEY')

            return {'message': 'True', 'token': token, 'username': user.username}
    return {'message':"False"}
    # return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content="Authentication Failed")

async def updatePassword(user: UpdatePasswd):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("Users")
    row = await collection.find_one({"username": user.username, 'securityQuestion': user.securityQuestion, 'securityAnswer': user.securityAnswer})
    if row:
        await collection.update_one({'username': user.username},
                                    {'$set': {'password': bcrypt.hash(user.password)}})
        return {"message": "passwordUpdated"}
    return {"message": "verification code mismatch"}

async def dataUpload(data: DataUploadModel):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("Data")
    usr = {"h1n1_concern":data.h1n1_concern,"h1n1_knowledge":data.h1n1_knowledge,"behavioral_antiviral_meds":data.behavioral_antiviral_meds,"behavioral_avoidance":data.behavioral_avoidance,"behavioral_face_mask":data.behavioral_face_mask,"behavioral_wash_hands":data.behavioral_wash_hands,"behavioral_large_gatherings":data.behavioral_large_gatherings,"behavioral_outside_home":data.behavioral_outside_home,"behavioral_touch_face":data.behavioral_touch_face,"doctor_recc_h1n1":data.doctor_recc_h1n1,"doctor_recc_seasonal":data.doctor_recc_seasonal,"chronic_med_condition":data.chronic_med_condition,"child_under_6_months":data.child_under_6_months,"health_worker":data.health_worker,"health_insurance":data.health_insurance,"opinion_h1n1_vacc_effective":data.opinion_h1n1_vacc_effective,"opinion_h1n1_risk":data.opinion_h1n1_risk,"opinion_h1n1_sick_from_vacc":data.opinion_h1n1_sick_from_vacc,"opinion_seas_vacc_effective":data.opinion_seas_vacc_effective,"opinion_seas_risk":data.opinion_seas_risk,"opinion_seas_sick_from_vacc":data.opinion_seas_sick_from_vacc,"age_group":data.age_group,"education":data.education,"race":data.race,"sex":data.sex,"income_poverty":data.income_poverty,"marital_status":data.marital_status,"rent_or_own":data.rent_or_own,"employment_status":data.employment_status,"hhs_geo_region":data.hhs_geo_region,"census_msa":data.census_msa,"household_adults":data.household_adults,"household_children":data.household_children,"employment_industry":data.employment_industry,"employment_occupation":data.employment_occupation}
    dbuser = DataUploadModel(**usr)
    if (collection.insert_one(dbuser.dict())):
        return {"message": "Data Uploaded Succesfully"}
    else:
        return {"message": "Data not Uploaded"}