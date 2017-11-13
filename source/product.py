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
    src = source + "/" + projectno + "/" + prime_dubya + "/" + edgeid
    
    # Create Directories as needed
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
    
    
        #setup final destination in complex situations
    if not item_name == None and not item_outdir == None:
        finaldestination = destination + "/" + str(item_name) + "/" + str(item_outdir)
    elif not item_name == None and item_outdir == None:
        finaldestination = destination + "/" + str(item_name)
    elif item_name == None and not item_outdir == None:
        finaldestination = destination + "/" + str(item_outdir)     
    else:
        finaldestination = destination
     
     
    logger.info("\tDestination: " + str(destination))
    logger.info("\tFinal Destination: " + str(finaldestination))
             
    # Create Directories if needed
    if not os.path.isdir(finaldestination) and not noexec:
        os.makedirs(finaldestination,0777)
        logger.info("Creating Directory: " + finaldestination)
    else:
        logger.info("Creating Directory: " + finaldestination)   

    logger.info("Creating Product Files for ->" + component)
    for part in jobcard[component]:
        logger.info("component = " + str(part))
        if (not part == 'out_dir') and (not part == 'module') and (not part == 'account') and (not part[0:3] == 'map'):          
            #setup final source in complex situations
            if not jobcard[part]['name'] == None and not jobcard[part]['out_dir'] == None:
                src_final = src + "/" + str(item_name) + "/" + str(item_outdir)
            elif not jobcard[part]['name'] == None and jobcard[part]['out_dir'] == None:
                src_final = src + "/" + str(item_name)
            elif jobcard[part]['name'] == None and not jobcard[part]['out_dir'] == None:
                src_final = src + "/" + str(item_outdir)     
            else:
                src_final = src
   
    
            logger.info("Source Dir: " + str(src))
            logger.info("Final Src Dir: " + str(src_final))

    
    logger.info("Produce - End")
    return(Error)


def exists(source, output,  component, jobcard, config, noexec):
    logger.info("Exists - Start")
    
    
    
    logger.info("Exists - End")
    return(Error)



def ignore(source, output,  component, jobcard, config, noexec):
    logger.info("Ignore - Start")
    
    logger.warn("Component: " + str(component) + "is being ignored")
    
    logger.info("Ignore - End")
    return(Error)