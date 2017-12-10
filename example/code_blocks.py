# Variables for standard use:

config = {}
jobcard = {}
noexec = True
command = {}
command_status = {}
command_name = "example"
CMD = ''
item_src = ''

# Standard Imports
import os
import job
import logging
import subprocess


logger = logging.getLogger(__name__)



# Code Block - Run a command an check results

# 
command_name = 'MyCommand'

# Run Command

if noexec:
    command[command_name] = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
else:
    logger.warning("Running Command - " + str(command_name))  
    command[command_name] = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)       
    logger.info( "COMMAND" + command_name + " for "+ item_src + " Started" )
    

# Check if Command executed
logger.info("Check if " + str(command_name) + " Completed")
stdoutdata, stderrdata = command[command_name].communicate()
command_status[command_name] = command[command_name].returncode 
if command_status[command_name] == 0:
    logger.info(str(command_name) + " Completed, returned Status: " + str(command_status[command_name]))
else:
    logger.error(str(command_name) + "failed, with Status:"+ str(command_status[command_name]))
    Error = True

        