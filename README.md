# Project idea
The goal of the wildfire_prediction project is to predict wheather a wildfire is going to occur, and if so, how big it will be. 
The location of interest is Australia. 

# Model for prediction of weather a wildfire is going to happen 
The optimal model is a random forest. We chose among several machine learning models, as well as deep learning models, because it exhibited the best performance. 
For the exploration of different models, please refer to the notebooks FH_base_model.ipynb and FH_NN.ipynb. 

In the rf_model.py file, the following functions can be found:
- get_data(): loads the dataset 
- preprocess(): preprocesses the data, namely sums up the forest measures and does the train test split. One hot encoding has already been done for the csv file and scaling is not necessary for a random forest.
- train_model(): trains the random forest
- predict_rf(): returns a binary prediction of weather there will be a fire or not
- predict_proba_rf(): returns a probability that a wildfire happens 
- score_rf(): returns a score of the model based on the test set 
- save_model(): saves the model as a joblib file 
- load_model(): loads the model 

