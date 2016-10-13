# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 14:46:09 2016

@author: sassi
"""
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from user_agents import parse
from math import sqrt
from sklearn.metrics import  roc_auc_score, mean_squared_error

def browser_extraction(x):
    user_agent = parse(str(x))
    return user_agent.browser.family
def oper_system_extraction(x):
    user_agent = parse(str(x))
    return user_agent.os.family

    
def act_data_treatment(setname):
    dataset = setname
    dataset=dataset[['weekday','hour','useragent','IP','region','city','domain','slotid','slotwidth','slotheight',
                         'slotvisibility','slotformat','slotprice','creative','usertag']]
    dataset['Browser']=dataset['useragent'].apply(browser_extraction)
    dataset['Oper_sys']=dataset['useragent'].apply(oper_system_extraction)
    dataset=dataset.drop('useragent',axis=1)
    dataset.fillna('unknown', inplace=True)
    print(dataset['Browser'])
    for col in list(dataset.columns):
            enc=LabelEncoder()
            dataset[col]=enc.fit_transform(dataset[col])
    enc=OneHotEncoder()
    dataset=enc.fit_transform(dataset)        
    return dataset
    
def label_ecoding(setname):
    
    dataset=setname
    for col in list(dataset.columns):
            #if col not in ['weekday', 'hour', 'region', 'city','slotwidth','slotheight','slotprice','creative']:
            enc=LabelEncoder()
            dataset[col]=enc.fit_transform(dataset[col])
        
    return dataset
def onehot_encoding(setname):
    
            enc=OneHotEncoder()
            setname=enc.fit_transform(setname)
            return setname
    
    
        
#compains=['1458','2259','2261','2821','2997','3358','3386','3427','3476']
compains=['2997']

for X in compains:
    data_train=pd.read_csv("..\\"+X+"\\train.log.txt", header=0, sep='\t', index_col=False,engine='python')
    data_test=pd.read_csv("..\\"+X+"\\test.log.txt", header=0, sep='\t', index_col=False,engine='python')
    train_label=data_train['click']
    test_label=data_test['click']
    train_length=data_train.shape[0]
    test_length=data_test.shape[0]
    whole=pd.concat([data_train,data_test],axis=0)
    del data_train,data_test
    enc_whole=act_data_treatment(whole)
    del whole
    train_set=enc_whole[:train_length,]
    test_set=enc_whole[train_length:,]
    del enc_whole
    lg = LogisticRegression(C=1,penalty='l2')
    model=lg.fit(train_set,train_label)
    del train_set
    predicted=model.predict_proba(test_set)
    auc_score = roc_auc_score(test_label, predicted[:, 1])
    lg_rmse = sqrt(mean_squared_error(test_label, predicted[:, 1]))
    print("Auc score for "+X+" compaign is %.4f and the RSME score is %.4f"%(auc_score,lg_rmse))
    
