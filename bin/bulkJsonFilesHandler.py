# $SPLUNK_HOME/etc/apps/helloworld/bin/hello.py
from __future__ import print_function
import sys
sys.path.append("./python-3.12.1/")
from builtins import str
import xml.dom.minidom, xml.sax.saxutils
import os
import glob
import json
import hashlib
import codecs

from datetime import date

current_date = date.today()

# Empty introspection routine
def do_scheme():
    print("in scheme")
    pass

# Empty validation routine. This routine is optional.
def validate_arguments():
    pass

# Routine to get the value of an input
def get_path():
    try:
        # read everything from stdin
        config_str = sys.stdin.read()

        # parse the config XML
        doc = xml.dom.minidom.parseString(config_str)
        root = doc.documentElement
        conf_node = root.getElementsByTagName("configuration")[0]
        if conf_node:
            stanza = conf_node.getElementsByTagName("stanza")[0]
            if stanza:
                stanza_name = stanza.getAttribute("name")
                if stanza_name:
                    params = stanza.getElementsByTagName("param")
                    for param in params:
                        param_name = param.getAttribute("path")
                        if param_name and param.firstChild and \
                           param.firstChild.nodeType == param.firstChild.TEXT_NODE and \
                           param_name == "path":
                            return param.firstChild.data
    except Exception as e:
        raise Exception("Error getting Splunk configuration via STDIN: %s" % str(e))

    return ""

def read_and_index_the_data_with_checkpoint(file_complete_path):
    try:
        print(file_complete_path)
        with codecs.open(file_complete_path, mode='r', encoding="utf-8-sig") as f:
            data = json.load(f)
            print(json.dumps(data))
            return True
    except Exception as error:
        # handle the exception
        error_data = {}
        error_data["status_code"] = 500
        error_data["file_path"] = file_complete_path
        error_data["error"] = str(error)
        print(json.dumps(error_data))
        return False


def file_mod(path,checkpoint_path):
    os.chdir(path)
    print("Directory changed")
    if not os.path.isdir(checkpoint_path):
        os.mkdir(checkpoint_path)
    path_level_1 = path
    subFolder_level_2 = os.listdir(path_level_1)
    for item in subFolder_level_2:
        check_path = os.path.join(path_level_1,item)
        if os.path.isfile(check_path) and check_path.endswith(".json"):
            file_hash = str(hashlib.md5(item.encode()).hexdigest())+".txt"
            path_hash = str(hashlib.md5(path_level_1.encode()).hexdigest())
            checkpoint_path_final = os.path.join(checkpoint_path,path_hash,file_hash)
            if not os.path.isfile(checkpoint_path_final):
                print("This file is completely new processing it")
                isFileProcessed = read_and_index_the_data_with_checkpoint(check_path)
                if isFileProcessed:
                    os.chdir(checkpoint_path)
                    if not os.path.isdir(path_hash):
                        os.mkdir(path_hash)
                    os.chdir(os.path.join(checkpoint_path,path_hash))
                    file1 = open(file_hash, 'w+')
                    file1.close()
            else:
                print("This file is already processed")
        if os.path.isdir(check_path):
            # if item == str(current_date): # comment this line to disable the current date filter
            if True: # uncomment this line to index all the date folders
                for file in os.listdir(check_path):
                    file_inside_folder_path = os.path.join(check_path,file)
                    if os.path.isfile(file_inside_folder_path):
                        file_hash = str(hashlib.md5(file.encode()).hexdigest())+".txt"
                        path_hash = str(hashlib.md5(check_path.encode()).hexdigest())
                        checkpoint_path_final = os.path.join(checkpoint_path,path_hash,file_hash)
                        if not os.path.isfile(checkpoint_path_final):
                            print("This file is completely new processing it")
                            isFileProcessed = read_and_index_the_data_with_checkpoint(file_inside_folder_path)
                            if isFileProcessed:
                                os.chdir(checkpoint_path)
                                if not os.path.isdir(path_hash):
                                    os.mkdir(path_hash)
                                os.chdir(os.path.join(checkpoint_path,path_hash))
                                file1 = open(file_hash, 'w+')
                                file1.close()
                        else:
                            print("This file is already processed")
        

    # for file in glob.glob("*.json"):
    # #   print(''' file name --> ''', file)
    #   file_complete_path = path+"\\"+file
    #   file_hash = str(hashlib.md5(file.encode()).hexdigest())+".txt"
    #   path_hash = str(hashlib.md5(path.encode()).hexdigest())
    #   checkpoint_path_final = os.path.join(checkpoint_path,path_hash,file_hash)
    #   if not os.path.isfile(checkpoint_path_final):
    #     #  print("Looks like a new file")
    #     #  with codecs.open(file_complete_path, mode='r', encoding="utf-8-sig") as f:
    #     #   data = json.load(f)
    #     #   print(json.dumps(data))
    #      read_and_index_the_data_with_checkpoint(file_complete_path)
    #      os.chdir(checkpoint_path)
    #      if not os.path.isdir(path_hash):
    #       os.mkdir(path_hash)
    #      os.chdir(os.path.join(checkpoint_path,path_hash))
    #      file1 = open(file_hash, 'w+')
    #      file1.close()
    #   else:
    #     pass
        # print("This file was processed already")


# Routine to index data
def run_script():
    print("run_script")
    base_dir = ""
    checkpoint_path = ""
    with open(os.path.join("C:\\","Program Files","SplunkUniversalForwarder","etc","apps","bulk_json_files_handler","default","inputs.json"),"r") as file:
        inputs = json.load(file)
        print("opened inputs.conf")
        base_dir = inputs["data_source"]
        checkpoint_path = inputs["checkpoints_directory"]
        # print(base_dir, checkpoint_path)
    for dir in os.listdir(base_dir):
        print(dir)
        # for dir in dirs:
        path = os.path.join(base_dir,dir)
        # print("calling file_mod")
        file_mod(path,checkpoint_path)

# Script must implement these args: scheme, validate-arguments
if __name__ == '__main__':
    print("main")
    if len(sys.argv) > 1:
        if sys.argv[1] == "--scheme":
            do_scheme()
        elif sys.argv[1] == "--validate-arguments":
            validate_arguments()
        else:
            pass
    else:
        run_script()

    sys.exit(0)