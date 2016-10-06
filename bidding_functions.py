
import random
import numpy as np 
from fractions import Fraction


def truth_telling_bidding(pCTR, CPC):
    return pCTR*CPC
 
def random_bidding(min_bids,max_bids):
    return	random.randrange(min_bids,max_bids)

def linear_bidding(base_bid,base_CTR,pCTR):
    return  base_bid * pCTR / base_CTR
def Optimal_bidding1(pCTR,_lambda,c):
    return np.sqrt((c/_lambda)*pCTR +c*c)-c 
def Optimal_bidding2(pCTR,_lambda,c):
    var=Fraction(1,3)
    return c*(((pCTR+np.sqrt((c**2)*_lambda**2+pCTR**2))/(c*_lambda))**var-
     ((c*_lambda)/(pCTR+np.sqrt(c**2*_lambda**2+pCTR**2)))**var)
    


 
      
