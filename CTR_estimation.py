# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 14:10:36 2016

@author: sassi
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from math import sqrt
from sklearn.metrics import  roc_auc_score, mean_squared_error
from scipy.sparse import hstack
from ua_parser import user_agent_parser 


def browser_extraction(x):
    user_agent =user_agent_parser.ParseUserAgent(str(x))
    return user_agent['family']
def oper_system_extraction(x):
    user_agent =user_agent_parser.ParseOS(str(x))
    return user_agent['family']

def Tag_processing(x):
    tag=str(x).split(',')
    l=len(tag)
    output=pd.Series()
    for i in range(0,l):
        output=output.append(pd.Series({'tag_'+tag[i]:1}))
    return output


    
def act_data_treatment(dataset):
    dataset=dataset[['weekday','hour','useragent','IP','region','city','domain','slotid','slotwidth','slotheight',
                         'slotvisibility','slotformat','slotprice','creative']]
    intervals=np.array([0,1,11,51,101,1000000])
    dataset['slotprice']=pd.cut(dataset['slotprice'], intervals,right=True,labels=False)
    dataset['Browser']=dataset['useragent'].apply(browser_extraction)
    dataset['Oper_sys']=dataset['useragent'].apply(oper_system_extraction)
    dataset=dataset.drop('useragent',axis=1)
    dataset.fillna('unknown', inplace=True)
    for col in list(dataset.columns):
            enc=LabelEncoder()
            dataset[col]=enc.fit_transform(dataset[col])
    enc=OneHotEncoder()
    dataset=enc.fit_transform(dataset)      
    return dataset
    

def ctr_estimate(campaign,data_train,data_test):
    train_label=data_train['click']
    test_label=data_test['click']
    train_length=data_train.shape[0]
    whole=pd.concat([data_train,data_test],axis=0)
    del data_train,data_test
    user_tag=whole['usertag'].apply(Tag_processing)
    user_tag=user_tag.fillna(0)
    user_tag_train=user_tag[:train_length].reset_index()
    user_tag_test=user_tag[train_length:].reset_index()
    del user_tag
    whole=act_data_treatment(whole)
    train_set=hstack((whole[:train_length,],user_tag_train))
    test_set=hstack((whole[train_length:,],user_tag_test))
    del whole,user_tag_train,user_tag_test
    lg = LogisticRegression(C=1,penalty='l2')
    model=lg.fit(train_set,train_label)
    predicted=model.predict_proba(test_set)
    auc_score = roc_auc_score(test_label, predicted[:, 1])
    lg_rmse = sqrt(mean_squared_error(test_label, predicted[:, 1]))
    print("Auc score for "+campaign+" campaign is %.4f and the RSME score is %.4f"%(auc_score,lg_rmse))
    return predicted[:, 1]
    
def ctr_estimate_basedcampaign(campaign,data_train,data_test):
        pCTR=pd.DataFrame()
        predicted=ctr_estimate(campaign,data_train,data_test)
        pCTR[campaign]=predicted
        pCTR['payprice']=data_test['payprice']
        pCTR['click']=data_test['click']
        pCTR['conversion']=data_test['nconversation']
        return pCTR
    
def ctr_Global_estimate(campaign,data_train,data_test):
    predicted=ctr_estimate(campaign,data_train,data_test)
    return predicted
    

