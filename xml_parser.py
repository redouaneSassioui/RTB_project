import xml.etree.ElementTree as ET
import lxml.etree
import sys
import numbers

class DSP_class:
    DSP_name=None
    Number_ofcampaigns=None
    campaigns=[]
    bidding_functions=[]
    budgets=[]
    costs=[]
    arg=[] 


def check_max_budget(budget,compaing_id,mode_name):
    if mode_name== "mode1":
        campaigns=["1458","2259","2261","2821","2997","3358","3386","3427","3476"]
        max_budget=[45216454,43497557,28795996,68257100,3059109,34159766,45715525,46356518,43627585]
        index_campaign=campaigns.index(compaing_id)
        max_budget_compaig=max_budget[index_campaign]
        if budget > max_budget_compaig:
                print("In %s, the budget %d has to be less than the max budget:%d of the campaign %s. " %(mode_name,budget,max_budget_compaig,compaing_id))
                sys.exit()
    if mode_name== "mode2":
        campaigns=["1458","2259","2261","2821","2997","3358","3386","3427","3476"]
        max_budget=[45216454,43497557,28795996,68257100,3059109,34159766,45715525,46356518,43627585]
        sum_budget=sum(max_budget)
        if budget > sum_budget:
                print("In %s, the budget %d has to be less than the sum of all budgets:%d of the campaign %s. " %(mode_name,budget,sum_budget,compaing_id))
                sys.exit()
    


def Check_num_DSP(Number_of_DSPs,Number_of_DSPs_ct):
    if Number_of_DSPs_ct !=Number_of_DSPs:
      print("The number of DSPs does not match with the number entered by the user %d != %d!"%(Number_of_DSPs_ct,Number_of_DSPs))
      sys.exit()


def Check_bidding_function(name_funct):
    functions_names=["truth_telling_bidding","random_bidding","Optimal_bidding2","Optimal_bidding1","constant_bidding","linear_bidding"]
    if name_funct not in functions_names:
      print("The function entred by the user is unknown: %s!"%(name_funct))
      sys.exit()

def Check_compaing(compaing_id):
    campaigns=["1458","2259","2261","2821","2997","3358","3386","3427","3476"]
    if compaing_id not in campaigns:
      print("The campaign entred by the user is not in our database:%s!"%(compaing_id))
      sys.exit()

def Check_bidding_function_parameters(name_funct,list_arg):
    if name_funct=="Optimal_bidding1" or name_funct=="Optimal_bidding2":
                if len(list_arg)!=2:
                    print("The function %s function needs two parameters!"%(name_funct))
                    sys.exit()
    if name_funct=="truth_telling_bidding" or name_funct=="random_bidding" or name_funct=="constant_bidding" or name_funct=="linear_bidding" :
            if len(list_arg)>0:
                        print("Warning: The function %s does not need any parameter!"%(name_funct))

def Check_compaing_has_one_bid_function(number_function):
    if number_function!=1:
      print("Each campaign must have just  one bidding function!")
      sys.exit()


def Check_compaing_has_one_bid_function(number_function):
    if number_function!=1:
      print("Each campaign must have just  one bidding function!")
      sys.exit()

def Check_dsp_has_one_campaign_mode1(number_campaign):
    if number_campaign > 1:
      print("In mod1, each DSP must have just  one compain!")
      sys.exit()
def Check_dsp_has_at_least_one_campaign(number_campaign):
        if number_campaign==0:
            print("Warning:Each DSP must have at least one compaing!")
            return False;
def check_parameter_is_number(parmetre_value):
    parmetre_value=parmetre_value.strip()
    if parmetre_value.replace('.','',1).isdigit()==False:
            print("The parameters have to be a number: %s"%(parmetre_value))
            sys.exit()

def check_budget(budget):
    budget=budget.strip()
    if budget.replace('.','',1).isdigit()==False:
            print("The budget has to be a number: %s"%(budget))
            sys.exit()

def xml_parser(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    list_DSP=[]
    mode = root.find('mode')
    mode_name=mode.get('name')
    Number_of_DSPs=int(mode.find('DSPs_number').text)
    Number_of_DSPs_ct=0
    for DSP in mode.findall('DSP'):
        Number_of_DSPs_ct= Number_of_DSPs_ct+1
        DSP_instance=DSP_class()    
        name_DSP = DSP.get('name')
        i=0
        list_campaign=[]
        list_bidding_fct=[]
        list_budget=[]
        list_cost=[]
        list_bidding_fct_parameters=[]
        for campaign in DSP.findall('Compaing'):
            i=i+1
            compaing_id= campaign.get('id')
            budget=campaign.find('budget').text
            check_budget(budget)
            budget=float(campaign.find('budget').text)
            check_max_budget(budget,compaing_id,mode_name)
            list_campaign.append(compaing_id)
            list_budget.append(budget)
            list_cost.append(0)
            Check_compaing(compaing_id)
            number_function=0
            for fonction in campaign.findall('bidding_function'):
                name_func = fonction.get('name')
                Check_bidding_function(name_func)
                list_bidding_fct.append(name_func)
                number_function=number_function+1
                int_arg=[1,2]
                j=0
                for parametre in fonction.findall('parameter'):
                    j=j+1
                    parmetre_value=parametre.text
                    check_parameter_is_number(parmetre_value)                      
                    name_parameter = parametre.get('name')
                    if name_parameter=="lamda":
                            int_arg[0]=float(parametre.text)
                    if name_parameter=="c":
                            int_arg[1]=float(parametre.text)
                if j==0:       
                    list_bidding_fct_parameters.append([])
                    int_arg=[]
                else:
                    list_bidding_fct_parameters.append(int_arg)
                Check_bidding_function_parameters(name_func,int_arg)
            Check_compaing_has_one_bid_function(number_function)
        if mode_name== "mode1":
            Check_dsp_has_one_campaign_mode1(i)
        if Check_dsp_has_at_least_one_campaign(i)==False:
            continue
        DSP_instance.arg=list_bidding_fct_parameters
        DSP_instance.bidding_functions=list_bidding_fct
        DSP_instance.Number_ofcampaigns=i
        DSP_instance.campaigns=list_campaign
        DSP_instance.budgets=list_budget
        DSP_instance.costs=list_cost
        DSP_instance.name=name_DSP
        list_DSP.append(DSP_instance)

    Check_num_DSP(Number_of_DSPs,Number_of_DSPs_ct)
    return list_DSP,mode_name



    
        





