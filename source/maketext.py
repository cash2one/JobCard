#-*- coding: utf-8 -*-
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

# Additional Libraries
from string import Template

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

def word_wrap(string, width=80, ind1=0, ind2=0, prefix=''):
    """ word wrapping function.
        string: the string to wrap
        width: the column number to wrap at
        prefix: prefix each line with this string (goes before any indentation)
        ind1: number of characters to indent the first line
        ind2: number of characters to indent the rest of the lines
    """
    string = prefix + ind1 * " " + string
    newstring = ""
    while len(string) > width:
        # find position of nearest whitespace char to the left of "width"
        marker = width - 1
        while not string[marker].isspace():
            marker = marker - 1

        # remove line from original string and add it to the new string
        newline = string[0:marker] + "\n"
        newstring = newstring + newline
        string = prefix + ind2 * " " + string[marker + 1:]

    return newstring + string

def produce(source, output,  component, jobcard, config, noexec):
    TEXT = ""
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
        
        # Get Clip Information 
        clip_prime_dubya = jobcard['clipinfo']['prime_dubya']
        clip_shorttitle = jobcard['clipinfo']['shorttitle']
        clip_title = jobcard['clipinfo']['title']
        clip_description = jobcard['clipinfo']['description']
        clip_keywords = jobcard['clipinfo']['keywords']
        clip_productiondate = jobcard['clipinfo']['productiondate']
        clip_releasedate = jobcard['clipinfo']['releasedate']
        clip_licensor = jobcard['clipinfo']['licensor']
        clip_comment = jobcard['clipinfo']['comment']
        clip_star_name = jobcard['clipinfo']['star']['name'] if "name" in jobcard['clipinfo']['star'] else ''
        clip_star_birthdate = jobcard['clipinfo']['star']['birthdate'] if "birthdate" in jobcard['clipinfo']['star'] else None
        clip_star_age = jobcard['clipinfo']['star']['age'] if "age" in jobcard['clipinfo']['star'] else None
        clip_star_height = jobcard['clipinfo']['star']['height'] if "height" in jobcard['clipinfo']['star'] else None
        clip_star_weight = jobcard['clipinfo']['star']['weight'] if "weight" in jobcard['clipinfo']['star'] else None
        clip_star_measurements = jobcard['clipinfo']['star']['measurements'] if "measurements" in jobcard['clipinfo']['star'] else None
        clip_star_hair = jobcard['clipinfo']['star']['hair'] if "hair" in jobcard['clipinfo']['star'] else None
        clip_star_eyes = jobcard['clipinfo']['star']['eyes'] if "eyes" in jobcard['clipinfo']['star'] else None
        clip_star_skin = jobcard['clipinfo']['star']['skin'] if "skin" in jobcard['clipinfo']['star'] else None
        clip_star_birthplace = jobcard['clipinfo']['star']['birthplace'] if "birthplace" in jobcard['clipinfo']['star'] else None            
        clip_star2 = True if "star2" in jobcard['clipinfo'] else False
        if clip_star2:
            logger.info("Loading Star 2")
            clip_star2_name = jobcard['clipinfo']['star2']['name'] if "name" in jobcard['clipinfo']['star2'] else ''
            clip_star2_birthdate = jobcard['clipinfo']['star2']['birthdate'] if "birthdate" in jobcard['clipinfo']['star2'] else None
            clip_star2_age = jobcard['clipinfo']['star2']['age'] if "age" in jobcard['clipinfo']['star2'] else None
            clip_star2_height = jobcard['clipinfo']['star2']['height'] if "height" in jobcard['clipinfo']['star2'] else None
            clip_star2_weight = jobcard['clipinfo']['star2']['weight'] if "weight" in jobcard['clipinfo']['star2'] else None
            clip_star2_measurements = jobcard['clipinfo']['star2']['measurements'] if "measurements" in jobcard['clipinfo']['star2'] else None
            clip_star2_hair = jobcard['clipinfo']['star2']['hair'] if "hair" in jobcard['clipinfo']['star2'] else None
            clip_star2_eyes = jobcard['clipinfo']['star2']['eyes'] if "eyes" in jobcard['clipinfo']['star2'] else None
            clip_star2_skin = jobcard['clipinfo']['star2']['skin'] if "skin" in jobcard['clipinfo']['star2'] else None
            clip_star2_birthplace = jobcard['clipinfo']['star2']['birthplace'] if "birthplace" in jobcard['clipinfo']['star2'] else None
        clip_supporting_name = jobcard['clipinfo']['supporting']['name'] if "name" in jobcard['clipinfo']['supporting'] else ''
        clip_supporting_birthdate = jobcard['clipinfo']['supporting']['birthdate'] if "birthdate" in jobcard['clipinfo']['supporting'] else None
        clip_supporting_age = jobcard['clipinfo']['supporting']['age'] if "age" in jobcard['clipinfo']['supporting'] else None
        clip_supporting_height = jobcard['clipinfo']['supporting']['height'] if "height" in jobcard['clipinfo']['supporting'] else None
        clip_supporting_weight = jobcard['clipinfo']['supporting']['weight'] if "weight" in jobcard['clipinfo']['supporting'] else None
        clip_supporting_measurements = jobcard['clipinfo']['supporting']['measurements'] if "measurements" in jobcard['clipinfo']['supporting'] else None
        clip_supporting_hair = jobcard['clipinfo']['supporting']['hair'] if "hair" in jobcard['clipinfo']['supporting'] else None
        clip_supporting_eyes = jobcard['clipinfo']['supporting']['eyes'] if "eyes" in jobcard['clipinfo']['supporting'] else None
        clip_supporting_skin = jobcard['clipinfo']['supporting']['skin'] if "skin" in jobcard['clipinfo']['supporting'] else None
        clip_supporting_birthplace = jobcard['clipinfo']['supporting']['birthplace'] if "birthplace" in jobcard['clipinfo']['supporting'] else None      
        
    except Exception as e:  
        logger.warning("Not all variables set properly; exception " + str(e))   
    
    
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
    
    # Add Some log lines for clip info
    logger.info("\tClip Short Title: " + str(clip_shorttitle))
    logger.info("\tClip Star: " + str(clip_star_name))  
    if clip_star2:
        logger.info("\tClip Star2: " + str(clip_star2_name))  
    logger.info("\tClip Supporting: " + str(clip_supporting_name))           
    # Create Directories if needed
    if not os.path.isdir(finaldestination) and not noexec:
        os.makedirs(finaldestination,0777)
        logger.info("Creating Directory: " + finaldestination)
    else:
        logger.info("Creating Directory: " + finaldestination)   

    logger.info("\tFile will be created @ " + destination)
    logger.info("\tUsing Template: "+ item_source)
    
    # Now let's do actual work
    
    desc_template = open(item_source,"r")
    if not noexec:
        desc_text = open(finaldestination + "/" + edgeid + item_suffix + item_ext, "w")
    
    for line in desc_template:
        if clip_star2:      
            replaced_line = Template(line).safe_substitute(EDGEID=edgeid, SUPPORTING=clip_supporting_name,SHORTTITLE=clip_shorttitle, KEYWORDS=clip_keywords, PRODUCTIONDATE=clip_productiondate, RELEASEDATE=clip_releasedate, LICENSOR=clip_licensor, PROJECTNO=projectno, DESCRIPTION=clip_description, TITLE=clip_title, PRIME_DUBYA=clip_prime_dubya, STAR=clip_star_name, STAR_BIRTHDATE=clip_star_birthdate, STAR_AGE=clip_star_age, STAR_HEIGHT=clip_star_height, STAR_WEIGHT=clip_star_weight, STAR_MEASUREMENTS=clip_star_measurements, STAR_HAIR=clip_star_hair, STAR_EYES=clip_star_eyes, STAR_SKIN=clip_star_skin, STAR_BIRTHPLACE=clip_star_birthplace, STAR2=clip_star2_name, STAR2_BIRTHDATE=clip_star2_birthdate, STAR2_AGE=clip_star2_age, STAR2_HEIGHT=clip_star2_height, STAR2_WEIGHT=clip_star2_weight, STAR2_MEASUREMENTS=clip_star2_measurements, STAR2_HAIR=clip_star2_hair, STAR2_EYES=clip_star2_eyes, STAR2_SKIN=clip_star2_skin, STAR2_BIRTHPLACE=clip_star2_birthplace)
        else:
            replaced_line = Template(line).safe_substitute(EDGEID=edgeid, SUPPORTING=clip_supporting_name,SHORTTITLE=clip_shorttitle, KEYWORDS=clip_keywords, PRODUCTIONDATE=clip_productiondate, RELEASEDATE=clip_releasedate, LICENSOR=clip_licensor, PROJECTNO=projectno, DESCRIPTION=clip_description, TITLE=clip_title, PRIME_DUBYA=clip_prime_dubya, STAR=clip_star_name, STAR_BIRTHDATE=clip_star_birthdate, STAR_AGE=clip_star_age, STAR_HEIGHT=clip_star_height, STAR_WEIGHT=clip_star_weight, STAR_MEASUREMENTS=clip_star_measurements, STAR_HAIR=clip_star_hair, STAR_EYES=clip_star_eyes, STAR_SKIN=clip_star_skin, STAR_BIRTHPLACE=clip_star_birthplace, )

        formatted_line = word_wrap(replaced_line, width=120, ind1=0, ind2=11, prefix='')
        TEXT = TEXT + formatted_line

    if not noexec:
        desc_text.write(TEXT)
        desc_text.close()
    desc_template.close()

    
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