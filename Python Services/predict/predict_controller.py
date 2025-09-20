import shutil
import pickle
from fastapi import UploadFile
from pathlib import Path
import os
import pandas as pd
import numpy as np
from starlette.responses import FileResponse
from fastapi.encoders import jsonable_encoder
import cProfile

from configs.configurations import PATH
from predict.predict_model import predictModel


def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    try:
        upload_file.file.seek(0)
        print(destination)
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()

def predictCSV(projectName: str, file: UploadFile, request):
    try:
        os.mkdir(PATH + '/Data/' + projectName + '/predict/')
    except OSError:
        try:
            path = Path(PATH + '/Data/' + projectName + '/predict/' + file.filename)
            save_upload_file(file, path)
        except OSError:
            print("Creation of the directory %s failed or already exists" % Path(PATH + '/Data/' + projectName + '/predict'))
        else:
            print( "Successfully created the directory %s" % Path(PATH + '/Data/' + projectName + '/predict'))
    else:
        path = Path(PATH + '/Data/' + projectName + '/predict/' + file.filename)
        save_upload_file(file, path)

    p = Path(PATH + '/Data/' + projectName + '/models/model_h1n1.sav')
    s = Path(PATH + '/Data/' + projectName + '/models/model_ses.sav')
    t = Path(PATH + '/Data/' + projectName + '/data/train.csv')
    l = Path(PATH + '/Data/' + projectName + '/data/training_set_labels.csv')
    if p.exists() and s.exists() and t.exists() and l.exists():
        path = Path(PATH + '/Data/' + projectName + '/predict/' + file.filename)
        test = pd.read_csv(path, index_col='respondent_id')
        train = pd.read_csv(t, index_col='respondent_id')
        labels = pd.read_csv(l, index_col='respondent_id')

        num_cols = train.select_dtypes('number').columns
        cat_cols = ['race', 'sex', 'marital_status', 'rent_or_own', 'hhs_geo_region', 'census_msa',
                    'employment_industry',
                    'employment_occupation']
        ord_cols = ['age_group', 'education', 'income_poverty', 'employment_status']
        for col in (cat_cols + ord_cols):
            test[col] = test[col].fillna(value='None')
        for col in num_cols:
            test[col] = test[col].fillna(value=-1)

        loaded_model = pickle.load(open(p, 'rb'))
        loaded_model.fit(train, labels.h1n1_vaccine)
        final_h1n1 = loaded_model.predict_proba(test)
        final_h1n1 = final_h1n1[:, 1].reshape(-1, 1)

        loaded_model = pickle.load(open(s, 'rb'))
        loaded_model.fit(train, labels.seasonal_vaccine)
        final_se = loaded_model.predict_proba(test)
        final_se = final_se[:, 1].reshape(-1, 1)

        store = Path(PATH + '/Data/' + projectName + '/predict/Predicted' + file.filename)
        result_df = pd.DataFrame(data=None, index=test.index)
        np.testing.assert_array_equal(test.index.values,result_df.index.values)
        result_df["h1n1_vaccine"] = final_h1n1
        result_df["seasonal_vaccine"] = final_se
        result_df.to_csv(store)
        return FileResponse(store)
    return {}


def predictIndividual(pred:predictModel):
    dict = pred.dict()
    projectName = dict['projectName']
    keys = list(dict.keys())
    df = pd.DataFrame(columns=keys)
    df = df.append(dict, ignore_index=True)
    df.drop('projectName', axis=1, inplace=True)
    p = Path(PATH + '/Data/' + projectName + '/models/model_h1n1.sav')
    s = Path(PATH + '/Data/' + projectName + '/models/model_ses.sav')
    t = Path(PATH + '/Data/' + projectName + '/data/train.csv')
    l = Path(PATH + '/Data/' + projectName + '/data/training_set_labels.csv')
    if p.exists() and s.exists() and t.exists() and l.exists():
        train = pd.read_csv(t, index_col='respondent_id')
        labels = pd.read_csv(l, index_col='respondent_id')

        loaded_model = pickle.load(open(p, 'rb'))
        # loaded_model.fit(train, labels.h1n1_vaccine)
        final_h1n1 = loaded_model.predict_proba(df)
        final_h1n1 = final_h1n1[:, 1].reshape(-1, 1)

        loaded_model = pickle.load(open(s, 'rb'))
        # loaded_model.fit(train, labels.seasonal_vaccine)
        final_se = loaded_model.predict_proba(df)
        final_se = final_se[:, 1].reshape(-1, 1)
        print(final_se, final_h1n1)
        return {'sesonal': final_se[0][0], 'h1n1': final_h1n1[0][0],}
    return {'sesonal': 0, 'h1n1': 0, }