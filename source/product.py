'''
Created on Sep 30, 2017

@author: colin
'''

#===============================================================================
# Import 
#===============================================================================

import os,glob
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
        logger.info("Working on part :" + str(part))
        
        try:
            part_make = jobcard[component][part] if part in jobcard[component] else None
            part_account = jobcard[component]['account'] if "account" in jobcard[component] else None
                      
        except Exception as e:  
            part_make = False
        
        if (part_make == True) and (not part == 'out_dir') and (not part == 'module') and (not part == 'account') and (not part[0:3] == 'map'): 
            mappedpart = "map_" + str(part)
            logger.info("Mapped Part " + mappedpart )
            try:
                part_name = jobcard[part]['name'] if "name" in jobcard[part] else None
                part_outdir = jobcard[part]['out_dir'] if "out_dir" in jobcard[part] else None
                map_part_name = jobcard[component][mappedpart] if mappedpart in jobcard[component] else None
                p_suffix =  jobcard[part]['suffix'] if "suffix" in jobcard[part] else "" 
                part_ext = jobcard[part]['ext'] if "ext" in jobcard[part] else None
                if part.startswith("video"):
                    logger.info("Creating suffix for videos")
                    part_height = jobcard[part]['size_height'] if "size_height" in jobcard[part] else 1900
                    part_width = jobcard[part]['size_width'] if "size_width" in jobcard[part] else 1000
                    part_kbps = jobcard[part]['size_kbps'] if "size_kbps" in jobcard[part] else 1200
                    logger.info("Video parameters are: " + str(part_height) +"x" + str(part_width) + "x" + str(part_kbps) )
                    part_suffix = "_" + str(part_width) +"x" + str(part_height) + "x" + str(part_kbps) + str(p_suffix)       
                else:
                    part_suffix =  p_suffix    
                      
            except Exception as e:  
                logger.warning("Not all variables set properly; exception " + str(e))   
                logger.warn("No Name or Outdir found")
                part_name = None
                part_outdir = None
            
            #setup final source in complex situations
            if not part_name == None and not part_outdir == None:
                src_final = src + "/" + str(part_name) + "/" + str(part_outdir)
            elif not part_name == None and part_outdir == None:
                src_final = src + "/" + str(part_name)
            elif part_name == None and not part_outdir == None:
                src_final = src + "/" + str(part_outdir)     
            else:
                src_final = src  
            
            if not part_account == None:
                accountdestination = "/" + part_account
                
            # Create part final destination and accomondate for mapped and not mapped
            if not map_part_name == None: 
                logger.info("Part is mapped to new directory")
                partfinaldestination = finaldestination + accountdestination + "/" + str(map_part_name)
            else:           
                logger.info("Use part name and/or outdir " + str(part_name) +" : " +str(part_outdir))
                if (not part_name == None) and (not part_outdir == None):
                    partfinaldestination = finaldestination + accountdestination + "/" + str(part_name) + "/" + str(part_outdir)
                elif not part_name == None and part_outdir == None:
                    partfinaldestination = finaldestination + accountdestination +  "/" + str(part_name)
                elif part_name == None and not part_outdir == None:
                    partfinaldestination = finaldestination + accountdestination + "/" + str(part_outdir)     
                else:
                    partfinaldestination = finaldestination
        
            logger.info("component = " + str(part) + " : " + str(part_make))
            logger.info("Evaluation requirements for component " + part)
            logger.info("Source Directory = " + src_final )
            logger.info("Source Volume = " + source )
            logger.info("Part Name: " + str(part_name) + " Part Outdir: " + str(part_outdir))
            logger.info("Mapped Part Name: " + str(map_part_name))
            logger.info("Part Suffix: " + str(part_suffix))
            logger.info("Part ext: " + str(part_ext))
            logger.info("Output directory = " + destination )
            logger.info("Destination directory = " + finaldestination)
            logger.info("Part directory = " + partfinaldestination)
            logger.info("Account name = " + str(part_account))
            
            # Create Directories if needed
            if not os.path.isdir(partfinaldestination) and not noexec:
                os.makedirs(partfinaldestination,0777)
                logger.info("Creating Directory [Final Destination]:\t" + partfinaldestination)
            else:
                logger.info("Creating Directory:[Final Destination]:\t" + partfinaldestination)  
            
            if not noexec:
                files =  src_final + "/" + edgeid +"*" + str( part_suffix ) +  str(part_ext)
                filelist = glob.glob(files)
                for myfile in filelist:
                    logger.info("Copy file: " + myfile + " to " + str(partfinaldestination) ) 
                    copy_result = shutil.copy(myfile , str(partfinaldestination))
                    
            else:
                logger.info("Copy: " + src_final + "/" + edgeid +"*" +str( part_suffix ) +   str(part_ext) + " to " + str(partfinaldestination) )
                logger.info("Command:\n\tcp " + src_final + "/" + edgeid +"*" +str( part_suffix ) +   str(part_ext) +" " + str(partfinaldestination))
    
    # Create Product Specific calls here
    # Allowed (clips4sale, ebay, flickrocket)
    
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