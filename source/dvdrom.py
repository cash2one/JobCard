'''
Created on Sep 30, 2017

@author: colin
'''

#===============================================================================
# Import 
#===============================================================================

import os
from string import Template
import shutil
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
    MKISOFS = config['locations']['mkisofs']
    DVDAUTHOR = config['locations']['dvdauthor']
    
    logger.debug("CURL = " + CURL)
    logger.debug("CONVERT = " + CONVERT)
    logger.debug("FFMPEG = " + FFMPEG)
    logger.debug("FFPROBE = " + FFPROBE)
    logger.debug("MOGRIFY = " + MOGRIFY)
    logger.debug("FONT = " + FONT)
    logger.debug("MKISOFS = " + MKISOFS)
    logger.debug("DVDAUTHOR = " + DVDAUTHOR)
    
    logger.info("Produce - Module Main - Start")
    # Start Code here
    
    
    logger.info("Produce - Module Main - Start")
    
    return(Error)

def produce(source, output,  component, jobcard, config, noexec):
    logger.info("Produce - Start")
    
    CURL=config['locations']['curl']
    CONVERT=config['locations']['convert']
    FFMPEG=config['locations']['ffmpeg']
    FFPROBE=config['locations']['ffprobe']
    MOGRIFY=config['locations']['mogrify']
    FONT=config['boxcover']['font']
    MKISOFS = config['locations']['mkisofs']
    DVDAUTHOR = config['locations']['dvdauthor']
    
    logger.debug("CURL = " + CURL)
    logger.debug("CONVERT = " + CONVERT)
    logger.debug("FFMPEG = " + FFMPEG)
    logger.debug("FFPROBE = " + FFPROBE)
    logger.debug("MOGRIFY = " + MOGRIFY)
    logger.debug("FONT = " + FONT)
    logger.debug("MKISOFS = " + MKISOFS)
    logger.debug("DVDAUTHOR = " + DVDAUTHOR)
    
    
    
    projectno = jobcard['clipinfo']['projectno']
    edgeid = jobcard['clipinfo']['edgeid']
    prime_dubya = jobcard['clipinfo']['prime_dubya']
    destination = output + "/" + projectno + "/" +  prime_dubya +"/" + edgeid + "/" + jobcard[component]['out_dir']
    

    if not os.path.isdir(destination ) and not noexec:
        os.makedirs(destination,0777)
        logger.info("Creating Directory: " + destination)
        
    logger.info("Writing files to " + destination)
    
        
    logger.info("Creating Product Files for ->" + component)
    for part in jobcard[component]:
        logger.warning("component = " + part)
        if (not part == 'out_dir') and (not part == 'module') :
            logger.info("Evaluation requirements for component " + part)
            logger.info("Target files = " + jobcard[part]['suffix'] )
            if jobcard[part]['out_dir']:
                src_dir = str(jobcard[part]['out_dir'])
            else:
                src_dir = ''    
            file_dir = source + "/" + projectno + "/" +  prime_dubya +"/" + edgeid + "/" + src_dir
            out_dir =  jobcard[part]['out_dir']
            suffix = str(jobcard[part]['suffix'] )
            for filename in os.listdir(file_dir):
                if filename.endswith(suffix) and not noexec:
                    logger.warning("copy filename=" + filename)
                    if not os.path.isdir(destination + "/" + out_dir ) and not noexec:
                        os.makedirs(destination + "/" + out_dir ,0777)
                    shutil.copy(file_dir + "/" + filename, destination + "/" + out_dir) 
                elif  filename.endswith(suffix):
                    logger.warning("copy filename=" + filename)
                    logger.warning("to " + destination + "/" + out_dir) 
        else:
            logger.critical("Ignoring component" + part) 
                     
                
            
            
        
    logger.info("Produce - End")
    return(Error)


def exists(source, output,  component, jobcard, config, noexec):
    logger.info("Exists - Start")
    
    logger.error("Not Valid")
    
    logger.info("Exists - End")
    return(Error)



def ignore(source, output,  component, jobcard, config, noexec):
    logger.info("Ignore - Start")
    
    
    
    logger.info("Ignore - End")
    return(Error)