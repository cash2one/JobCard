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
import subprocess
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
    
    Error = False
    
    projectno = jobcard['clipinfo']['projectno']
    edgeid = jobcard['clipinfo']['edgeid']
    prime_dubya = jobcard['clipinfo']['prime_dubya']
    
    myout_dir = jobcard[component]['out_dir']
    if not myout_dir[0] =='/':
        destination = output + "/" + projectno + "/" +  prime_dubya +"/" + edgeid + "/" + jobcard[component]['out_dir']
    else:
        destination = myout_dir

    if not os.path.isdir(destination ) and not noexec:
        os.makedirs(destination,0777)
        logger.info("Creating Directory: " + destination)
        
    logger.info("Writing files to " + destination)
    
        
    logger.info("Creating Product Files for ->" + component)
    for part in jobcard[component]:
        logger.info("component = " + part)
        
        # destination = product out_dir
        # srcdir = component out_dir
        # mapdir = component replacement for outdir 
                
            
        
        if (not part == 'out_dir') and (not part == 'module') and (not part == 'account') and (not part[0:3] == 'map'):
            if jobcard[part]['out_dir']:
                src_dir = jobcard[part]['out_dir']
                
            else:
                src_dir =  source + "/" + projectno + "/" +  prime_dubya +"/" + edgeid + "/"
            
            file_dir = source + "/" + projectno + "/" +  prime_dubya +"/" + edgeid + "/" + src_dir
            
            if jobcard[part]['out_dir']:
                my_dir = jobcard[part]['out_dir']
            
            else:
                my_dir = source + "/" + projectno + "/" +  prime_dubya +"/" + edgeid
                
                   
            
            # See if there is a mapping for the component out_dir
            mapped = "map_" + part
            logger.info("Check for mapping of " + mapped)
            logger.info("In component " + component)
            
            try:
                test_value = jobcard[component][mapped]
                logger.info("Key Exists [" + str(jobcard[component][mapped])+"]")
                out_dir = jobcard[component][mapped]
            except KeyError:
                # Key is not present
                logger.warning("Key is not set")
                out_dir = my_dir 
                
           
            logger.info("Evaluation requirements for component " + part)
            logger.info("Target files = " + jobcard[part]['suffix'] )
            logger.info("Source Directory = " + src_dir )
            logger.info("Source Volume = " + file_dir )
            logger.info("Output directory = " + out_dir )
            logger.info("Destination directory = " + destination)
            
            
            
            
            
            suffix = str(jobcard[part]['suffix'] )
            for filename in os.listdir(file_dir):
                if filename.endswith(suffix) and not noexec:
                    logger.info("copy filename=" + filename)
                    if not os.path.isdir(destination + "/" + out_dir ) and not noexec:
                        os.makedirs(destination + "/" + out_dir ,0777)
                    shutil.copy(file_dir + "/" + filename, destination + "/" + out_dir) 
                elif  filename.endswith(suffix):
                    logger.info("copy filename=" + filename)
                    logger.info("to " + destination + "/" + out_dir) 
        else:
            logger.critical("Ignoring component [" + part + "]") 
    
    if component == 'ebay' :
        logger.info("Creating DVD Image")
    
        CMD = MKISOFS + " -J -r -o " + destination + "/" + edgeid + "_ROM.iso -V " + edgeid + "_ROM -uid 500 -find " + destination
    
        logger.info("DVD Creation Command \n\t" + CMD)
    
        if not noexec:                
            result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdoutdata, stderrdata = result.communicate()
            status = result.returncode 
            if status == 0:
                logger.info("\t\t DVD Creation returned Status: " + str(status))
            else:
                logger.warning("\t\t DVD Creation failed with Status:"+ str(status))
                Error = True 
    
    else:       
        logger.info("Product specific action goes here -->" + component)
            
            
        
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