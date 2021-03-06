'''
Created on Sep 30, 2017

@author: colin
'''

#===============================================================================
# Import 
#===============================================================================

import os
import subprocess
from string import Template
import logging
logger = logging.getLogger(__name__)

#===============================================================================
# Setup Commnands for Produce and Exists
#===============================================================================

CMD_PRODUCE = ''

CMD_EXISTS = ''

#===============================================================================
# Module Global Variables
#===============================================================================

MESSAGE = ''
ERROR = ''
NEWLINE = '\n'
Error = False



def main (source, output,  component, jobcard, config, noexec):
    #===============================================================================
    # Module Global Variables
    #===============================================================================
    
    CURL=config['locations']['curl']
    CONVERT=config['locations']['convert']
    FFMPEG=config['locations']['ffmpeg']
    FFPROBE=config['locations']['ffprobe']
    MOGRIFY=config['locations']['mogrify']
    FONT=config['boxcover']['font']
    
    logger.debug("CURL = " + CURL)
    logger.debug("CONVERT = " + CONVERT)
    logger.debug("FFMPEG = " + FFMPEG)
    logger.debug("FFPROBE = " + FFPROBE)
    logger.debug("MOGRIFY = " + MOGRIFY)
    logger.debug("FONT = " + FONT)
    
    logger.info("Produce - Module Main - Start")
    # Start Code here
    
    
    logger.info("Produce - Module Main - Start")
    
    return(Error)

def produce(source, output,  component, jobcard, config, noexec):
    
    logger.info("Produce - Start")
    
    FFPROBE=config['locations']['ffprobe']
    projectno = jobcard['clipinfo']['projectno']
    edgeid = jobcard['clipinfo']['edgeid']
    prime_dubya = jobcard['clipinfo']['prime_dubya']
    video = source + "/" + jobcard['video']['src']
    videoName = os.path.basename(video)
    pathName = os.path.dirname( source + "/" + video)
    
    set_src = source + "/" + jobcard[component]['src']
    set_dir = jobcard[component]['out_dir']
    set_width = jobcard[component]['set_width']
    set_height = jobcard[component]['set_height']
    if jobcard[component]['suffix'] == None:
        set_suffix = "__"
    else:    
        set_suffix =  jobcard[component]['suffix']
    set_ext =  jobcard[component]['ext']
    set_timed =  jobcard[component]['timed']
    set_name = jobcard[component]['name']

    
    Error = False
    
    logger.info("\tGetting Information about video:" + video )
    logger.info("\tDestination: "+ destination)
    
   destination = output + "/" + projectno + "/" + prime_dubya + "/" + edgeid
    
    # Create Directories if needed
    if not os.path.isdir(destination + "/" + set_name + "/" + set_dir) and not noexec:
        os.makedirs(destination + "/" + set_name + "/" + set_dir,0777)
        logger.info("Creating Directory: " + destination + "/" + set_name + "/" + set_dir)
    else:
        logger.info("Creating Directory: " + destination + "/" + set_name + "/" + set_dir)   
    
    for format in ['csv', 'json', 'xml']:
            logger.info("Output Video Information in " + format )
            logger.info("Output Location:\n" + pathName)
        
            CMD = FFPROBE + " -v error -show_format -show_streams -print_format " + format + " '" +  video + "' > '" + destination +"/" + edgeid + "-info" +"."+ format +"'"
            logger.warning("\tCommand:\n\t" + CMD)
            if noexec:
                logger.warning("No execute") 
            else:    
                result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)        
                stdoutdata, stderrdata = result.communicate()
                status = result.returncode
            
                if not status == 0:
                    Error = True
                    logger.error("Command Error Code: " + status) 
                else:
                    logger.info("Return Code Successul")      

    
    logger.info("Produce - End")
    return(Error)


def exists(source, output,  component, jobcard, config, noexec):
    logger.info("Exists - Start")
    
    logger.error("Not Valid")
    Error = True
    
    logger.info("Exists - End")
    return(Error)



def ignore(source, output,  component, jobcard, config, noexec):
    logger.info("Ignore - Start")
    
    
    
    logger.info("Ignore - End")
    return(Error)