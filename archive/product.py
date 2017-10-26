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
    
    logger.info("Produce - Module Main - Start")
    # Start Code here
    
    
    logger.info("Produce - Module Main - Start")
    
    return(Error)

def produce(source, output,  component, jobcard, config, noexec):
    logger.info("Produce - Start")
    
    Error = False
    
    # Always Needed Variables
    projectno = jobcard['clipinfo']['projectno']
    edgeid = jobcard['clipinfo']['edgeid']
    prime_dubya = jobcard['clipinfo']['prime_dubya']
    
    # Product Based Variables:
    
    
    
    
       
    myout_dir = jobcard[component]['out_dir']
    
    if not myout_dir[0] =='/':
        destination = output + "/" + projectno + "/" +  prime_dubya +"/" + edgeid + "/" + jobcard[component]['out_dir']
    else:
        destination = myout_dir    
        
    # Some error logic for suffix (it is optional)
    #
    # Set use of thumbnails and or watermarks
    # Set if we are needing Thumbnails or Watermarks
    
    try:
        make_thumbnail = jobcard[component]['thumbnail']
        thumbnail_outdir = jobcard[thumbnails]['out_dir']
        thumbnail_suffice = jobcard[thumbnails]['suffix']
    except:
        make_thumbnail = False
        
    try:
        make_watermark = jobcard[component]['watermark']
        watermark_outdir = jobcard['watermark']['out_dir']
        watermark_suffix = jobcard['watermark']['suffix']
    except:
        make_watermark = False    
     
    logger.info("Thumnails " + str(make_thumbnail))
    logger.info("Watermark Images " + str(make_watermark))
  
            
   # Assemble Parts
    for part in jobcard[component]:
        logger.info("component = " + str(part))         
        logger.info("Evaluation requirements for component " + part)
       
        if (not part == 'out_dir') and (not part == 'module') and (not part == 'account') and (not part[0:3] == 'map') and (not part == 'watermark') and (not part == 'thumbnail'):
            
            if  jobcard[part]['suffix'] == None:
                suffix = ""
            else:   
                suffix = jobcard[part]['suffix'] 
            
            if not make_watermark == True:            
                if jobcard[part]['out_dir']:
                    try:
                        src_dir = source + "/" + projectno + "/" +  prime_dubya +"/" + edgeid + "/" + jobcard[part]['name'] + "/" + jobcard[part]['out_dir']
                    except:
                        src_dir =  source + "/" + projectno + "/" +  prime_dubya +"/" + edgeid + "/" + jobcard[part]['out_dir']
                    else:
                        src_dir =  source + "/" + projectno + "/" +  prime_dubya +"/" + edgeid + "/" + jobcard[part]['name'] + "/" + jobcard[part]['out_dir']
            else:
                if jobcard[part]['out_dir']:
                    try:
                        src_dir = source + "/" + projectno + "/" +  prime_dubya +"/" + edgeid + "/" + jobcard[part]['name'] + "/" + watermark_outdir
                    except:
                        src_dir =  source + "/" + projectno + "/" +  prime_dubya +"/" + edgeid + "/" + watermark_outdir
                    else:
                        src_dir =  source + "/" + projectno + "/" +  prime_dubya +"/" + edgeid + "/" + jobcard[part]['name'] + "/" + watermark_outdir
                    
                
           
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
            
            # Create Target Suffix w/or w/o Watermark
            if make_watermark == True and str(jobcard[part]['ext']) == '.jpg' and not part == 'boxcover':
                target_files = suffix + watermark_suffix + str(jobcard[part]['ext'])
            else:
                target_files = suffix + str(jobcard[part]['ext'])
            
            logger.info("Target files = *" + target_files )
            logger.info("Source Directory = " + src_dir )
            logger.info("Destination directory = " + destination + "/" + out_dir )
           
    logger.info("Produce - End")
    return(Error)


def exists(source, output,  component, jobcard, config, noexec):
    logger.info("Exists - Start")
    
    
    
    logger.info("Exists - End")
    return(Error)



def ignore(source, output,  component, jobcard, config, noexec):
    logger.info("Ignore - Start")
    
    
    
    logger.info("Ignore - End")
    return(Error)