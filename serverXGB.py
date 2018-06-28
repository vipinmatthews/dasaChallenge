# import Flask class from the flask module
from flask import Flask, request

import numpy as np
import pandas as pd
import pickle
from xgboost.sklearn import XGBClassifier

# Create Flask object to run
app = Flask(__name__)

@app.route('/')
def home():
    return "Hi, Welcome to Flask!!"

@app.route('/predict')
def predict():

	# Get values from browser
	step = int(request.args['step'])
	transactionType = int(request.args['type'])
	amount = float(request.args['amount'])
	oldbalanceOrg = float(request.args['oldbalanceOrg'])
	newbalanceOrig = float(request.args['newbalanceOrig'])
	oldbalanceDest = float(request.args['oldbalanceDest'])
	newbalanceDest = float(request.args['newbalanceDest'])
	#errorBalanceOrig = float(request.args['errorBalanceOrig'])
	#errorBalanceDest = float(request.args['errorBalanceDest'])
	
	errorBalanceOrig = float(newbalanceOrig) + float(amount) - float(oldbalanceOrg)
	errorBalanceDest = float(oldbalanceDest) + float(amount) - float(newbalanceDest)
	columnNames=['step', 'type', 'amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest', 'errorBalanceOrig', 'errorBalanceDest']

	testData = np.array([step, transactionType, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest, errorBalanceOrig, errorBalanceDest]).reshape(1,9)
	pdTest = pd.DataFrame(testData, columns=columnNames)
	class_prediced = int(xgbModel.predict(pdTest))
	output = "Predicted Class: " + str(class_prediced)
	
	return (output)
	
# Load the pre-trained and persisted XGB model
# Note: The model will be loaded only once at the start of the server
def load_model():
	global xgbModel
	xgbFile = open('models/XGBModel.pckl', 'rb')
	xgbModel = pickle.load(xgbFile)
	xgbFile.close()

if __name__ == "__main__":
	print("**Starting Server...")
	
	# Call function that loads Model
	load_model()
	
	# Run Server
	app.run()
