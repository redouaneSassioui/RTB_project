# -*- coding: utf-8 -*-
"""
Created on Fri Oct 07 10:40:11 2016

@author: redouane sassioui
"""
# this script calculate the following data statistics: CTR,base_bid,CVR,and CPC

import pandas as pd
compains=['1458','2259','2261','2821','2997','3358','3386','3427','3476']
######## train data set##############
statistics_train=pd.DataFrame()
for X in compains:
    data_set=pd.read_csv("C:\\Project\\make-ipinyou-data\\"+X+"\\train.log.txt", header=0, sep='\t', index_col=False,engine='python')
    #print(train.dtypes)
    cliks=float(data_set['click'].sum())
    convs=float(data_set[data_set['logtype']==3].shape[0])
    Imps=float(data_set.shape[0])
    cost=data_set['payprice'].sum()
    base_CTR=(cliks/Imps)
    base_CVR=convs/cliks
    CPC=cost/cliks 
    base_bid=data_set['bidprice'].mean()
    statistics_train=statistics_train.append(pd.DataFrame([[int(X),base_CTR,base_bid,base_CVR,CPC]],columns=['compaign','base_CTR','base_bid','base_CVR','CPC']),ignore_index=True)
    #print(base_CTR_bid)
    del data_set
statistics_train.to_csv("C:\\Project\\make-ipinyou-data\\base_CTR_bid\\statistics_trainData.csv", index=True)


######### Test data set
statistics_test=pd.DataFrame()
for X in compains:
    data_set=pd.read_csv("C:\\Project\\make-ipinyou-data\\"+X+"\\test.log.txt", header=0, sep='\t', index_col=False,engine='python')
    cliks=float(data_set['click'].sum())
    convs=float(data_set[data_set['logtype']==3].shape[0])
    Imps=float(data_set.shape[0])
    cost=data_set['payprice'].sum()
    print(cost)
    base_CTR=(cliks/Imps)
    base_CVR=convs/cliks
    CPC=cost/cliks
    base_bid=data_set['bidprice'].mean()
    statistics_test=statistics_test.append(pd.DataFrame([[int(X),base_CTR,base_bid,base_CVR,CPC]],columns=['compaign','base_CTR','base_bid','base_CVR','CPC']),ignore_index=True)
    print(statistics_test)
    del data_set
statistics_test.to_csv("C:\\Project\\make-ipinyou-data\\base_CTR_bid\\statistics_testData.csv", index=True)





