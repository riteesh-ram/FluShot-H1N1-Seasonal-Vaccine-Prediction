import pymongo
import uvicorn
from bson import json_util
from fastapi import FastAPI, UploadFile, File, Form, Request
from starlette.middleware.cors import CORSMiddleware
from collections import defaultdict
import logging

from build.build_controller import add_projects, get_all_projects, findDeployedProjects, findUnDeployedProjects, \
    add_data, get_data, view_csv, trainDataSet, getModelInfo, deployModel, deleteModel
from build.build_model import Projects, BuildModel, changeModel
from predict.predict_controller import predictCSV, predictIndividual
from predict.predict_model import predictModel
from user.user_controller import loginFun, signUpFun, updatePassword, dataUpload
from user.user_model import UserInDB, login, UpdatePasswd, DataUploadModel

ALLOWED_EXTENSIONS = set(['csv'])

app = FastAPI(title= 'Flushot',version='1.0',  description="Provides Regression API")
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#
@app.post("/login",tags=['User'])
async def log(usr:login):
    return await loginFun(usr)

@app.put("/updatePassword", tags=["User"], summary="Update Password", description="Update Password")
async def update(usr:UpdatePasswd):
    return await updatePassword(usr)

@app.post("/signUp",tags=['User'])
async def su(usr:UserInDB):
    return await signUpFun(usr)

@app.post("/dataUpload", tags=["User"], summary="Uplod Data", description="Upload the data for sampelling")
async def def_dataUpload(pred:DataUploadModel):
    return await dataUpload (pred)

@app.post("/addproject", tags=["Projects"], summary="Add Project", description="Add / Insert Projects")
async def def_post_add_projects(project: Projects):
    return await add_projects(project)

@app.get("/allProjects", tags=["Projects"], summary="Get All Projects", description="Retrieve All Projects")
async def find_all_projects():
    return await get_all_projects()

@app.get("/deployedprojects/", tags=["Projects"], summary="Get Deployed Projects", description="Get Deployed Project details By username")
async def def_get_deployed_projects(pid: str):
    return await findDeployedProjects(pid)

@app.get("/unDeployedprojects/", tags=["Projects"], summary="Get UnDeployed Projects", description="Get UnDeployed Project details By Username")
async def def_get_undeployed_projects(pid: str):
    return await findUnDeployedProjects(pid)

@app.post("/addData", tags=["Data set"], summary="Add datas", description="Add / Insert data")
async def def_post_add_data(request: Request, file: UploadFile = File(...), project_name: str = Form(...)):
    return await add_data(project_name, file, request)

@app.get("/getcsv", tags=["Data set"], summary="Get datas", description="Get data")
def def_get_data(project_name: str, filename: str):
    return get_data(project_name, filename)

@app.get("/viewcsv", tags=["Data set"], summary="viewcsv", description="view csv")
def def_view_csv(project_name: str, filename: str, request: Request):
    return view_csv(project_name, filename, request)

@app.post("/trainmodel", tags=["Model"], summary="model pkl", description="model pkl")
def train_dataSet(build_model: BuildModel):
    return trainDataSet(build_model)

@app.get("/getModelInfo", tags=["Model"], summary="Get Model Info", description="Get Model Information")
def def_get_data(project_name: str):
    return getModelInfo(project_name)

@app.put("/deployModel", tags=["Model"], summary="Deploy Model", description="Get Model Information")
async def deploy(usr:changeModel):
    return await deployModel(usr.projectName,usr.userName)

@app.delete("/deleteModel", tags=["Model"], summary="Delete Model", description="Get Model Information")
async def delete(project_name: str, username:str):
    return await deleteModel(project_name,username)

@app.post("/predictCSV", tags=["Predictions"], summary="Predict Given CSV", description="Predict Given CSV")
def def_predictCSV(request: Request, file: UploadFile = File(...), project_name: str = Form(...)):
    return predictCSV(project_name, file, request)

@app.post("/predictINd", tags=["Predictions"], summary="Predict Given Individual", description="Predict Given Individual")
def def_predictInd(pred:predictModel):
    return predictIndividual (pred)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)