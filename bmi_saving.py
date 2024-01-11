# Here, we'll be saving bmi score as a string (Because of encryption)
import json
from encrypt import encrypt_data

def save_bmi(current_bmi):
    #This is a json file containing standard clinical data in the OpenEHR standards form
    full_path_bmi_json = 'bmi_20231002121554_000001_1.json'
    #Demographic data file:
    with open(full_path_bmi_json, 'r') as openfile:
        # Reading from json file
        json_object_bmi = json.load(openfile)

    json_object_bmi["content"][2]["data"]["events"][0]["data"]["items"][0]["value"]["magnitude"]=encrypt_data(str(current_bmi))

    return(json_object_bmi)