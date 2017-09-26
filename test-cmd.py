#!/usr/bin/python

# import
import sys
import os
import argparse

# Parse the Command Line

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")
parser.add_argument("-j", "--jobcard", type=str, action="store", help="jobcard.yml file to process")
parser.add_argument("-l","--logfile", action="store", help="Write Logfile if ommitted write to STDOUT")
parser.add_argument("-c","--configfile", default="config.yml", help="use config file, default is config.yml in working dir")
args = parser.parse_args()
print args

# Check for minimum requirements
if args.jobcard == None:
    print "Please provide a valid Job card: this is required"
    print parser.parse_args(['-h'])
    exit(1)
    
 