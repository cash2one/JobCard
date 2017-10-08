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
    
    CONVERT=config['locations']['convert']
    
    projectno = jobcard['clipinfo']['projectno']
    edgeid = jobcard['clipinfo']['edgeid']
    prime_dubya = jobcard['clipinfo']['prime_dubya']

    image=jobcard['boxcover']['src']
    title=jobcard['clipinfo']['title'] + " " + edgeid 
    star=jobcard['clipinfo']['star'] 
    supporting = jobcard['clipinfo']['supporting']
    keywords = jobcard['clipinfo']['shorttitle']
    title_size=config['boxcover']['title_size']
    star_size= config['boxcover']['star_size']
    support_size= config['boxcover']['support_size']
    keyword_size= config['boxcover']['keyword_size']
    edgeid_size= config['boxcover']['partno_size']
    FONT = config['boxcover']['font']
    width = config['boxcover']['box_width']
    height = config['boxcover']['box_height']
    alignment= jobcard['boxcover']['alignment']
    color= config['boxcover']['font_color']
    Error = False

    
    destination = output + "/" + projectno + "/" +  prime_dubya +"/" + edgeid + "/" + jobcard[component]['out_dir']
    sourceimg = source + "/" + jobcard[component]['src']
    image = edgeid + "_cover.jpg"
    
    if not os.path.isdir(destination) and not noexec:
        os.makedirs(destination,0777)
        logger.info("Creating Directory: " + destination)
      

    logger.info( "Title:" + str(title) + " : size " + str(title_size))
    logger.info( "Star:" +  str(star) + " : size " + str(star_size))
    logger.info( "Supporting:" +  str(supporting) + " : size " + str(support_size))
    logger.info( "Keywords:" +  str(keywords) + " : size " + str(keyword_size))
    logger.info( "Part Num:" +  str(edgeid) + " : size " + str(edgeid_size))
    logger.info( "Title Alignment:" + str(alignment))
    logger.info( "Text Color:" + str(color))
    logger.info( "Font:" + str(FONT))
    logger.info( "Cover Image:" + sourceimg)
    
    
    
    if alignment == 'left':
        title = " " + title
        star = " " + star
        supporting = "  " + supporting
        gravity='Northwest'
    if alignment == 'center':
        gravity = 'North'
    if alignment == 'right':
        gravity='NorthEast'       
        title = title + " "
        star = star + " "
        supporting =  supporting + "  "
        
        
    RESIZE_CMD = CONVERT + " -size 3724x5616 canvas:black '" + str(sourceimg) + "' -gravity center -resize " + str(width) +"x" + str(height) + "  -flatten '" + destination +  "/" + str(edgeid)  + config['boxcover']['suffix'] + "_source" + ".jpg'"
    resizeimg =   destination +  "/" + str(edgeid)  + config['boxcover']['suffix'] + "_source" + ".jpg"
    logger.warning("Resize Image Command\n\t" + RESIZE_CMD)
    
        #Make keywords split by line
        
    keywords_f = keywords.replace(" ","\\n")
    title_f = title.replace("'","\\'")
        
    CMD = CONVERT + " -verbose -size " + str(config['boxcover']['box_width']) + "x" + str(config['boxcover']['box_height']) + " -font " + str(FONT) + " -pointsize " + str(title_size)
    CMD = CMD + " -fill " + str(color) + " \( \( -gravity " + gravity + " -background transparent -pointsize  " + str(title_size) + "  label:\"" + title_f +"\"" + " -pointsize " + str(star_size)
    CMD = CMD + " -annotate +0+250 '" + str(star) + "'" + " -pointsize " + str(support_size) + " -annotate +0+450 '" +  str(supporting) + "' -splice 0x16 \)"
    CMD = CMD + " \( +clone -background black -shadow 20x-9+0+0 \) -background transparent +swap -layers merge +repage \)  \( \( -gravity West -background transparent -pointsize " 
    CMD = CMD + str(keyword_size) + " label:'" + str(keywords_f) + "'  -splice 50x0 \)  \( +clone -background black -shadow 20x-9+0+0 \) -background transparent +swap -layers merge +repage \) \( -gravity SouthWest "+ " -pointsize " +str(edgeid_size) + " -background transparent label:"
    CMD = CMD + str(edgeid) +" -splice 100x0 \) " + "  \( \( -gravity SouthEast -background transparent label:'EDGE   \n' -splice 0x18  -pointsize 50  -annotate +50+192 '  _____________________   ' -splice 0x18 -pointsize 100 -annotate +50+120 'interactive  '   \) "
    CMD = CMD + " \( +clone -background black -shadow 60x18+0+0 \) -background transparent +swap -layers merge +repage \) \(  -label 'image' -background transparent -mosaic label:blank "
    CMD = CMD + "'" + str(resizeimg) + "' \) \(  -clone 0--1 -mosaic  \) -trim -reverse '" + str(destination) + "/" + str(edgeid) + str(config['boxcover']['suffix']) + ".psd'; " + CONVERT + " -flatten '" + destination + "/" + edgeid + config['boxcover']['suffix'] + ".psd' '" + destination + "/" +edgeid + config['boxcover']['suffix'] +".jpg'"
    
     
    
    logger.warning("Box Cover Command\n\t" + CMD)
    
    if not noexec:
        result = subprocess.Popen( RESIZE_CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
        
        stdoutdata, stderrdata = result.communicate()
        status = result.returncode 
        if status == 0:
            logger.info("\t\t Resize returned Status: " + str(status))
        else:
            logger.warning("\t\t Resize failed with Status:"+ str(status))
            Error = True 
            
            
        result = subprocess.Popen( CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
        stdoutdata, stderrdata = result.communicate()
        status = result.returncode 
        if status == 0:
            logger.info("\t\t Make Box Cover returned Status: " + str(status))
        else:
            logger.warning("\t\t Make Box Cover failed with Status:"+ str(status))
            Error = True 
            
    
    logger.info("Produce - End")
    return(Error)


def exists(source, output,  component, jobcard, config, noexec):
    logger.info("Exists - Start")
    projectno = jobcard['clipinfo']['projectno']
    edgeid = jobcard['clipinfo']['edgeid']
    prime_dubya = jobcard['clipinfo']['prime_dubya']

    sourceimg = source + "/" + jobcard[component]['src']
    image = edgeid + str(config['boxcover']['suffix']) +".jpg"
    
    destination = output + "/" + projectno + "/" +  prime_dubya +"/" + edgeid + "/" + jobcard[component]['out_dir']
    
    if not os.path.isdir(destination) and not noexec:
        os.makedirs(destination,0777)
        logger.info("Creating Directory: " + destination)
        
        
    logger.info("\tCopying Box cover:" + sourceimg + " to " + destination)
    
    if not os.path.isfile(destination + "/" + image):
        if not noexec:
            shutil.copy(sourceimg, destination + "/" + image)
            logger.info("File Copied: " + image)
    else:
        logger.warning("File Already exists, not overwritten")    
    
    
    logger.info("Exists - End")
    return(Error)



def ignore(source, output,  component, jobcard, config, noexec):
    logger.info("Ignore - Start")
    
    
    
    logger.info("Ignore - End")
    return(Error)