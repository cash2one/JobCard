'''
Created on Sep 30, 2017

@author: colin
'''

#===============================================================================
# Import 
#===============================================================================

import os
from string import Template
import logging
import subprocess
import getvideosize

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
    
        

    FFMPEG=config['locations']['ffmpeg']
    MOGRIFY=config['locations']['mogrify']

    
    MESSAGE = ''
    ERROR = ''
    NEWLINE = '\n'
    WORK = ''
    Error = False
    
    # Define Parameters
    video =  source + "/" +jobcard['video']['src']
    seconds = jobcard['capture']['frame_every']
    projectno = jobcard['clipinfo']['projectno']
    edgeid = jobcard['clipinfo']['edgeid']
    prime_dubya = jobcard['clipinfo']['prime_dubya']
    videoName = os.path.basename(video)
    pathName = os.path.dirname( source + "/" + video)
    t_size = jobcard['thumbnails']['size']
    thumb_dir = jobcard['thumbnails']['out_dir']
    
    
    # Get video Size 
    Error, SizeOfVideo, Duration, Bitrate  = getvideosize.produce(source, output, component, jobcard, config, noexec)
    
    # We need the size to name the capture directory
    
    destination = output + "/" + projectno + "/" +  prime_dubya +"/" + edgeid + "/" + jobcard[component]['out_dir'] 
    
    
    if not os.path.isdir(destination + "/" + thumb_dir) and not noexec:
        os.makedirs(destination + "/" + thumb_dir,0777)
        logger.info("Creating Directory: " + destination)
        logger.info("\tincluding thumbnail dir")
        
        
        
    logger.info("Make Stills for Video: " + videoName )
    logger.info("Source Dir:"  + pathName )
    logger.info("Put Stills in Destination:\n  " )
    logger.info("\t\t"+destination)
    

    
    
    
           
   
    CMD = FFMPEG + " -c:v h264_vda -i '"  + video + "' -thread_type slice -hide_banner -vf fps=1/" + str(seconds) + "  -c:v mjpeg '" + destination + "/" + edgeid  + "_capture_%03d.jpg'" 
    
    logger.info("Making stills from video:" + video + " Size:" + str(SizeOfVideo) + " Duration:" + str(Duration) + " seconds @ bitrate:" + str(Bitrate) )
    logger.warning("StillCommand:\n  " + CMD )
    
    if noexec:
        logger.info( "No Execute" )
        result=subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        logger.warning("Running Command" )  
        result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdoutdata, stderrdata = result.communicate()
        status = result.returncode 
        if status == 0:
            logger.info("\t\t Capture returned Status: " + str(status))
        else:
            logger.warning("\t\t Capture failed with Status:"+ str(status))
            Error = True 
    
     
    logger.info( "Capture on " + videoName + " Completed" )
        
 
 
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


def exists(source, output,  component, jobcard, config, noexec):
    logger.info("Exists - Start")
    
    logger.warning("Not Valid")
    
    logger.info("Exists - End")
    return(Error)



def ignore(source, output,  component, jobcard, config, noexec):
    logger.info("Ignore - Start")
    
    
    
    logger.info("Ignore - End")
    return(Error)