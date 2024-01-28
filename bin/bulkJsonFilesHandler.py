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

def file_mod(path,checkpoint_path):
    os.chdir(path)
    # print("Directory changed")
    for file in glob.glob("*.json"):
      # print(''' file name --> ''', file)
      file_complete_path = path+"\\"+file
      file_hash = str(hashlib.md5(file.encode()).hexdigest())+".txt"
      path_hash = str(hashlib.md5(path.encode()).hexdigest())
      checkpoint_path_final = os.path.join(checkpoint_path,path_hash,file_hash)
      if not os.path.isfile(checkpoint_path_final):
        #  print("Looks like a new file")
         with open(file_complete_path, mode='r') as f:
          data = json.load(f)
          print(json.dumps(data))
         os.chdir(checkpoint_path)
         if not os.path.isdir(path_hash):
          os.mkdir(path_hash)
         os.chdir(os.path.join(checkpoint_path,path_hash))
         file1 = open(file_hash, 'w+')
         file1.close()
      else:
        pass
        # print("This file was processed already")


# Routine to index data
def run_script():
    base_dir = r'C:\Soft Mania\Usecase 3\mkdir'
    checkpoint_path = r'C:\Program Files\SplunkUniversalForwarder\etc\apps\bulk_json_files_handler\checkpoints'
    for root, dirs, files in os.walk(base_dir):
        for dir in dirs:
            path = os.path.join(base_dir,dir)
            file_mod(path,checkpoint_path)

# Script must implement these args: scheme, validate-arguments
if __name__ == '__main__':
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