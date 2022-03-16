from flask import redirect

from dtale.app import build_app
from dtale.views import startup
import pandas as pd
from pathlib import Path

from flask_cors import CORS

from build import build_model
from configs.configurations import PATH

if __name__ == '__main__':
    app = build_app(reaper_on=False)
    cors = CORS(app)

    @app.route("/editing/<project>",methods = ['POST', 'GET'])
    def create_df(project:str):
        p = Path(PATH + '/Data/' + project + '/data/training_set_features.csv')
        s = Path(PATH + '/Data/' + project + '/data/test_set_features.csv')
        xP = Path(PATH + '/Data/' + project + '/data/training_set_labels.csv')
        if p.exists() and xP.exists() and s.exists():
            train = pd.read_csv(p, index_col='respondent_id')
            test = pd.read_csv(s, index_col='respondent_id')
            labels = pd.read_csv(xP, index_col='respondent_id')
            full = train.join(labels)
            instance = startup(data=full, ignore_duplicate=True)
            print(instance._data_id)
            return {'message': instance._data_id}
        return {'message': '0'}
            # return redirect(f"/dtale/main/{instance._data_id}", code=302)

    @app.route("/")
    def hello_world():
        return 'Hi there, load data using <a href="/editing/string">create-df</a>'

    app.run(host="127.0.0.1", port=8080)