# -*- coding: utf-8 -*-
"""
Created on Fri Oct 07 10:40:11 2016

@author: redouane sassioui
"""
# this script calculate the following data statistics: CTR,base_bid,CVR,and CPC
import pandas as pd 

def data_statistics_test(data_set,campaign):
    clicks=float(data_set['click'].sum())
    convs=float(data_set['nconversation'].sum())
    Imps=float(data_set.shape[0])
    min_bid=data_set['bidprice'].min()
    max_bid=data_set['bidprice'].max()
    mean_bid=data_set['bidprice'].mean()
    cost=data_set['payprice'].sum()
    base_CTR=(clicks/Imps)
    if clicks>0:
         base_CVR=convs/clicks
         CPC=cost/clicks
    else:
        base_CVR=0
        CPC=0
     
    base_bid=data_set['bidprice'].mean()
    return pd.DataFrame([[campaign,Imps,clicks,convs,base_CTR,base_bid,base_CVR,CPC,min_bid,max_bid,mean_bid,cost]],
                                                          columns=['Campaign','Imps','Clicks','Convs','CTR','base_bid','CVR','CPC','min_bid','max_bid','mean_bid','Cost'])
   
def data_statistics_train(data_set,campaign):
    clicks=float(data_set['click'].sum())
    #convs=float(data_set['nconversation'].sum())
    Imps=float(data_set.shape[0])
    min_bid=data_set['bidprice'].min()
    max_bid=data_set['bidprice'].max()
    mean_bid=data_set['bidprice'].mean()
    cost=data_set['payprice'].sum()
    base_CTR=(clicks/Imps)
    if clicks>0:
         #base_CVR=convs/clicks
         CPC=cost/clicks
    else:
        #base_CVR=0
        CPC=0
     
    base_bid=data_set['bidprice'].mean()
    return pd.DataFrame([[campaign,Imps,clicks,base_CTR,base_bid,CPC,min_bid,max_bid,mean_bid,cost]],
                                                          columns=['campaign','Imps','Clicks','base_CTR','base_bid','CPC','min_bid','max_bid','mean_bid','cost'])







