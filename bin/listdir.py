import os
import json

# def files_dir(path):
#   for root, dirs, files in os.walk(path):
#     for file in files:
#       print(json.dumps({"file":file}))
   
# path = os.getcwd()
# path = r'C:\Soft Mania\Usecase 3\mkdir\folder_6'
# files_dir(path)

f = open(r'C:\Soft Mania\Usecase 3\mkdir\folder_6\file_1.json')
data = json.load(f)
 
# Iterating through the json
# list
print(data)
 
# Closing file
f.close()