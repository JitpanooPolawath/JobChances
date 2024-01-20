import os
from gtts import gTTS
from .model import Votingmodel
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler


def train_model(Age,tempAces,tempEd,Employment,
                Gender,MentalHealth, 
                YearsCode,YearsCodePro, Country, 
                Salary, ComputerSkills):

    data = {
        'Age': [Age],
        'Accessibility': [tempAces],
        'EdLevel': [tempEd],
        'Employment' : [Employment],
        'Gender': [Gender],
        'MentalHealth' : [MentalHealth],
        'MainBranch': [0],
        'YearsCode' : [YearsCode],
        'YearsCodePro' : [YearsCodePro],
        'Country': [Country],
        'PreviousSalary': [Salary],
        'ComputerSkills': [ComputerSkills]
    }

    X_data = pd.DataFrame(data)
    X_data['TotalYears'] = X_data['YearsCode'] + X_data['YearsCodePro']
    scale = StandardScaler()
    X_data['PreviousSalary'] = scale.fit_transform(X_data[['PreviousSalary']])


    if not os.path.isfile('.\pred\model.pkl'):
        print("Creating model")
        model = Votingmodel()
    else:
        print("Using previous model")
        with open('.\pred\model.pkl', 'rb') as f:
            model = pickle.load(f)

    y_predict = model.predict(X_data)
    prob1 = round(abs(model.predict_proba(X_data)[(0,0)] - 1), 2)
    prob2 = round(model.predict_proba(X_data)[(0,1)], 2)

    if y_predict == 0:
        print("You got a low chance of getting a job")
        print(f"confidence of answer: {prob1}")
        percent = prob1 * 100
        sentences = "Your probability for getting a Job is" +" "+ str(percent) +" "+"percent, so You got a low chance of getting a job" 
    elif y_predict == 1:
        print("You got a high chance of getting a job")
        print(f"confidence of answer: {prob2}")
        percent = prob2 * 100
        sentences = "Your probability for getting a Job is" +" "+ str(percent) +" "+"percent, so You got a high chance of getting a job" 
    else:
        print("N/A")
        sentences = "Invalid Data" 

    print(sentences)
    return sentences
