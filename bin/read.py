import json
import os
import codecs

from datetime import date

current_date = date.today()

config = {}
with open(os.path.join("C:\\","Program Files","SplunkUniversalForwarder","etc","apps","bulk_json_files_handler","default","inputs.json"),"r") as file:
    inputs = json.load(file)
    config=inputs
    # print(inputs["data_source"])

def read_and_index_the_data_with_checkpoint(foldername, filename):
    print(foldername,filename)
    file_complete_path = os.path.join(foldername,filename)
    try:
        with codecs.open(file_complete_path, mode='r', encoding="utf-8-sig") as f:
            data = json.load(f)
            print(json.dumps(data))
    except Exception as error:
        # handle the exception
        error_data = {}
        error_data["status_code"] = 500
        error_data["file_path"] = file_complete_path
        error_data["error"] = str(error)
        print(json.dumps(error_data))

root_path = os.path.join("C:\\","Program Files","SplunkUniversalForwarder","etc","apps","bulk_json_files_handler","bin","__svclog__")
subFolder_level_1 = os.listdir(root_path)
for folder in subFolder_level_1:
    print("folder --> ", folder)
    path_level_1 = os.path.join(root_path,folder) # path_level_1 = .....\__svclog__\BudgetCalc
    subFolder_level_2 = os.listdir(path_level_1) # subFolder_level_2 = ['2024-01-24', '2024-02-03', 'backup', 'test.json']
    print(subFolder_level_2)
    for item in subFolder_level_2:
        print("item --> ",item) # '2024-01-24', '2024-02-03', 'backup', 'test.json'
        check_path = os.path.join(path_level_1,item) # C:\Program Files\SplunkUniversalForwarder\etc\apps\bulk_json_files_handler\bin\__svclog__\BudgetCalc\2024-01-24
        # print(check_path, os.path.isfile(check_path))
        if os.path.isfile(check_path):
            # print("testing for file")
            file_name = folder
            read_and_index_the_data_with_checkpoint(path_level_1, item)
    
        if os.path.isdir(check_path):
            # print("testing for folder --> ", str(item), str(current_date))
            if item == str(current_date): # comment this line to disable the current date filter
            # if True: # uncomment this line to index all the date folders
                print("it is matching with today's date")
                for file in os.listdir(check_path):
                    if os.path.isfile(os.path.join(check_path,file)):
                        # print("testing for file inside the folder")
                        read_and_index_the_data_with_checkpoint(check_path, file)
            
            
            else:
                print("this is not a right folder as it is not matching with today's date")

# # for (root,dirs,files) in os.listdir(os.path.join("C:\\","Program Files","SplunkUniversalForwarder","etc","apps","bulk_json_files_handler","bin","__svclog__")):
# #     print (root) 
# #     print (dirs) 
# #     print (files) 
# #     print ('--------------------------------')
