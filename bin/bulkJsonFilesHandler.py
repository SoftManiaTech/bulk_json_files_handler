# $SPLUNK_HOME/etc/apps/helloworld/bin/hello.py
from __future__ import print_function
from builtins import str
import sys
import xml.dom.minidom, xml.sax.saxutils
import os

# Empty introspection routine
def do_scheme():
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

# Routine to index data
def run_script():
    # the folders with sample data structure
    # python logic to index the list of json files
    for root, dirs, files in os.walk(get_path()):
        for file in files:
            print("hello world, %s!" % file)

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