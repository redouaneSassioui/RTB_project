# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 12:17:11 2016
@author: sassi

This is the main file. lines fron 29 to 50 need to be run once, those lines are for computing pCTR for each campaignand computing data statistics. 
For the first time uncomment those lines and comment them when the first run is finished. 
"""
from Data_statistics import data_statistics_test
from Data_statistics import data_statistics_train
from CTR_estimation import ctr_estimate_basedcampaign
from CTR_estimation import ctr_Global_estimate
from Auctions import auction_based_adviser
from Auctions import auction_adviser_less
from Generate_statistics import generate_statistics_based_adviser
from Generate_statistics import generate_statistics_adviser_Less
import pandas as pd
from xml_parser import xml_parser


DSP_list,mode=xml_parser('../Conf_file/Conf_file_mode2.xml') # read the configuration file 



#############################################################
############################################################
###########################################################

#campaings=['2997','2821','2261','2259','3358','3386','3427','3476','1458']
#statistics_train=pd.DataFrame()
#statistics_test=pd.DataFrame()
#data_test_all=pd.read_csv("../all/test.log.txt", header=0, sep='\t', index_col=False,engine='python')# load all test set merged in one file 
#global_pCTR=pd.DataFrame()
#global_pCTR['payprice']=data_test_all['payprice']
#for campaign in campaings:
#    data_train=pd.read_csv("../"+campaign+"/train.log.txt", header=0, sep='\t', index_col=False,engine='python')# load train data 
#    data_test=pd.read_csv("../"+campaign+"/test.log.txt", header=0, sep='\t', index_col=False,engine='python')# load test data 
#    pCTR=ctr_estimate_basedcampaign(campaign,data_train,data_test) # estimate the CTR for the campaign
#    pCTR.to_csv("../pCTR_data/"+campaign+"_pCTR_based_campaigns.csv") # write the prdictions to a specific file
#    global_pCTR[campaign]=ctr_Global_estimate(campaign,data_train,data_test_all)# estimate the CTR of the all test set for all compaigns
#    statistics=data_statistics_train(data_train,campaign)  # compute the historical train statitics for each campaign
#    statistics_train=statistics_train.append(statistics,ignore_index=True) 
#    statistics=data_statistics_test(data_test,campaign) # # compute the historical train statitics for each campaign
#    statistics_test=statistics_test.append(statistics,ignore_index=True)
#    del data_test,data_train,statistics,pCTR
#   
#statistics_train.to_csv("../data_statistics/statistics_trainData.csv", index=True)# write train statistics in a file
#statistics_test.to_csv("../data_statistics/statistics_testData.csv", index=True)# write test statistics in a file
#global_pCTR.to_csv("../pCTR_data/Global_pCTR.csv")# write global CTR estimation in a file
#del statistics_train,statistics_test,global_pCTR

train_stats=pd.read_csv("../data_statistics/statistics_trainData.csv")
test_stats=pd.read_csv("../data_statistics/statistics_testData.csv")
#################################################
################################################
###############################################
# here we compute the simulation statistics 

if mode=="mode1":
    statistics_set=pd.DataFrame()
    for dsp in DSP_list:
             print("compute statistics for campaign "+dsp.campaigns[0])
             pCTR_set=pd.read_csv("../pCTR_data/"+dsp.campaigns[0]+"_pCTR_based_campaigns.csv")
             statistics_set=statistics_set.append(auction_based_adviser(pCTR_set,dsp,train_stats),ignore_index=True)
             print("Statistics computed for campaign "+dsp.campaigns[0])
             del pCTR_set
    print("Generate output statistics")
    generate_statistics_based_adviser(statistics_set,DSP_list,test_stats,"report_based_campaign","../Report/")
    print("Output generated")
    
elif mode=="mode2":
    pCTR_set=pd.read_csv("../pCTR_data/Global_pCTR.csv")
    print("compute statistics")
    statistics_set=auction_adviser_less(pCTR_set,DSP_list,train_stats)
    print("Statistics computed")
    print("Generate output statistics")
    generate_statistics_adviser_Less(statistics_set,DSP_list,"report_campaign_less","../Report/")
    print("Output generated")
else:
    print("the mode "+mode+" does not exists")