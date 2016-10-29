
import random
import numpy as np 
from fractions import Fraction
import sys

def constant_bidding(const_bid):
    return const_bid

def truth_telling_bidding(pCTR, CPC):
    return pCTR*CPC
 
def random_bidding(min_bids,max_bids):
    return	random.randrange(min_bids,max_bids)

def linear_bidding(base_bid,base_CTR,pCTR):
    return  (base_bid * pCTR) / base_CTR
def Optimal_bidding1(pCTR,_lambda,c):
    return np.sqrt((c/_lambda)*pCTR +c*c)-c 
def Optimal_bidding2(pCTR,_lambda,c):
    var=Fraction(1,3)
    return c*(((pCTR+np.sqrt((c**2)*_lambda**2+pCTR**2))/(c*_lambda))**var-
     ((c*_lambda)/(pCTR+np.sqrt(c**2*_lambda**2+pCTR**2)))**var)
    

def bid_compute(campaign,data_stat,function_name,*argv):
    
    if function_name=='constant_bidding':
        return constant_bidding(data_stat[5])
    
    elif function_name=='truth_telling_bidding':
        bid= truth_telling_bidding(argv[0],data_stat[2])
        return bid
    elif function_name=='random_bidding':
        if data_stat[4]>data_stat[3]:
            bid=random_bidding(data_stat[3],data_stat[4])
        else:
            bid=data_stat[4]
        return bid
    elif function_name=='linear_bidding':
        bid=linear_bidding(data_stat[1],data_stat[0],argv[0])
        return bid
    elif function_name=='Optimal_bidding1':
        bid=Optimal_bidding1(argv[0],argv[1][0],argv[1][1])
        return bid
    elif function_name=='Optimal_bidding2':
        bid=Optimal_bidding2(argv[0],argv[1][0],argv[1][1])
        return bid
    else:
        print("Error: the bidding function "+function_name+" does not exist!")
        sys.exit()
 
      
