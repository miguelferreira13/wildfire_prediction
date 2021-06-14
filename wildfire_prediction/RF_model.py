import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from joblib import dump, load
from google.cloud import storage

BUCKET_NAME = 'wildfires_le_wagon'
BUCKET_TRAIN_DATA_PATH = 'merged_data/merged_file.csv'
MODEL_NAME = 'wildfire prediction'
STORAGE_LOCATION = 'models/wildfire_prediction/model_binary.joblib'

def get_data():
    root_path = os.path.dirname(os.path.abspath(os.path.curdir))
    data_folder_path = os.path.join(root_path, 'wildfire_prediction/wildfire_prediction', 'data')
    data_file_path = os.path.join(data_folder_path, 'FH_data_final.csv')

    data = pd.read_csv(data_file_path)
    return data

def preprocess(data):
    data['forest'] = data['Closed forest, evergreen, broad leaf']\
        + data['Closed forest, deciduous broad leaf']\
            + data['Closed forest, unknown']\
                + data['Open forest, evergreen broad leaf']\
                    + data['Open forest, deciduous broad leaf']\
                        + data['Open forest, unknown definitions'] 
    data.drop(columns = ['Closed forest, evergreen, broad leaf',\
        'Closed forest, deciduous broad leaf',\
            'Closed forest, unknown',\
                'Open forest, evergreen broad leaf',\
                    'Open forest, deciduous broad leaf',\
                        'Open forest, unknown definitions'],\
                            inplace= True)
    y = data.target
    X = data.drop(columns = ['target', 'Day', 'Month', 'Year', 'Vegetation_index_variance'])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=3)
    return X_train, y_train, X_test, y_test

def train_model(X_train, y_train):
    rf_model = RandomForestClassifier(n_estimators = 700, 
                                      criterion = 'entropy', 
                                      max_depth = 100, 
                                      random_state = 1)
    rf_model = rf_model.fit(X_train, y_train)
    return rf_model

def predict_rf(rf_model, X_test):
    result_rf =rf_model.predict(X_test)
    return result_rf

def predict_proba_rf(rf_model, X_test):
    result_rf =rf_model.predict_proba(X_test)
    return result_rf[0][1]

def score_rf(rf_model, X_test, y_test):
    score = rf_model.score(X_test, y_test)
    return score

#def save_model(rf_model):
    model_binary = dump(rf_model, 'model_binary.joblib') 
    return model_binary

def upload_model_to_gcp():
    client = storage.Client()

    bucket = client.bucket(BUCKET_NAME)

    blob = bucket.blob(STORAGE_LOCATION)

    blob.upload_from_filename('model_binary.joblib')

def save_model(rf_model):
    dump(rf_model, 'model_binary.joblib')
    
    # Implement here
    upload_model_to_gcp()

def load_model():
    model = load('model_binary.joblib')
    return model

if __name__ == '__main__':
    data = get_data()

    # preprocess data
    X_train, y_train, X_test, y_test = preprocess(data)

    #train model
    rf_model = train_model(X_train, y_train)

    # save trained model 
    save_model(rf_model)