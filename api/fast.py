from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sklearn.utils.fixes import _joblib_parallel_args
from google.cloud import storage
import joblib
import api.weather as w

BUCKET_NAME= 'wildfires_le_wagon'
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
def predict_fire(HORIZON):
    
    # Binary model
    client = storage.Client()
    bucket = client.get_bucket(BUCKET_NAME)
    blob = bucket.blob(STORAGE_LOCATION1)
    blob.download_to_filename('model_binary.joblib')
    
    rf_model = joblib.load('model_binary.joblib')
    
    
    # Size model
    client2 = storage.Client()
    bucket = client2.get_bucket(BUCKET_NAME)
    blob2 = bucket.blob(STORAGE_LOCATION2)
    blob2.download_to_filename('wildfire_size_model.joblib')
    
    size_model = joblib.load('wildfire_size_model.joblib')
    
    # Data for prediction
    # size, binary = w.size(1, 'Wagga Wagga')
    
    size, binary = w.get_all_states(HORIZON)
    
    
    
    # Results
    probability = rf_model.predict_proba(binary)
    size_pred = size_model.predict(size)

    
    return {"probability": probability, 'size': size_pred}

@app.get("/city")
def predict_city(HORIZON, CITY):
    
    # Binary model
    client = storage.Client()
    bucket = client.get_bucket(BUCKET_NAME)
    blob = bucket.blob(STORAGE_LOCATION1)
    blob.download_to_filename('model_binary.joblib')
    
    rf_model = joblib.load('model_binary.joblib')
    
    
    # Size model
    client2 = storage.Client()
    bucket = client2.get_bucket(BUCKET_NAME)
    blob2 = bucket.blob(STORAGE_LOCATION2)
    blob2.download_to_filename('wildfire_size_model.joblib')
    
    size_model = joblib.load('wildfire_size_model.joblib')
    
    # Data for prediction
    # size, binary = w.size(1, 'Wagga Wagga')
    
    size, binary = w.size(HORIZON, CITY)
    
    
    
    # Results
    probability = rf_model.predict_proba(binary)
    size_pred = size_model.predict(size)

    
    return {"probability": probability, 'size': size_pred}
