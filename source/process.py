#!/opt/local/bin/python2.7

#Import Libraries
import yaml
import subprocess
import os
import sys
import argparse
import shlex
import datetime



# Parse the Command Line

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true", help="Display detailed debugging information")
group.add_argument("-q", "--quiet", action="store_true")
parser.add_argument("-j", "--jobcard", action="store", help="jobcard.yml file to process")
parser.add_argument("-l","--logfile", action="store", help="Write Logfile if ommitted write to STDOUT")
parser.add_argument("-c","--configfile", default="config.yml", help="use config file, default is config.yml in working dir")
parser.add_argument("-n","--noexec", action="store_true", help="Do not run commands on the OS; echo the command on the OS only" )

args = parser.parse_args()
print args

__all__ = []
__version__ = 0.1
__date__ = '2017-09-29'
__updated__ = '2017-09-29'

DEBUG = 1
TESTRUN = 0
PROFILE = 1

