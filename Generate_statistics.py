# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 11:30:10 2016

@author: sassi
"""
#statistics_set columns=['campaigns','wining_price','strategy','click','conversion']

import pandas as pd 




def append_pdf(input,output):
    [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]



def generate_statistics_based_adviser(statistics_set,DSP_list,test_stats,report_name,report_path):
    test_stats=test_stats[['Campaign','Imps','Clicks','Convs','CTR','CVR','Cost']]
    output_data=pd.DataFrame()
    for dsp in DSP_list:
        campaign=dsp.campaigns[0]
        Num_bids=statistics_set.shape[0]
        strategy=dsp.bidding_functions[0]
        imprs=statistics_set[(statistics_set['dsp']==dsp.name) &(statistics_set['imps']==1) ]['imps'].count()
        #strategy=statistics_set[(statistics_set['campaigns']==campaign) & (statistics_set['strategy'] != "Na")].ix[1]['strategy']
        clicks=statistics_set[(statistics_set['dsp']==dsp.name) &(statistics_set['clicks']==1)]['clicks'].count()
        convs=statistics_set[(statistics_set['dsp']==dsp.name) & (statistics_set['convs']==1)]['convs'].count()
        wining_ratio=float(imprs)/float(Num_bids)
        if imprs>0:
            CTR=float(clicks)/float(imprs)
        else:
            CTR=0
        if clicks>0:
            CVR=float(convs)/float(clicks)
        else:
            CVR=0
        output_data=output_data.append(pd.DataFrame([[dsp.name,campaign,strategy,imprs,clicks,convs,wining_ratio,CTR,CVR]],
                      columns=['dsp','campaigns','bidding function','imps','clicks','Convs','win ratio','CTR','CVR']),ignore_index=True)
    output_data.to_html(report_path+'/'+report_name+'.html')
    


def generate_statistics_adviser_Less(statistics_set,DSP_list,report_name,report_path):
    output_dsp=pd.DataFrame()
    output_campaign=pd.DataFrame()
    output_strategy=pd.DataFrame()
    Num_bids=statistics_set.shape[0]
    for dsp in DSP_list:
        imprs=statistics_set[(statistics_set['wining_dsp']==dsp.name)]['wining_dsp'].count()
        wining_ratio=float(imprs)/float(Num_bids)
        output_dsp=output_dsp.append(pd.DataFrame([[dsp.name,imprs,wining_ratio]],
                      columns=['dsp','imps','wining ratio']),ignore_index=True)
    campaigns=[]
    for dsp in DSP_list:
        for campaign in dsp.campaigns:
            if campaign not in campaigns:
                campaigns.append(campaign)
                      
    for campaign in campaigns:
        imprs=statistics_set[(statistics_set['wining_compains']==campaign)]['wining_dsp'].count()
        wining_ratio=float(imprs)/float(Num_bids)
        output_campaign=output_campaign.append(pd.DataFrame([[campaign,imprs,wining_ratio]],
                      columns=['campaign','imps','wining ratio']),ignore_index=True)    
        
    strategies=[]
    for dsp in DSP_list:
        for strategy in dsp.bidding_functions:
            if strategy not in strategies:
                strategies.append(strategy)
    for strategy in strategies:
        imprs=statistics_set[(statistics_set['wining_strategy']==strategy)]['wining_dsp'].count()
        wining_ratio=float(imprs)/float(Num_bids)
        output_strategy=output_strategy.append(pd.DataFrame([[strategy,imprs,wining_ratio]],
                      columns=['Bidding function','imps','wining ratio']),ignore_index=True) 
    
    output_dsp.to_html(report_path+'/'+report_name+'_dsps.html',index=False)
    output_campaign.to_html(report_path+'/'+report_name+'_campaigns.html',index=False)
    output_strategy.to_html(report_path+'/'+report_name+'_strategy.html',index=False)
    
      
