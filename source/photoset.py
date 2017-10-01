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
    
    logger.info("\tModule Main - Start")
    # Start Code here
    
       
    MESSAGE = ''
    ERROR = ''
    WORK = ''
    NEWLINE = '\n'
    Error = False
    
    projectno = jobcard['clipinfo']['projectno']
    edgeid = jobcard['clipinfo']['edgeid']
    prime_dubya = jobcard['clipinfo']['prime_dubya']
    sourcedir = source + "/" + jobcard[component]['src']
    t_size = jobcard['thumbnails']['size']
    thumb_dir = jobcard['thumbnails']['out_dir']
    
    logger.info("\tSource Directory:" + sourcedir)
    
    CONVERT=config['locations']['convert']
    MOGRIFY=config['locations']['mogrify']
    
    destination = output + "/" + projectno + "/" +  prime_dubya +"/" + edgeid + "/" + jobcard[component]['out_dir'] + "_" + str(jobcard[component]['set_width']) + "x" + str(jobcard[component]['set_height'])
    if not os.path.isdir(destination + "/" + thumb_dir) and not noexec:
        os.makedirs(destination + "/" + thumb_dir,0777)
        logger.info("Creating Directory: " + destination)
        logger.info("\tincluding thumbnail dir")
        
        
    PhotoMatrix = {}
    ErrorMatrix = {}
    #=======================================================================
    # Produce Images
    #=======================================================================
    
    
    
    count = 0
        
    for filename in os.listdir(sourcedir):
        if filename.endswith(".tif") or filename.endswith(".jpg"): 
            logger.info( "\t\tcopying file " + filename + " to " + destination )
            CMD = CONVERT +" '" + sourcedir + "/" + filename + "' -resize " + str(jobcard[component]['set_width']) + "x" + str(jobcard[component]['set_height']) + " -set filename:mysize '%wx%h' '" + destination + "/" + edgeid + "_" + str(count).zfill(3) + ".jpg'; "           
            logger.warning ( "\t\tmakePhotoSetCMD\n  " + CMD  )
            if not noexec:    
                PhotoMatrix[count] = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                count = count + 1    
            else:
                logger.info( "ignoring file " + filename )
        
    if not noexec:
        # Wait for the last convert to complete. 
        for photo in range(0,count):
            logger.info( "  Checking on Photo # " + str(photo) + " to complete" )
            stdoutdata, stderrdata = PhotoMatrix[photo].communicate()
            status = PhotoMatrix[photo].returncode 
            if status == 0:
                logger.info(  "   Photo conversion returned Status: " + str(status))
            else:
                logger.warning(" Photo conversion failed with status code "+ str(status))
                Error = True
    else:
        logger.info("No run")
    
    #===========================================================================
    # Create Thumbnails
    #===========================================================================
    # Create Thumbnails for all of the images
    logger.info("\t\t Creating Thumbnails")
    
    CMD = MOGRIFY + " -path '" + destination + "/" + str(thumb_dir) +"' -thumbnail '" + str(t_size) + "' '" + destination + "/*.jpg'"
        
    logger.info("Creating Thumbnails in " + destination)
    logger.warning( " ThumbCMD\n  " + CMD )
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
        
    
    
    return(Error)

def produce(source, output,  component, jobcard, config, noexec):
    logger.info("Produce - Start")
    
    Error = main(source, output,  component, jobcard, config, noexec)
    
    logger.info("Produce - End")
    return(Error)


def exists(source, output,  component, jobcard, config, noexec):
    logger.info("Exists - Start")
    
    Error = main(source, output,  component, jobcard, config, noexec)
    
    logger.info("Exists - End")
    return(Error)



def ignore(source, output,  component, jobcard, config, noexec):
    logger.info("Ignore - Start")
    
    
    
    logger.info("Ignore - End")
    return(Error)