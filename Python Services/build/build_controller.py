import base64
import shutil
import dtale
from dtale.app import build_app
from dtale.views import startup
from flask import redirect
import dtale.app as dtale_app
from sklearn.metrics import roc_curve, roc_auc_score
from shutil import rmtree
import time
import os
import os.path
import json
import string, os, random
import datetime
import pandas as pd
from typing import List
from fastapi import UploadFile
import pymongo
from fastapi_mail import FastMail
import jwt
from bson import json_util
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.hash import bcrypt
from starlette import status
from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse
from starlette.responses import FileResponse
import logging
from pathlib import Path
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from category_encoders import OrdinalEncoder as oe
from catboost import CatBoostClassifier
from catboost import Pool, cv
import pandas_profiling as pf
import sweetviz as sv
from sklearn.metrics import roc_curve, roc_auc_score
import optuna
import pickle
import io

from build.build_model import ProjectsInDB, Projects, BuildModel
from configs.configurations import PATH
from configs.configurations import MONGODB_URL, MONGODB_DB_NAME


train_dataset =""
X_train, X_test, y_train, y_test = "","","",""


async def get_all_projects_from_db():
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("Projects")
    aProjects = collection.find({'status': 'Deployed'})
    if aProjects:
        resp = []
        async for leave in aProjects:
            data = ProjectsInDB(**leave)
            resp.append(data.dict()['projectName'])
        # print(resp)
        return resp

async def get_all_projects():
    projects_list = os.listdir(PATH + '/Data/')
    if '.DS_Store' in projects_list:
        projects_list.remove('.DS_Store')

    resp = await get_all_projects_from_db()
    projects_list = list(set(resp) & set(projects_list))
    projects_list = sorted(projects_list, key=str.capitalize)
    # print(projects_list)
    return json.loads(json_util.dumps(projects_list))

async def findDeployedProjects(pid:str):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("Projects")

    projects_list = os.listdir(PATH + '/Data/')
    if '.DS_Store' in projects_list:
        projects_list.remove('.DS_Store')

    aProjects = collection.find({"owner": pid,'status': 'Deployed'})
    if aProjects:
        resp = []
        async for leave in aProjects:
            data = ProjectsInDB(**leave)
            resp.append(data.dict()['projectName'])
        # print(resp)
        projects_list = list(set(resp) & set(projects_list))
        projects_list = sorted(projects_list, key=str.capitalize)
        # print(projects_list)
        return json.loads(json_util.dumps(projects_list))

async def findUnDeployedProjects(pid:str):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("Projects")

    projects_list = os.listdir(PATH + '/Data/')
    if '.DS_Store' in projects_list:
        projects_list.remove('.DS_Store')

    aProjects = collection.find({"owner": pid,'status': 'Undeployed'})
    if aProjects:
        resp = []
        async for leave in aProjects:
            data = ProjectsInDB(**leave)
            resp.append(data.dict()['projectName'])
        # print(resp)
        projects_list = list(set(resp) & set(projects_list))
        projects_list = sorted(projects_list, key=str.capitalize)
        # print(projects_list)
        return json.loads(json_util.dumps(projects_list))

async def addProjects(project: Projects):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("Projects")
    try:
        row = await collection.find_one({"projectName": project.projectName})
        if row:
            return {"message": "Project Already Exists"}
            # return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content="Project Already Exists")
        else:
            Project = {'projectName': project.projectName, 'owner': project.owner,'status':project.status}
            dbProject = ProjectsInDB(**Project)
            response = await collection.insert_one(dbProject.dict())
            return {"message": "Project Created Successfully"}
    except pymongo.errors.CollectionInvalid as e:
        logging.info(e)
    return {"message": "Internal Server Error"}

