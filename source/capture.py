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
logger = logging.getLogger(__name__)

#Additional Libraries
import subprocess
import getvideosize
from os.path import basename


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
    
    FFMPEG=config['locations']['ffmpeg']
    MOGRIFY=config['locations']['mogrify']
    CONVERT=config['locations']['convert']


    logger.info("Produce - Start")
    logger.info("Source: " + str(source))
    logger.info("Output: " + str(output))

    
    if noexec:
        logger.info("Don't execute any commands for real, test mode only")
    
    # Set common variables for Components
    # Relative to the component being passed. 
    # If value is not present; prevent an error
    
    # Setup the Output Destination
    projectno = jobcard['clipinfo']['projectno']
    edgeid = jobcard['clipinfo']['edgeid']
    prime_dubya = jobcard['clipinfo']['prime_dubya']
    destination = output + "/" + projectno + "/" + prime_dubya + "/" + edgeid
    
    
    try:
        item_src = jobcard[component]['src'] if "src" in jobcard[component] else None
        item_width = jobcard[component]['set_width'] if "set_width" in jobcard[component] else None
        item_height = jobcard[component]['set_height'] if "set_height" in jobcard[component] else None
        item_kbps =  jobcard[component]['set_kbps'] if "set_kbps" in jobcard[component] else None
        item_outdir = jobcard[component]['out_dir'] if "out_dir" in jobcard[component] else None
        item_suffix = jobcard[component]['suffix'] if "suffix" in jobcard[component] else None
        item_ext = jobcard[component]['ext'] if "ext" in jobcard[component] else None
        item_name = jobcard[component]['name'] if "name" in jobcard[component] else None
        item_thumbnail = jobcard[component]['thumbail'] if "thumbail" in jobcard[component] else None
        item_watermark = jobcard[component]['watermark'] if "watermark" in jobcard[component] else None
        item_count = jobcard[component]['count'] if "count" in jobcard[component] else None
        item_timed = jobcard[component]['timed'] if "timed" in jobcard[component] else None
        item_size = jobcard[component]['size'] if "size" in jobcard[component] else None
    except:
         logger.warning("Not all variables set properly")   
    # Test Source for relative or absoulte path
    
    if item_src[0] != "/":                       
        logger.debug("Relative Path")    
        item_source = source + "/" + item_src
    else:
        logger.debug("Absolute Path")
        item_source = jobcard[component]['src']  
    
        #setup final destination in complex situations
    if not item_name == None and not item_outdir == None:
        finaldestination = destination + "/" + str(item_name) + "/" + str(item_outdir)
    elif not item_name == None and item_outdir == None:
        finaldestination = destination + "/" + str(item_name)
    elif item_name == None and not item_outdir == None:
        finaldestination = destination + "/" + str(item_outdir)     
    else:
        finaldestination = destination
     
     
    logger.info("\tItem Src: " + str(item_src))
    logger.info("\tItem Source: " + str(item_source))
    logger.info("\tDestination: " + str(destination))
    logger.info("\tFinal Destination: " + str(finaldestination))
    logger.info("\tItem Width: " + str(item_width))   
    logger.info("\tItem Height: " + str(item_height))  
    logger.info("\tItem Kbps: " + str(item_kbps))  
    logger.info("\tItem Name: " + str(item_name))
    logger.info("\tItem Outdir: " + str(item_outdir))
    logger.info("\tItem Suffix: " + str(item_suffix))
    logger.info("\tItem Ext: " + str(item_ext))
    logger.info("\tItem Thumbnail: " + str(item_thumbnail))
    logger.info("\tItem Watermark: " + str(item_watermark))
    logger.info("\tItem Count: " + str(item_count))
    logger.info("\tItem Timed: " + str(item_timed))
    logger.info("\tItem Size: " + str(item_size))   
             
    # Create Directories if needed
    if not os.path.isdir(finaldestination) and not noexec:
        os.makedirs(finaldestination,0777)
        logger.info("Creating Directory: " + finaldestination)
    else:
        logger.info("Creating Directory: " + finaldestination)   

    # Get video Size 
    Error, SizeOfVideo, Duration, Bitrate  = getvideosize.produce(source, output, component, jobcard, config, noexec)
    
    logger.info("Make Stills for Video: " + item_src )
    logger.info("Component Destination: " + destination)
    logger.info("Put Stills in Destination:\n  " + finaldestination)
    
    
    logger.info("Produce - End")
    return(Error)


def exists(source, output,  component, jobcard, config, noexec):
    logger.info("Exists - Start")
    
    logger.warn("Nothing is configured for this; I would copy files if configured")
    
    Error = False
    logger.info("Exists - End")
    return(Error)



def ignore(source, output,  component, jobcard, config, noexec):
    logger.info("Ignore - Start")
    
    logger.warn("Component: " + str(component) + "is being ignored")
    
    logger.info("Ignore - End")
    return(Error)