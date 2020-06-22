#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import os
import sys
import getopt
import requests
import re
import subprocess

target = ''
output = ''

def usage():
    print ""
    print "┌─┐┬ ┬┌┐ ┬  ┬┌─┐┌┐┌┬┌─┌─┐┌┐┌"
    print "└─┐│ │├┴┐└┐┌┘├┤ │││├┴┐│ ││││ By: Sam Paredes(CoffeeJunkie)"
    print "└─┘└─┘└─┘ └┘ └─┘┘└┘┴ ┴└─┘┘└┘ Twitter: @coffeejunkiee_"
    print ""
    print "Usage: subvenkon.py -d redacted.com"
    print "-h --help                           - Help"
    print "-d --domain                         - Domain to gather subdomains"
    print "Example:"
    print "subvenkon.py -d redacted.com"
    sys.exit(0)

def run_scan(scan, stderr=None):
    return subprocess.check_output(scan, shell=True, stderr=stderr, universal_newlines=True)

def main():
    global target
    global output
    
    if not len(sys.argv[1:]):
        print usage()
    
    try:
        opts, args = getopt.getopt(sys.argv[1:],"h:d:",["help","domain"])
    except getopt.GetoptError as err:
            print str(err)
            usage()
    
    for o,a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-d", "--domain"):
            target   = a   
        else:
            assert False, usage()
main()    


def input_work():

    global target

    if not len(target):
        print ""
        print "Something wrong has happened."
        print "Please type 'python subvenkon.py -h' for more options."
    elif target is not None:
        encoder =  base64.b64encode(bytes(target))
        url = "https://cloud.venkon.us/subdomain-lister-process/%s/dGVzdEB0ZXN0LmNvbQ=="%(encoder)
        r = requests.get(url)
        if "Done scan subdomains" in r.text:
            text = r.text
            start = text.find('loadJson("') + 10
            end = text.find('");', start)
            found = text[start:end]
            url2 = "https://cloud.venkon.us/subdomain-lister-report/%s"%(found)
            r2 = requests.get(url2)
            text2 = r2.text
            grep = "echo '%s' | grep '%s' | tr -d '                                    '"%(text2, target)
            run_scan(grep)
            grep2 = '''echo "%s"|  awk '{gsub("tr", "");print}' |  awk '{gsub("td", "");print}' |  awk '{gsub("h3", "");print}' |  awk '{gsub("<>", "");print}' |  awk '{gsub("</>", "");print}' |  awk '{gsub("<divclass=", "");print}' | awk '{gsub("TargetDomain:&nbsp;<songclass=", "");print}' |  awk '{gsub("</div>", "");print}'  | awk '{gsub("</song>", "");print}' |  awk '{gsub(">", "");print}' |  awk '{gsub("info-2-data", "");print}' |  awk '{gsub("target-host", "");print}' | tr -d '"'| awk '{gsub("&lt;BR&gt;", "\\n");print}' |  uniq  | tee -a %s-subvenkon.txt''' % (run_scan(grep),target)
            print run_scan(grep2)
        else:
            print "\nDid you type the correct domain? Try again!"
input_work()