async def add_projects(project: Projects):
    try:
        os.mkdir(PATH + '/Data/')
    except OSError:
        try:
            Project = await addProjects(project)
            os.mkdir(PATH + '/Data/' + project.projectName)
            response1 = Project["message"]
        except OSError:
            print("Creation of the directory %s failed or already exists" % PATH + '/Data/')
            response = "Project Already Exists"
        else:
            print("Successfully created the directory %s" % PATH + '/Data/')
            response = response1
    else:
        print("In else")
        os.mkdir(PATH + '/Data/' + project.projectName)
        Project = await addProjects(project)
        response = Project["message"]
    return {"message": response}

async def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        upload_file.file.seek(0)
        print(destination)
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()

async def add_data(projectName: str, file: UploadFile, request):
    try:
        os.mkdir(PATH + '/Data/' + projectName + '/data/')
    except OSError:
        try:
            path = Path(PATH + '/Data/' + projectName + '/data/' + file.filename)
            await save_upload_file(file, path)
        except OSError:
            print("Creation of the directory %s failed or already exists" % Path(
                PATH + '/Data/' + projectName + '/data'))
        else:
            print(
                "Successfully created the directory %s" % Path(PATH + '/Data/' + projectName + '/data'))
    else:
        path = Path(PATH + '/Data/' + projectName + '/data/' + file.filename)
        await save_upload_file(file, path)
    fileurl = "http://" + request.client.host + ":" + str(request.url.port) + (
            '/get_csv' + '?' + "projectName" + "=" + projectName + '&' + "fileName" + "=" + file.filename)
    return {"fileurl": fileurl}

def get_data(project: str, fileName: str):
    dirPath = PATH + '/Data/' + project + '/data/' + fileName
    if Path(dirPath).exists():
        return FileResponse(dirPath)
    else:
        return FileResponse(PATH + '/Data/NOTFOUND.html')

def view_csv(projectName, fileName, request):
    csv_path = PATH + '/Data/' + projectName + '/data/' + fileName
    yes = []
    names = "http://" + request.client.host + ":" + str(request.url.port) + (
            "/getcsv" + '?' + "project_name" + "=" + projectName + '&' + "filename" + "=" + fileName)
    yes.append(names)
    print(yes)
    csvURL = []
    for key in yes:
        csvURL.append({"csv_url": key})
    dataset = pd.read_csv(csv_path)
    print(dataset.shape[1])
    datalist = list(dataset.columns)
    columns_list = []
    dataset = dataset.fillna('')

    for key in datalist:
        columns_list.append({"columns": key})
        # print(type(columns_list))
    data_val = dataset.values.tolist()
    # print("datavalues", data_val)
    data_lists = []

    for key in data_val:
        data_lists.append({"var": key})
        # print(type(data_lists))
    merged_list = columns_list + data_lists + csvURL
    # print(merged_list)
    return FileResponse(csv_path, media_type='application/octet-stream', filename=fileName)


def optunaSelection(trial):
    param = {
        'iterations':trial.suggest_categorical('iterations', [100,200,300,500,1000,1200,1500]),
        'learning_rate':trial.suggest_float("learning_rate", 0.001, 0.3),
        'random_strength':trial.suggest_int("random_strength", 1,10),
        'bagging_temperature':trial.suggest_int("bagging_temperature", 0,10),
        'max_bin':trial.suggest_categorical('max_bin', [4,5,6,8,10,20,30]),
        'grow_policy':trial.suggest_categorical('grow_policy', ['SymmetricTree', 'Depthwise', 'Lossguide']),
        'min_data_in_leaf':trial.suggest_int("min_data_in_leaf", 1,10),
        'od_type' : "Iter",
        'od_wait' : 100,
        "depth": trial.suggest_int("max_depth", 2,10),
        "l2_leaf_reg": trial.suggest_loguniform("l2_leaf_reg", 1e-8, 100),
         'one_hot_max_size':trial.suggest_categorical('one_hot_max_size', [5,10,12,100,500,1024]),
        'custom_metric' : ['AUC'],
        "loss_function": "Logloss",
        'auto_class_weights':trial.suggest_categorical('auto_class_weights', ['Balanced', 'SqrtBalanced']),
        }
    scores = cv(train_dataset, param,fold_count=5,early_stopping_rounds=10,plot=False, verbose=False)

    return scores['test-AUC-mean'].max()

