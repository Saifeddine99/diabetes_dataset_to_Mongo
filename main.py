# IF you want to remove all these records from databases run the clearing_databases.py script
# Import time module
import time
 
# record start time
start = time.time()
import pymongo as py
import csv
import uuid
import datetime
from age_compo import add_age_to_compo
from vital_status_compo import vital_status
from risk_factors import save_risk_factors
from problem_list import save_problem_list
from laboratory_tests import save_laboratory_test_results
from bmi_saving import save_bmi
from demographics import add_demographic_data
from encrypt import encrypt_data
#------------------------------------------------------------------------
myclient=py.MongoClient("mongodb://localhost:27017")
#Relating data to "clinical_data"
medical_data_coll=myclient["Clinical_database"]["Medical data"]
medical_hist_coll=myclient["Clinical_database"]["Medical history"]

#relating data to "demographic_database"
demographic_data_coll=myclient["Demographic_database"]["Demographic data"]
#---------------------------------------------------------------------------------------
#This line saves the csv file path to the "csv_file_path" variable
csv_file_path="Dataset of Diabetes .csv"

#This function returns "True" if value=='1' else it returns "False"
def diabetes_boolean(diabetes_):
    return diabetes_ == 'Y'

#This function returns "MALE" value if gender=="M" and "FEMALE" value if gender=="F"
def male_female(gender):
    if gender.upper()=='M':
        return "MALE"
    else:
        return "FEMALE"

with open(csv_file_path, 'r', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for idx, row in enumerate(csv_reader, start=1):
        #To avoid multiple saving of the same records we made this simple condition. So, before saving change the condition to idx>3000
        if idx>3000:
            break
        #uuid generation for each user:
        uuid_= str(uuid.uuid4())
        #generating a virtual phone number for each patient
        phone_number= "+"+str(idx+300)

        #data extraction:
        #assigning each value to its correspending variable:
        gender= male_female(row['Gender'])
        age= round(float(row['AGE']))
        urea= float(row['Urea'])
        cr= float(row['Cr'])
        hba1c= float(row['HbA1c'])
        chol= float(row['Chol'])
        tg= float(row['TG'])
        hdl= float(row['HDL'])
        ldl= float(row['LDL'])
        vldl= float(row['VLDL'])
        bmi= float(row['BMI'])
        diabetes= diabetes_boolean(row['CLASS'])

        # "problem_dict" is a dictionary containing the list of medical diseases existing in the csv file.(Here we only have diabetes)
        problem_dict={
            'diabetes':diabetes,
        }
        # "analyses_dict" is a dictionary containing the list of all analysis + their results existing in the csv file.
        analyses_dict={
            'urea': urea,
            'cr': cr,
            'hba1c': hba1c,
            'chol': chol,
            'tg': tg,
            'hdl': hdl,
            'ldl': ldl,
            'vldl': vldl,
        }

        #Giving anonymised values for resting demographic datapoints
        name,surname,country_of_birth,province_birth,town_birth,street_name,street_number,country,province,town="Patient",str(idx+300),"test","test","test","test",idx+300,"test","test","test"
        birthday="xxxx-xx-xx"
        dni="00000000X"
        postal_code="00000"
        current_date=str(datetime.date.today())
        #"add_demographic_data" is a function allowing to save the demographic data following the OpenEHR format. 
        json_object_demographic_data= add_demographic_data(name,surname,dni,gender,birthday,country_of_birth,province_birth,town_birth,street_name,street_number,postal_code,country,province,town)
        #This will be the structure of the document to be saved in the demographic db.
        demographic_doc={
                    "uuid": uuid_,
                    "phone number": encrypt_data(phone_number),
                    "current date": encrypt_data(current_date),
                    "demographic data": json_object_demographic_data
                }
        demographic_data_coll.insert_one(demographic_doc)

        #This will be the structure of the document to be saved in the medical data db.
        medical_data_dict={
            "uuid": uuid_,
            "saving date": encrypt_data(current_date),
            "problem list": save_problem_list(problem_dict),
            "risk factors": save_risk_factors(bmi),
            "vital status": vital_status("UNKNOWN"),#########
            "age":add_age_to_compo(age),
        }
        
        #This will be the structure of the document to be saved in the medical history db.
        medical_history_dict={
            "uuid": uuid_,
            "saving date": encrypt_data(current_date),
            "analytics": [save_laboratory_test_results(analyses_dict),save_bmi(bmi)],
        }

        medical_data_coll.insert_one(medical_data_dict)
        medical_hist_coll.insert_one(medical_history_dict)

#Here we're calculating the total time this script takes to save all records to db.
# record end time
end = time.time()

# print the difference between start and end time in milli. secs
print("The time of execution of above program is :",
    (end-start) * 10**3, "ms")