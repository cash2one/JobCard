#!/usr/bin/python

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
    









#===================================================================#
# Functions                                                         #
#===================================================================#

#===============================================================================
# Setup  Logging
#===============================================================================
import logging
import logging.config



logger = logging.getLogger(__name__)

logging.basicConfig(filename=args.logfile, disable_existing_loggers=False,format='%(asctime)s %(name)s:%(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)



       
#===============================================================================
# Pre Main Code
#===============================================================================
# Check Job card is really there
if os.path.isfile(args.jobcard):
    logger.info("Job Card Exists: " + args.jobcard)
    job = open(args.jobcard,'r')
    jobcard = yaml.load(job)
else:
    logger.info("Job card invalid")
    exit(2)


    
#Open Config File

if os.path.isfile(args.configfile):
    logger.info("Config file exists")
    cfg = open(args.configfile,'r')
    config = yaml.load(cfg)
else:
    logger.info("Missing Config File")
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
    
#===============================================================================
# Main Code
#===============================================================================
logger.info(sys.argv[0] + "[Starting]")
logger.info('Starting Job Processing for ' + jobcard['clipinfo']['edgeid'])


# For debugging (Select only these and in order)
products = ['capture','videoinfo','promoimg','photoset1','description_txt','boxcover','video1', 'video2']
productZ = ['photoset1']


if not validate.produce(source, output, component, jobcard, config, noexec):
    logger.info("JobCard is valid")

debug = True

if debug == True:
# If Job Card is Good Code Goes Here
    logger.info('Creating Components')
    for component in jobcard['component']:
    #for component in productZ:
        # Get Processing Module
        logger.warning("Processing Component " + str(component))
        run_module = jobcard[component]['module']
        myModule = importlib.import_module(run_module)
        jobflag = jobcard['component'][component]
        logger.warning("Job Flag: " + jobflag)
        
        if jobflag == 'produce':
            myModule.produce(source, output,  component, jobcard, config, noexec)
        elif jobflag == 'exists':
            myModule.exists(finish, output,  component, jobcard, config, noexec)
        else:
            myModule.ignore(source, output,  component, jobcard, config, noexec)    

    
    logger.info("Creating Products")

    if debug == True:    

        for product in jobcard['product']:
            logger.info("Make " + product)
            # Get Processing Module
            run_module = jobcard[product]['module']
            myModule = importlib.import_module(run_module)
            jobflag = jobcard['product'][product]
            output = config['default']['scratch']
            source = config['default']['assembly']
            component = product
            
            if jobflag == 'produce':
                myModule.produce(source, output,  component, jobcard, config, noexec)
            elif jobflag == 'exists':
                myModule.exists(finish, output,  component, jobcard, config, noexec)
            else:
                #myModule.ignore(source, output,  component, jobcard, config, noexec)  
                logger.warning("Ignoring product " + product)          
        
 

# JobCard doesn't validate
else:
    logger.error("Fix JobCard issues; then rerun")    

logger.info('[end program]')