def Analyze(tpath):
    global train_dataset, X_train, X_test, y_train, y_test
    train = pd.read_csv(tpath + '/data/training_set_features.csv', index_col='respondent_id')
    # test = pd.read_csv(tpath + '/data/test_set_features.csv', index_col='respondent_id')
    labels = pd.read_csv(tpath + '/data/training_set_labels.csv', index_col='respondent_id')
    full = train.join(labels)

    full_profile = pf.ProfileReport(full, title='Profiling Report', html={'style': {'full_width': True}})
    full_profile.to_file(output_file=tpath + "/data/Profiling_Report.html")

    my_report = sv.analyze(train.join(labels))
    my_report.show_html(tpath + "/data/sweetviz.html", False)

    num_cols = train.select_dtypes('number').columns
    cat_cols = ['race', 'sex', 'marital_status', 'rent_or_own', 'hhs_geo_region', 'census_msa', 'employment_industry','employment_occupation']
    ord_cols = ['age_group', 'education', 'income_poverty', 'employment_status']
    assert len(num_cols) + len(cat_cols) + len(ord_cols) == train.shape[1]

    for col in (cat_cols + ord_cols):
        train[col] = train[col].fillna(value='None')
    for col in num_cols:
        train[col] = train[col].fillna(value=-1)

    X_train, X_test, y_train, y_test = train_test_split(train, labels, test_size=0.3, random_state=68)
    X_test.to_csv(tpath + '/data/xTest.csv')
    y_test.to_csv(tpath + '/data/yTest.csv')
    train.to_csv(tpath + '/data/train.csv')

def trainDataSet(build_model:BuildModel):
    global train_dataset, X_train, X_test, y_train, y_test
    tpath = PATH + '/Data/' + build_model.fileName
    Analyze(tpath)

    categorical_features_indices = np.where(X_train.dtypes != float)[0]
    train_dataset = Pool(data=X_train,
                         label=y_train.h1n1_vaccine,
                         cat_features=categorical_features_indices)

    sampler = optuna.samplers.TPESampler(seed=68)
    study = optuna.create_study(direction="maximize", sampler=sampler)
    study.optimize(optunaSelection, n_trials=1)

    trial = study.best_trial
    final_model_h1n1 = CatBoostClassifier(verbose=False, cat_features=categorical_features_indices,**trial.params)
    final_model_h1n1.fit(X_train, y_train.h1n1_vaccine)

    train_dataset = Pool(data=X_train,
                         label=y_train.seasonal_vaccine,
                         cat_features=categorical_features_indices)

    sampler = optuna.samplers.TPESampler(seed=68)
    study = optuna.create_study(direction="maximize", sampler=sampler)
    study.optimize(optunaSelection, n_trials=1)

    trial = study.best_trial
    final_model_ses = CatBoostClassifier(verbose=False, cat_features=categorical_features_indices, **trial.params)
    final_model_ses.fit(X_train, y_train.seasonal_vaccine)

    picklepath = PATH + '/Data/' + build_model.fileName + '/models/'
    pkl_filename_h1n1 = 'model_h1n1.sav'
    pkl_filename_ses = 'model_ses.sav'

    try:
        os.mkdir(picklepath)
    except OSError:
        try:
            model_pkl = open(picklepath + pkl_filename_h1n1, 'wb')
            pickle.dump(final_model_h1n1, model_pkl, protocol=pickle.HIGHEST_PROTOCOL)
            model_pkl.close()

            model_pkl = open(picklepath + pkl_filename_ses, 'wb')
            pickle.dump(final_model_ses, model_pkl, protocol=pickle.HIGHEST_PROTOCOL)
            model_pkl.close()

        except OSError:
            print("Creation of the directory %s failed or already exists" % picklepath)
        else:
            print("Successfully Created %s" % picklepath)
    else:
        model_pkl = open(picklepath + pkl_filename_h1n1, 'wb')
        pickle.dump(final_model_h1n1, model_pkl, protocol=pickle.HIGHEST_PROTOCOL)
        model_pkl.close()

        model_pkl = open(picklepath + pkl_filename_ses, 'wb')
        pickle.dump(final_model_ses, model_pkl, protocol=pickle.HIGHEST_PROTOCOL)
        model_pkl.close()
    return {'message': "Sucessfully Trained"}

