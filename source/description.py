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
    
    name = jobcard['clipinfo']['edgeid'] + jobcard[component]['suffix']
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
    template = template = jobcard[component]['src']
    TEXT = ''
    

    destination = output + "/" + projectno + "/" +  prime_dubya +"/" + edgeid + "/" + jobcard[component]['out_dir']
    
    logger.info("\tFile will be created @ " + destination)
    logger.info("\tUsing Template: "+ template)
    
    
    if not os.path.isdir(destination) and not noexec:
        os.makedirs(destination,0777)
           
    desc_template = open(template,"r")
    if not noexec:
        desc_text = open(destination + "/" + name, "w")
    
    for line in desc_template:
        
        formatted_line = word_wrap(line, width=80, ind1=0, ind2=11, prefix='')
        TEXT = TEXT + formatted_line
    

    Modified = Template(TEXT).safe_substitute(STAR=star, EDGEID=edgeid, SUPPORTING=supporting,SHORTTITLE=shorttitle, KEYWORDS=keywords, PRODUCTIONDATE=productiondate, RELEASEDATE=releasedate, LICENSOR=licensor, PROJECTNO=projectno, DESCRIPTION=description, TITLE=title)
    
    if not noexec:
        desc_text.write(Modified)
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