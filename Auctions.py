# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 15:02:26 2016

@author: sassi
"""

from Bidding_functions import bid_compute
import pandas as pd 
import sys 

#DSPs=xml_parser(conf.xml)

def dspExtraction(x):
    if x=='wining_price':
        return 'Na'
    else:
        return str(x).split(',')[0]
def campaignExtraction(x):
    if x=='wining_price':
        return 'Na'
    else:
        return str(x).split(',')[1]
        
def strategyExtraction(x):
    if x=='wining_price':
        return 'Na'
    else:
        return str(x).split(',')[2]
def bisection(ind,budget,pCTR_set):
    index=range(0,len(ind))
    min1=index[0]
    max1=index[-1]
    lambda1=min1
    sum1=pCTR_set.ix[ind[0:min1+1]]['payprice'].sum()
    sum2=pCTR_set.ix[ind[0:max1+1]]['payprice'].sum()
    sum3=pCTR_set.ix[ind[0:lambda1+1]]['payprice'].sum()
    while (sum1<budget)&(sum2>budget)&(max1-min1>1):
        if sum3>=budget:
           max1=lambda1
        else:
           min1=lambda1
        lambda1=int((min1+max1)/2)
        sum1=pCTR_set.ix[ind[0:min1+1]]['payprice'].sum()
        sum2=pCTR_set.ix[ind[0:max1+1]]['payprice'].sum()
        sum3=pCTR_set.ix[ind[0:lambda1+1]]['payprice'].sum()
    if(sum1==budget):
         return min1+1
    elif (sum1>budget):
         return min1
    elif sum2<=budget:
         return max1+1
    else:
        return max1


def auction_based_adviser(pCTR_set,dsp,data_stat):
    campaign = dsp.campaigns[0]
    statistics_set=pd.DataFrame()
    ind=data_stat[data_stat['campaign']==int(campaign)]['campaign'].index
    if len(ind)== 0:
        print("Error: the campaign does not exist") 
        sys.exit()
    base_CTR=data_stat[data_stat['campaign']==int(campaign)]['base_CTR'].values
    base_bid=data_stat[data_stat['campaign']==int(campaign)]['base_bid'].values
    CPC=data_stat[data_stat['campaign']==int(campaign)]['CPC'].values
    min_bid=data_stat[data_stat['campaign']==int(campaign)]['min_bid'].values
    max_bid=data_stat[data_stat['campaign']==int(campaign)]['min_bid'].values
    mean_bid=data_stat[data_stat['campaign']==int(campaign)]['mean_bid'].values
    
    Data_stat=[base_CTR,base_bid,CPC,min_bid,max_bid,mean_bid]
    statistics_set['bid']=pCTR_set[campaign].apply(lambda x: bid_compute(campaign,Data_stat,dsp.bidding_functions[0],x,dsp.arg[0]))
    statistics_set['wining_price']=pCTR_set['payprice']
    statistics_set['clicks']=0
    statistics_set['convs']=0
    statistics_set['imps']=0
    statistics_set['strategy']=dsp.bidding_functions[0]
    statistics_set['campaigns']=campaign
    statistics_set['dsp']=dsp.name
    ind=statistics_set[statistics_set['bid']>statistics_set['wining_price']].index
    if len(ind>0):
       index=bisection(ind,dsp.budgets[0],pCTR_set)
       statistics_set.iloc[ind[0:index],statistics_set.columns.get_loc('imps')]=1
       statistics_set.iloc[ind[0:index],statistics_set.columns.get_loc('clicks')]=pCTR_set.ix[ind[0:index]]['click']
       statistics_set.iloc[ind[0:index],statistics_set.columns.get_loc('convs')]=pCTR_set.ix[ind[0:index]]['conversion']
    return statistics_set
    
    
def auction_adviser_less(pCTR_set,DSP_list,data_stat):
        bid_set=pd.DataFrame()
        for dsp in DSP_list:
            intern_set=pd.DataFrame()
            for campaign in dsp.campaigns: 
                ind=dsp.campaigns.index(campaign)
                base_CTR=data_stat[data_stat['campaign']==int(campaign)]['base_CTR'].values
                base_bid=data_stat[data_stat['campaign']==int(campaign)]['base_bid'].values
                CPC=data_stat[data_stat['campaign']==int(campaign)]['CPC'].values
                min_bid=data_stat[data_stat['campaign']==int(campaign)]['min_bid'].values
                max_bid=data_stat[data_stat['campaign']==int(campaign)]['min_bid'].values
                mean_bid=data_stat[data_stat['campaign']==int(campaign)]['mean_bid'].values
                Data_stat=[base_CTR,base_bid,CPC,min_bid,max_bid,mean_bid]
                intern_set[dsp.name+','+campaign+','+dsp.bidding_functions[ind]]=pCTR_set[campaign].apply(lambda x: bid_compute(campaign,Data_stat,dsp.bidding_functions[0],x,dsp.arg[0]))
            ind_n=[]
            ind_n_1=[]
            column=intern_set.columns.tolist()
            
            while True:
                intern_set['wining']=intern_set[column].idxmax(axis=1)
                for l in range(0,len(dsp.campaigns)):
                    indices=intern_set[(intern_set['wining']==dsp.name+','+dsp.campaigns[l]+','+dsp.bidding_functions[l])&
                                                 (intern_set[dsp.name+','+dsp.campaigns[l]+','+dsp.bidding_functions[l]]>0)].index
                    ind_n.append(indices)
                    if len(indices)>0:
                       temp=bisection(indices,dsp.budgets[l],pCTR_set)
                       intern_set.iloc[indices[temp:],intern_set.columns.get_loc(dsp.name+','+dsp.campaigns[l]+','+dsp.bidding_functions[l])]=0
                if ind_n==ind_n_1:
                    break
                ind_n_1=ind_n
            bid_set=pd.concat([bid_set,intern_set[column]],axis=1)
        bid_set['wining_price']=pCTR_set['payprice']
        bid_set['wining']=bid_set.idxmax(axis=1)
        bid_set['wining_dsp']=bid_set['wining'].apply(dspExtraction)
        bid_set['wining_compains']=bid_set['wining'].apply(campaignExtraction)
        bid_set['wining_strategy']=bid_set['wining'].apply(strategyExtraction)
        
        return bid_set[['wining_dsp','wining_price','wining_compains','wining_strategy']]
