# RTB_project
In this project is, we have implemented a RTB sumilator using IpinYou public data set. The simulator has the following components:


1- Configuration file: it is an XML file in wich we define how many DSPs we want to simulate, for each dsp which campaigns it manages and for each campaign you have to define its budget and bidding function. Finaly we define the parameters of the bidding function. We define also the mode of simulation we want to perform:

  -Mode1: in this mode we run a campaign based simulation 
  -Mode2: in this mode we run a campaign less simulation
  
2- Simulator.py: this is the main file that we run after we define our parameters in configuration file. In which we do the following: 
    
   2.1 read the parameters of configuration file (Line 21)
    
   2.2 Estimate the pCTR of all test files for each campaign and save the result in separate file and compute data statstics for each campaign (line 29-50). Note that this step should be run one time and just use the saved file in future simulation in order to optimise simulation time. 
   
   2.3 depending on the simulation mode, we run the auction and generate the statistics. (Line 52-80)
    
3-XML-parser: this is the program that reads the xml file and output the simulation mode and the DSP list. We represent a DSP as a class with different attributes so that each dsp is an object of this class. The output is a list of DSP objects. IN this file we define many functions that check the configuration file and garantees that the user has properly entred the file parameters.

4- CTR_estimation.py: here we define the ctr estimation functions that we have used. 

5- Bidding_functions.py: here we define all the bidding functions that we use. Note that the majority of those bidding functions don't require a user defined parameters, all parameters are derrived from data statistics, except the optimal bidding functions that requiere the parameters lambda and c to be defined by the user. 

6- Data-statistics: here we compute the statistics of the historical data: CTR, CVR...

7- Auctions: here we define two functions, auction_based_adviser for mode1 and  auction_adviser_less for mode2. note that for speed raisons, we  tryed to implement those function in parrallele fashion. 

8- Generate_statistics.py: here we define two functions that generete statistics and write them in an output. generate_statistics_based_adviser and generate_statistics_adviser_Less. 

Finaly, note that tha data shoud be prepared based on the processing of this link https://github.com/wnzhang/make-ipinyou-data
