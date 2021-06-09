from google.cloud import storage
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
import joblib

### GCP configuration - - - - - - - - - - - - - - - - - - -

# /!\ you should fill these according to your account

### GCP Project - - - - - - - - - - - - - - - - - - - - - -

# not required here

### GCP Storage - - - - - - - - - - - - - - - - - - - - - -

BUCKET_NAME = 'wildfires_le_wagon'

##### Data  - - - - - - - - - - - - - - - - - - - - - - - -

# Data file location
BUCKET_TRAIN_DATA_PATH = 'merged_data/merged_file.csv'

# model folder name (will contain the folders for all trained model versions)
MODEL_NAME = 'wildfire prediction'

# model version folder name (where the trained model.joblib file will be stored)
MODEL_VERSION = 'v1'


def get_data():
    """method to get the training data (or a portion of it) from google cloud bucket"""
    df = pd.read_csv(f"gs://{BUCKET_NAME}/{BUCKET_TRAIN_DATA_PATH}", nrows=1000)
    return df


def train_model(df):
    """method that pre-process the data"""
    df.Estimated_fire_area.fillna(0, inplace=True)
    df.Mean_estimated_fire_brightness.fillna(0, inplace=True)
    df.Mean_estimated_fire_radiative_power.fillna(0, inplace=True)
    
    X = df.drop(columns=['Estimated_fire_area', 'Date_x'])
    y = df.Estimated_fire_area
    
    imputer = KNNImputer()
    
    numeric_features = X.dtypes[(X.dtypes == 'float64') | (X.dtypes == 'int64')].index
    categorical_features = X.dtypes[(X.dtypes != 'float64') | (X.dtypes != 'int64')].index


    numeric_transformer = Pipeline(steps=[
    ('imputer', KNNImputer()),
    ('scaler', StandardScaler())])

    categorical_transformer = OneHotEncoder(handle_unknown='ignore')

    preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ],
        remainder='passthrough'
        )

    model = KNeighborsRegressor()

    pipe = Pipeline([
        ('pre', preprocessor),
        ('model', model),
    ])
    
    return pipe.fit(X, y)


# def train_model(X_train, y_train):
#     """method that trains the model"""
    
#     model.fit(X_train, y_train)
#     print("trained model")
#     return model


STORAGE_LOCATION = 'models/wildfire_prediction/model.joblib'


def upload_model_to_gcp():


    client = storage.Client()

    bucket = client.bucket(BUCKET_NAME)

    blob = bucket.blob(STORAGE_LOCATION)

    blob.upload_from_filename('model.joblib')


def save_model(reg):
    """method that saves the model into a .joblib file and uploads it on Google Storage /models folder
    HINTS : use joblib library and google-cloud-storage"""

    # saving the trained model to disk is mandatory to then beeing able to upload it to storage
    # Implement here
    joblib.dump(reg, 'model.joblib')
    print("saved model.joblib locally")

    # Implement here
    upload_model_to_gcp()
    print(f"uploaded model.joblib to gcp cloud storage under \n => {STORAGE_LOCATION}")


if __name__ == '__main__':
    # get training data from GCP bucket
    df = get_data()

    # preprocess data
    # X_train, y_train = preprocess(df)

    # train model (locally if this file was called through the run_locally command
    # or on GCP if it was called through the gcp_submit_training, in which case
    # this package is uploaded to GCP before being executed)
    model = train_model(df)

    # save trained model to GCP bucket (whether the training occured locally or on GCP)
    save_model(model)