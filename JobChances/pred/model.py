import numpy
import pandas as pd


#save model 
import pickle

#sklearn import 
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
from sklearn.ensemble import GradientBoostingClassifier, VotingClassifier
from sklearn.metrics import roc_curve, auc


def encodeData(data):
    encoding = ['Age','Accessibility', 'EdLevel', 'Gender', 'MentalHealth', 'MainBranch', 'Country' ]
    temp = data.copy()
    lecode = LabelEncoder()
    for encode in encoding:
        temp[encode] = lecode.fit_transform(data[encode])

    scale = StandardScaler()
    temp['PreviousSalary'] = scale.fit_transform(temp[['PreviousSalary']])
    return temp

initData = pd.read_csv(".\pred\stackoverflow_full.csv")
initData = initData.drop(['Unnamed: 0','HaveWorkedWith'] , axis=1)
initData = initData[initData['Country'].isin(["Canada", "United States of America", "United Kingdom of Great Britain and Northern Ireland"])].copy()

encData = encodeData(initData)
encData['TotalYears'] = encData['YearsCode'] + encData['YearsCodePro']
ytrain = encData['Employed'].copy()
Xtrain = encData.drop('Employed', axis=1)
X_train, X_test, y_train, y_test = train_test_split(Xtrain, ytrain, test_size=0.1)

def Votingmodel():
    clf1 = LGBMClassifier(**{
    'learning_rate' : 0.01,
    'n_estimators' : 600,
    'num_leaves' : 30,
    'max_depth' : 7,   
    })
    clf2 = XGBClassifier(**{
        'n_estimators': 200,
        'max_depth': 5,
        'learning_rate': 0.01})
    clf3 = GradientBoostingClassifier(
        learning_rate=0.01,
        max_depth=10,    
    )
    voting = VotingClassifier(
            estimators=[('LGBM', clf1), ('XG', clf2), ('GB', clf3)],
            voting='soft',
            weights=[1,1,1]
    )
    voting.fit(X_train, y_train)

    with open('.\pred\model.pkl', 'wb') as f:
        pickle.dump(voting, f)

    return voting


def predict_and_test(model):
    y_predict = model.predict(X_test)
    print(f"score: {model.score(X_test, y_test)}")
    print(f"probability: {model.predict_proba(X_test[:1])}")
    print(f"predicted: {y_predict[:1]} -- \nactual: {y_test[:1]}")
    y_scores_dt = model.predict_proba(X_test)[:, 1]
    fpr_dt, tpr_dt, thresholds_dt = roc_curve(y_test, y_scores_dt)
    auc_dt = auc(fpr_dt, tpr_dt)
    print(auc_dt)


def train():
    # Predict using the best Decision Tree model
    model = Votingmodel()
    predict_and_test(model)
    


    

    
    


