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
    
           
    MESSAGE = ''
    ERROR = ''
    WORK = ''
    NEWLINE = '\n'
    Error = False
    
    
    projectno = jobcard['clipinfo']['projectno']
    edgeid = jobcard['clipinfo']['edgeid']
    prime_dubya = jobcard['clipinfo']['prime_dubya']
    sourcedir = source + "/" + jobcard[component]['src']
    t_size = jobcard[component]['size']
    thumb_dir = jobcard[component]['out_dir']
    suffix = jobcard[component]['suffix']
    
    logger.info("Component:" + str(component))
    logger.info("\tSource Directory:" + sourcedir)
    
    CONVERT=config['locations']['convert']
    MOGRIFY=config['locations']['mogrify']
    
    
        
    destination = output + "/" + projectno + "/" +  prime_dubya +"/" + edgeid + "/" + jobcard[component]['out_dir'] 
    logger.info("\tDestination Directory: " + destination)
    
    if not os.path.isdir(destination + "/" ) and not noexec :
        os.makedirs(destination + "/" + thumb_dir,0777)
        logger.info("Creating Destination Directory: " + destination)
        
    
    

    if os.path.isdir(sourcedir):
        # Make Thumbnails for a directory
        
        logger.info("\tCreating thumbnails for a directory")
        for thumbfile in os.listdir(sourcedir):
            if filename.endswith(".tif") or filename.endswith(".jpg"):
                logger.info("\tCreate thumbnail for" + str(thumbfile))
                CMD = CONVERT + " " + sourcedir + " -thumbnail " + str(t_size) + " -set filename:fname '%t" + suffix + "' +adjoin '" + destination  + "/%[filename:fname].jpg'"  
                logger.info("Command: " + CMD)
                if not noexec:     
                    result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdoutdata, stderrdata = result.communicate()
                    status = result.returncode 
                    if status == 0:
                        logger.info("\t\t Thumbnail conversion returned Status: " + str(status))
                    else:
                        logger.warning("\t\t Thumbnail conversion failed with Status:"+ str(status))
                else:
                    # No Exec
                    logger.info("No Run")       
                    

    
    else:
        # Make one thumbnail for file.  
        # Make the assumption one file should be named edgeid + suffix
        logger.info("\tCreating thumbnails for a single file")
        logger.info("\rCreate thumbnail of " + sourcedir)
        CMD = CONVERT + " " + sourcedir + " -thumbnail " + str(t_size) + " -set filename:fname '" + edgeid + " " + suffix + "' +adjoin '" + destination  + "/%[filename:fname].jpg'"  
        logger.info("Command: " + CMD)
        if not noexec:     
            result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdoutdata, stderrdata = result.communicate()
            status = result.returncode 
            if status == 0:
                logger.info("\t\t Thumbnail conversion returned Status: " + str(status))
            else:
                logger.warning("\t\t Thumbnail conversion failed with Status:"+ str(status))
                Error = True
        else:
            # No Exec
            logger.info("No Run")       
            


       


    logger.info("Produce - End")
    return(Error)


def exists(source, output,  component, jobcard, config, noexec):
    logger.info("Exists - Start")
    
    logger.error("Not Valid")
    
    logger.info("Exists - End")
    return(Error)



def ignore(source, output,  component, jobcard, config, noexec):
    logger.info("Ignore - Start")
    
    logger.warning("Ignoring")
    
    logger.info("Ignore - End")
    return(Error)