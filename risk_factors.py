import json
import copy
from encrypt import encrypt_data

#---------------------------------------------------------------------------------------
def save_risk_factors(bmi):
    #This is a json file containing standard clinical data in the OpenEHR standards form
    full_path_risk_factors_json = 'risk_factors_20231002120317_000001_1.json'
    #Demographic data file:
    with open(full_path_risk_factors_json, 'r') as openfile:
        # Reading from json file
        json_object_risk_factors = json.load(openfile)

    risk_factors=[]

    if(bmi>=30):
        risk_factors.append(copy.deepcopy(json_object_risk_factors))
        risk_factors[-1]["content"][0]["data"]["items"][1]["items"][0]["value"]["value"] = encrypt_data("OBESITY")
    
    return(risk_factors)