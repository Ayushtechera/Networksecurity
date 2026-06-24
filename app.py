import sys
import os

# Certifi verify the SSL certificate of server from the CA(Certificate Authority) that certifi has.
import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()

mongo_db_url = os.getenv("MONGODB_URL_KEY")
print(mongo_db_url)

import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd 


from networksecurity.utils.main_utils.utils import load_object

client = pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)

from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME
from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]


app = FastAPI()
origins=["*"]

app.add_middleware(
    CORSMiddleware,
    # who can access this api 
    allow_origins=origins,
    # cookies/tokens allow
    allow_credentials=True,
    # Allow all methods of http GET,POST,PUT,DELETE
    allow_methods = ["*"],
    # allow all headers 
    allow_headers=["*"],
)


from fastapi.templating import Jinja2Templates
templates= Jinja2Templates(directory="./templates")

@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train_rount():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_training_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    


@app.post("/predict")
async def predict_route(request:Request,file:UploadFile=File(...)):

    try:
        df=pd.read_csv(file.file)
        preprocessor = load_object("final_models/preprocessing.pkl")
        final_model = load_object("final_models/model.pkl")
        network_model = NetworkModel(preprocessor,final_model)
        print(df.iloc[0])
        y_pred = network_model.predict(df)
        print(y_pred)
        df['predicted_column'] = y_pred
        print(df['predicted_column'])
        df.to_csv("prediction_output/output.csv")
        table_html = df.to_html(classes="table table-striped")
        return templates.TemplateResponse(
            request=request,
            name="table.html",
            context={"table": table_html}
        )
    except Exception as e:
        raise NetworkSecurityException(e,sys)

if __name__ == "__main__":
    app_run(app,host="0.0.0.0",port=8080)
    