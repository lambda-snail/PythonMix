
# A Simple Job Ad Analyzer

This is my first attempt at using natural language processing and machine learning. The program downloads all ads from the Swedish Public Employment Agency, filters out those that have the tag "Data/IT" and categorize them using a k-means clustering algorithm.


## Installation 

There are two steps neccessary to get the code running.

1. The first step after downloading is to install all dependencies. This can be done manually or using the provided requirements.txt:    
```bash 
conda create --name <env> --file requirements.txt
```

2. Request an API key. This can be done [here](https://jobtechdev.se/en/products/jobstream). To get the API key into the code, look at the file JobAdsIO.py to see how to do this.

Note that the API can only be called once per minute. The program should automatically cache the ads the first time the program is run, and subsequent runs of the program should load the ads from "platsbanken-ads". If newer ads are required, this file should be deleted to force the program to call the API again.


## Roadmap

- The parameters of the model need tweaking, since the categories that are found are not really useful (yet).


  
