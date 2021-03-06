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
import getvideosize

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

#===============================================================================
# Module Functions
#===============================================================================

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
    
    name = jobcard['clipinfo']['edgeid'] + jobcard[component]['suffix'] + jobcard[component]['ext']
    projectno = jobcard['clipinfo']['projectno']
    edgeid = jobcard['clipinfo']['edgeid']
    prime_dubya = jobcard['clipinfo']['prime_dubya']
    star = jobcard['clipinfo']['star']
    supporting = jobcard['clipinfo']['supporting']
    shorttitle = jobcard['clipinfo']['shorttitle']
    title = jobcard['clipinfo']['title']
    description = jobcard['clipinfo']['description']
    keywords = jobcard['clipinfo']['keywords']
    productiondate = jobcard['clipinfo']['productiondate']
    releasedate = jobcard['clipinfo']['releasedate']
    licensor = jobcard['clipinfo']['licensor']
    birthdate = jobcard['clipinfo']['birthdate']
    age = jobcard['clipinfo']['age']
    height = jobcard['clipinfo']['height']
    weight = jobcard['clipinfo']['weight']
    measurements = jobcard['clipinfo']['measurements']
    hair = jobcard['clipinfo']['hair']
    eyes = jobcard['clipinfo']['eyes']
    skin = jobcard['clipinfo']['skin']
    birthplace = jobcard['clipinfo']['birthplace']
    
    # Video Information
    vheight = jobcard['video1']['size_height']
    vwidth = jobcard['video1']['size_width']
    vkbps = jobcard['video1']['size_kbps']
    duration = jobcard['video']['duration']
    
    # Photo Set Information
    photoset1_count  = jobcard['photoset1']['count']
    photoset1_width = jobcard['photoset1']['set_width']
    photoset1_height = jobcard['photoset1']['set_height']
    
    
    test_source = str(jobcard[component]['src'])
    if test_source[0] != "/":                       
        logger.debug("Relative Path")    
        template = source + "/" + jobcard[component]['src']
    else:
        logger.debug("Absolute Path")
        template = jobcard[component]['src']
    
   
    TEXT = ''
    Error = False
    

    

    
    destination = output + "/" + projectno + "/" +  prime_dubya +"/" + edgeid + "/" + jobcard[component]['out_dir']
    
    logger.info("\tFile will be created @ " + destination)
    logger.info("\tUsing Template: "+ template)
    
    
    if not os.path.isdir(destination) and not noexec:
        os.makedirs(destination,0777)
           
    desc_template = open(template,"r")
    if not noexec:
        desc_text = open(destination + "/" + name, "w")
    
    for line in desc_template:
        
        replaced_line = Template(line).safe_substitute(STAR=star, EDGEID=edgeid, SUPPORTING=supporting,SHORTTITLE=shorttitle, KEYWORDS=keywords, PRODUCTIONDATE=productiondate, RELEASEDATE=releasedate, LICENSOR=licensor, PROJECTNO=projectno, DESCRIPTION=description, TITLE=title, PRIME_DUBYA=prime_dubya, BIRTHDATE=birthdate, AGE=age, HEIGHT=height, WEIGHT=weight, MEASUREMENTS=measurements, HAIR=hair, EYES=eyes, SKIN=skin, BIRTHPLACE=birthplace, DURATION=duration, VHEIGHT=vheight, VWIDTH=vwidth, VKBPS=vkbps, PHOTOSET1_COUNT=photoset1_count, PHOTOSET1_WIDTH=photoset1_width, PHOTOSET1_HEIGHT=photoset1_height)
        formatted_line = word_wrap(replaced_line, width=120, ind1=0, ind2=11, prefix='')
        TEXT = TEXT + formatted_line
    

    
    if not noexec:
        desc_text.write(TEXT)
        desc_text.close()
    desc_template.close()
    
    logger.info("Produce - End")
    return(Error)


def exists(source, output,  component, jobcard, config, noexec):
    logger.info("Produce - Start")
    logger.error("Not Valid")
    Error = True
    
    
    logger.info("Produce - End")
    return(Error)



def ignore(source, output,  component, jobcard, config, noexec):
    logger.info("Produce - Start")
    
    
    
    logger.info("Produce - End")
    return(Error)