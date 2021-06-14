from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import wildfire_prediction.RF_model as rf
from google.cloud import storage
import joblib
import api.weather as w

BUCKET_NAME = 'wildfires_le_wagon'
BUCKET_TRAIN_DATA_PATH = 'merged_data/merged_file.csv'
MODEL_NAME = 'wildfire prediction'
STORAGE_LOCATION1 = 'models/wildfire_prediction/model_binary.joblib'
STORAGE_LOCATION2 = 'models/wildfire_prediction/wildfire_size_model.joblib'


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
    blob1 = bucket.blob(STORAGE_LOCATION1)
    blob1.download_to_filename('model_binary.joblib')
    blob2 = bucket.blob(STORAGE_LOCATION2)
    blob2.download_to_filename('wildfire_size_model.joblib')
    rf_model =joblib.load('model_binary.joblib')
    size_model = joblib.load('wildfire_size_model.joblib')
    
    size, binary = w.size(1, 'Sydney')
    
    probability = rf.predict_proba_rf(rf_model, binary)
    size_pred = size_model.predict(size)
    
    return dict({"probability": probability, "size_pred": size_pred})
