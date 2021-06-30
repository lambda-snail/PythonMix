
from os import path

import json
import pickle
import requests

SNAPSHOT_ENDPOINT   = "https://jobstream.api.jobtechdev.se/snapshot"
API_KEY_FILE        = path.join("..", "..", "..", "..", "API Keys", "jobtech-platsbanken.txt")

def GetAPIKey():
    key = ""
    with open(API_KEY_FILE,"r") as f:
        key = f.read()
    return key


def GetAllJobAds(apiKey: str):
    """Use the Platsbanken API to get a list of all jobs. Note that this can only be called once per minute, so the
    downloaded jobs should be saved locally."""
    headers = {'api-key': apiKey, 'accept': 'application/json'}
    response = requests.get(SNAPSHOT_ENDPOINT, headers=headers)
    response.raise_for_status()
    adList = json.loads(response.content.decode('utf8'))
    return adList


def GetTechJobsAds(adList):
    """Filter out all tech jobs (Data/IT) from the list of all jobs"""
    techAdList = filter(lambda ad: ad['occupation_field']['label'] == 'Data/IT', adList)
    return list(techAdList)


def SaveJobsToFile(filename: str, jobList: list):
    """Save a list of jobs to file."""
    outfile = open(filename, "rb")
    pickle.dump(jobList, filename)
    outfile.close()


def GetJobsFromFile(filename: str):
    """Retrieve a list of jobs from file. Warning: only use with files that you know are safe!"""
    infile = open(filename, "rb")
    adList = pickle.load(infile)
    infile.close()
    return adList
