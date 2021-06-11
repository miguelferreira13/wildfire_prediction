import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, RobustScaler
from sklearn.impute import KNNImputer
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
import joblib

df = pd.read_csv('data/merged_file.csv', index_col=0)

df.drop(columns=['max() Precipitation', 
                 'max() RelativeHumidity',
                 'max() SoilWaterContent',
                 'max() SolarRadiation',
                 'max() WindSpeed',
                 'mean() SoilWaterContent',
                 'min() Precipitation', 
                 'min() RelativeHumidity',
                 'min() SoilWaterContent',
                 'min() SolarRadiation',
                 'min() WindSpeed',
                 'variance() Precipitation', 
                 'variance() RelativeHumidity',
                 'variance() SoilWaterContent',
                 'variance() SolarRadiation',
                 'variance() WindSpeed',
                 'variance() Temperature',
                 'Mean_estimated_fire_brightness',
                 'Mean_estimated_fire_radiative_power',
                 'Year',
                 'Month',
                 'Day'
                 ], inplace=True)


#Replacing na by 0
df.Estimated_fire_area.fillna(0, inplace=True)
# df.Mean_estimated_fire_brightness.fillna(0, inplace=True)
# df.Mean_estimated_fire_radiative_power.fillna(0, inplace=True)

#Solar Radiation to UV
df['mean() SolarRadiation'] = df['mean() SolarRadiation']*0.1
#Defining features and target
X = df.drop(columns=['Estimated_fire_area', 'Date_x'])
y = df.Estimated_fire_area


#Region Encoder
encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
encoded = encoder.fit_transform(X[['Region']])
encoder.categories_
for i, col in enumerate(encoder.categories_[0]):
    X[col] = pd.DataFrame(encoded)[i]
X.drop(columns='Region', inplace=True)

#Imputing null values
numerical_features = X.dtypes[(df.dtypes == 'float64') | (X.dtypes == 'int64')].index
imputer = KNNImputer()
values = imputer.fit_transform(X[X.dtypes[(df.dtypes == 'float64') | (X.dtypes == 'int64')].index])
X[X.dtypes[(df.dtypes == 'float64') | (X.dtypes == 'int64')].index] = values

#Scaler
scaler = RobustScaler()
scaled = scaler.fit_transform(X[X.dtypes[(df.dtypes == 'float64') | (X.dtypes == 'int64')].index])
X[X.dtypes[(df.dtypes == 'float64') | (X.dtypes == 'int64')].index] = scaled

#Train Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.3)



#Random Forest Model
rdf = RandomForestRegressor(criterion= 'mae', max_features= 'log2', n_estimators= 100)
rdf.fit(X_train, y_train)

print(rdf.score(X_test, y_test))
y_pred = rdf.predict(X_test)
print(np.sqrt((y_test-y_pred)**2).mean())
print(cross_val_score(rdf, X_test, y_test).mean())

X_test.to_csv('test_X', index=False)
y_test.to_csv('test_y', index=False)
joblib.dump(rdf, 'rdf_model_fire_size.joblib')
