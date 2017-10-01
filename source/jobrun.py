#!/opt/local/bin/python2.7

#Import Modules
import yaml
import subprocess
import os
import sys
import argparse
import shlex
import datetime
import importlib

# Import Local Modules
import validate


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




# Check for minimum requirements
if args.jobcard == None:
    print "Please provide a valid Job card: this is required"
    print parser.parse_args(['-h'])
    exit(1)
    
# If logfile is found open for writing

if args.logfile != None:
    print "Opening Log file: " + args.configfile
    log = open(args.logfile, 'w')        
else:
    print "Logging disabled"    

def logger(message):
        myTime = datetime.datetime.now()
        if args.logfile != None:
            log.write(str(myTime) + "-> " + message + "\n")
        else:
            print str(myTime) + "-> " + str(message)
            

# Check Job card is really there
if os.path.isfile(args.jobcard):
    logger("Job Card Exists: " + args.jobcard)
    job = open(args.jobcard,'r')
    jobcard = yaml.load(job)
else:
    logger("Job card invalid")
    exit(2)


    
#Open Config File

if os.path.isfile(args.configfile):
    logger("Config file exists")
    cfg = open(args.configfile,'r')
    config = yaml.load(cfg)
else:
    logger("Missing Config File")
    exit(2)

# Set Global short cuts
# Set Global Configuration Values

CURL=config['locations']['curl']
CONVERT=config['locations']['convert']
FFMPEG=config['locations']['ffmpeg']
FFPROBE=config['locations']['ffprobe']
MOGRIFY=config['locations']['mogrify']
FONT=config['boxcover']['font']


    
#===================================================================#
#                Global Variables                                   #
#===================================================================#

JobMatrix = {}
PartMatrix = {}
ErrorMatrix = {}
source = config['default']['source']
output = config['default']['assembly']
finish = config['default']['finish']
component = 'validate'
noexec = args.noexec


#===================================================================#
# Functions                                                         #
#===================================================================#

#===============================================================================
# Setup  Logging
#===============================================================================
import logging
import logging.config

logger = logging.getLogger(__name__)

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',disable_existing_loggers=False, level=logging.INFO)


#===============================================================================
# Main Code
#===============================================================================
logger.info(sys.argv[0] + "[Starting]")
logger.info('Starting Job Processing for ' + jobcard['clipinfo']['edgeid'])


# For debugging (Select only these and in order)
products = ['capture','box_cover','videoinfo','promoimg','photoset1','video1','video2' ]
product = ['description']


if not validate.produce(source, output, component, jobcard, config, noexec):
    logger.info("JobCard is valid")

# If Job Card is Good Code Goes Here

    for component in product:
        # Get Processing Module
        run_module = jobcard[component]['module']
        myModule = importlib.import_module(run_module)
        jobflag = jobcard['component'][component]
        
        if jobflag == 'produce':
            myModule.produce(source, output,  component, jobcard, config, noexec)
        elif jobflag == 'exists':
            myModule.exists(source, output,  component, jobcard, config, noexec)
        else:
            myModule.ignore(source, output,  component, jobcard, config, noexec)    



# JobCard doesn't validate
else:
    logger.error("Fix JobCard issues; then rerun")    

logger.info('[end program]')
