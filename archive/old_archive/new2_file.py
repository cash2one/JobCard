'''
Created on Sep 30, 2017

@author: colin
'''
import yaml
import importlib
import os
import sys

# Import Local Modules
import validate


#===============================================================================
# Setup test Logging
#===============================================================================
import logging
import logging.config

logger = logging.getLogger(__name__)



logging.basicConfig(format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',disable_existing_loggers=False, level=logging.INFO)




component = 'promoimg'
prefix = '/Users/colin/Documents/Appcelerator_Studio_Workspace/JobCard/Assembly/'
source = '/Users/colin/Documents/Appcelerator_Studio_Workspace/JobCard/EdgeSource01'
finish = '/Users/colin/Documents/Appcelerator_Studio_Workspace/JobCard/Finished'
card = '/Users/colin/Documents/Appcelerator_Studio_Workspace/JobCard/example/edge0022.yaml'
job = open('/Users/colin/Documents/Appcelerator_Studio_Workspace/JobCard/example/edge0022.yaml','r')
cfile = open('/Users/colin/Documents/Appcelerator_Studio_Workspace/JobCard/example/config.yaml','r')
noexec = False
jobcard = yaml.load(job)
config = yaml.load(cfile)
jobflag = 'exists'

#destination = prefix + jobcard['clipinfo']['projectno'] + "/" + jobcard['clipinfo']['prime_dubya'] + "/" + jobcard['clipinfo']['edgeid']
#if not os.path.isdir(destination):
#        os.makedirs(destination,0777)
logger.info(sys.argv[0] + "[Starting]")
logger.info('Starting Job Processing for ' + jobcard['clipinfo']['edgeid'])



if not validate.produce(source, prefix, component, jobcard, config, noexec):
    logger.info("JobCard is valid")
else:
    logger.error("Fix JobCard issues; then rerun")    

logger.info('[end program]')
