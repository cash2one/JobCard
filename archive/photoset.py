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
    suffix = jobcard[component]['suffix']
    t_suffix =jobcard['thumbnails']['suffix']
    
    logger.info("\tSource Directory:" + sourcedir)
    
    CONVERT=config['locations']['convert']
    MOGRIFY=config['locations']['mogrify']
    
    # Check if thumbnails are needed
    if jobcard['component']['thumbnails'] == 'produce' or jobcard['component']['thumbnails'] == 'validate':
        make_thumbnail = True
        logger.info("\tMaking Thumbnails")
    else:   
        make_thumbnail = False   
        
    destination = output + "/" + projectno + "/" +  prime_dubya +"/" + edgeid + "/" + jobcard[component]['out_dir'] 
    
    if not os.path.isdir(destination + "/") and not noexec:
        os.makedirs(destination,0777)
        logger.info("Creating Directory: " + destination)
        
    if not os.path.isdir(destination + "/" + thumb_dir) and not noexec and make_thumbnail:
        os.makedirs(destination + "/" + thumb_dir,0777)
        logger.info("Creating Thumbnail Directory: " + destination + "/" + thumb_dir)
        
        
    PhotoMatrix = {}
    ErrorMatrix = {}
    #=======================================================================
    # Copy Images
    #=======================================================================
    
     
    
    
    count = 0
        
    for filename in os.listdir(sourcedir):
        if filename.endswith(".tif") or filename.endswith(".jpg"): 
            logger.info( "\tcopying file " + filename + " to " + destination )
            CMD = CONVERT +" '" + sourcedir + "/" + filename + "' -resize " + str(jobcard[component]['set_width']) + "x" + str(jobcard[component]['set_height']) + " -set filename:mysize '%wx%h' '" + destination + "/" + edgeid + "_" + str(count).zfill(3) + "_" + str(jobcard[component]['set_width']) + "x" + str(jobcard[component]['set_height'])+ suffix + "'"           
            logger.warning ( "\tmakePhotoSetCMD\n  " + CMD  )
            if not noexec:    
                PhotoMatrix[count] = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                count = count + 1    
        else:
            logger.warning( "\tignoring file " + filename )
        
    if not noexec:
        # Wait for the last convert to complete. 
        for photo in range(0,count):
            logger.info( "\tChecking on Photo # " + str(photo) + " to complete" )
            stdoutdata, stderrdata = PhotoMatrix[photo].communicate()
            status = PhotoMatrix[photo].returncode 
            if status == 0:
                logger.info(  "\tPhoto conversion returned Status: " + str(status))
            else:
                logger.warning("\tPhoto conversion failed with status code "+ str(status))
                Error = True
    else:
        logger.info("No run")
        for photo in range(0,count):
            logger.info('\tDestination:' + destination)
            logger.info( "\tChecking on Photo # " + str(photo) + " to complete" )
            
    
    #===========================================================================
    # Create Thumbnails
    #===========================================================================
   
    if make_thumbnail:
    # Create Thumbnails for all of the images
        logger.info("\t\t Creating Thumbnails")
        
        CMD = CONVERT + " " + destination + "/*.jpg  -thumbnail " + str(t_size) + " -set filename:fname '%t" + t_suffix + "' +adjoin '" + destination + "/" + thumb_dir + "/%[filename:fname].jpg'"  
        
        
        logger.info("Creating Thumbnails from " + destination)
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