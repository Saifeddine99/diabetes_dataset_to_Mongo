#By running this script, we can remove all the data extracted from the csv file and added to Mongo
from paths import parameter_to_directory
import pymongo as py
from encrypt import encrypt_data
#---------------------------------------------------------------------------------------
myclient=py.MongoClient("mongodb://localhost:27017")
#Relating data to "clinical_data"
medical_data_coll=myclient["Clinical_database"]["Medical data"]
medical_hist_coll=myclient["Clinical_database"]["Medical history"]

#relating data to "demographic_database"
demographic_data_coll=myclient["Demographic_database"]["Demographic data"]
#---------------------------------------------------------------------------------------
#All the people added using the "main.py" script will have the name:"Patient"
#To correctly query the encrypted names, We'll start with encrypting the name and then applying it to the .find function in pymongo.
cipher_name = encrypt_data("Patient")

cursor= demographic_data_coll.find({parameter_to_directory("Name"): cipher_name,})

uuid_list=[]
for demog_doc in cursor:
    uuid_list.append(demog_doc["uuid"])

medical_data_coll.delete_many({"uuid": {"$in":uuid_list}})
medical_hist_coll.delete_many({"uuid": {"$in":uuid_list}})
demographic_data_coll.delete_many({"uuid": {"$in":uuid_list}})