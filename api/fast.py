from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import wildfire_prediction.RF_model as rf
from google.cloud import storage
import joblib

BUCKET_NAME = 'wildfires_le_wagon'
BUCKET_TRAIN_DATA_PATH = 'merged_data/merged_file.csv'
MODEL_NAME = 'wildfire prediction'
STORAGE_LOCATION = 'models/wildfire_prediction/model_binary.joblib'

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
@app.get("/")
def predict_fire():
    client = storage.Client()
    bucket = client.get_bucket(BUCKET_NAME)
    blob = bucket.blob(STORAGE_LOCATION)
    blob.blob.download_to_filename('model_binary.joblib')
    rf_model =joblib.load('model_binary.joblib')
    
    probability = rf.predict_proba_rf(rf_model, 'DATAFRAME_FROM_API')
    return {"probability": probability}