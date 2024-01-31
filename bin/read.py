import json
import os

with open(os.path.join("C:\\","Program Files","SplunkUniversalForwarder","etc","apps","bulk_json_files_handler","default","inputs.json"),"r") as file:
    inputs = json.load(file)
    print(inputs["data_source"])