def plot_roc(y_true, y_score, label_name, ax):
    fpr, tpr, thresholds = roc_curve(y_true, y_score)
    ax.plot(fpr, tpr)
    ax.plot([0, 1], [0, 1], color='grey', linestyle='--')
    ax.set_ylabel('TPR')
    ax.set_xlabel('FPR')
    ax.set_title(f"{label_name}: AUC = {roc_auc_score(y_true, y_score):.4f}")

def getModelInfo(project:str):
    p = Path(PATH + '/Data/' + project + '/models/model_h1n1.sav')
    s = Path(PATH + '/Data/' + project + '/models/model_ses.sav')
    xP = Path(PATH + '/Data/' + project + '/data/xTest.csv')
    yP = Path(PATH + '/Data/' + project + '/data/yTest.csv')
    if p.exists() and xP.exists() and yP.exists()and s.exists():

        ploaded_model = pickle.load(open(p, 'rb'))
        sloaded_model = pickle.load(open(s, 'rb'))
        xTest = pd.read_csv(xP, index_col='respondent_id')
        yTest = pd.read_csv(yP, index_col='respondent_id')

        predictions_h1 = ploaded_model.predict_proba(xTest)
        predictions_h1 = predictions_h1[:, 1].reshape(-1, 1)
        presult = ploaded_model.score(xTest, yTest.h1n1_vaccine)
        fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        plot_roc(yTest['h1n1_vaccine'],predictions_h1,'h1n1_vaccine', ax=ax)
        fig.savefig(Path(PATH + '/Data/' + project + '/models/model_h1n1.png'))
        my_stringIObytes = io.BytesIO()
        fig.savefig(my_stringIObytes, format='jpg')
        my_stringIObytes.seek(0)
        my_base64_jpgData = base64.b64encode(my_stringIObytes.read())


        predictions_ses = sloaded_model.predict_proba(xTest)
        predictions_ses = predictions_ses[:, 1].reshape(-1, 1)
        sresult = sloaded_model.score(xTest, yTest.seasonal_vaccine)
        figA, axA = plt.subplots(1, 1, figsize=(10, 8))
        plot_roc( yTest['seasonal_vaccine'], predictions_ses, 'sesonal_vaccine', ax=axA)
        figA.savefig(Path(PATH + '/Data/' + project + '/models/model_seasonal.png'))
        Xmy_stringIObytes = io.BytesIO()
        figA.savefig(Xmy_stringIObytes, format='jpg')
        Xmy_stringIObytes.seek(0)
        my_base64_jpgDataA = base64.b64encode(Xmy_stringIObytes.read())


        return {'message':"Successful",'Accuracy_h1n1':presult, 'Accuracy_ses':sresult, 'img1':my_base64_jpgData,'img2':my_base64_jpgDataA,'modelName':project}
    else:
        return {'message': "Fail"}

async def deployModel(project:str,username:str):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("Projects")
    print("In deployed")
    row = await collection.find_one({"projectName": project,"owner":username})
    if row:
        await collection.update_one({"projectName": project,"owner":username},
                                    {'$set': {'status': 'Deployed'}})
        return {'message':'Deployed Succesfully'}
    return {'message':"You are Not Authorized"}

async def deleteModel(project:str,username:str):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.get_database(MONGODB_DB_NAME)
    collection = db.get_collection("Projects")
    row = await collection.find_one({"projectName": project,"owner":username})
    if row:
        data = ProjectsInDB(**row)
        collection.delete_one(data.dict())
        p = Path(PATH + '/Data/' + project)
        if p.exists():
            rmtree(p)
            return {'message': 'Deleted Succesfully'}
    return {'message': "You are Not Authorized"}