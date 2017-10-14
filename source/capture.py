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
import subprocess
import getvideosize
from os.path import basename

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
    
        

    FFMPEG=config['locations']['ffmpeg']
    MOGRIFY=config['locations']['mogrify']
    CONVERT=config['locations']['convert']

    
    MESSAGE = ''
    ERROR = ''
    NEWLINE = '\n'
    WORK = ''
    Error = False
    
    # Define Parameters
    video =  source + "/" +jobcard['video']['src']
    seconds = jobcard['capture']['frame_every']
    projectno = jobcard['clipinfo']['projectno']
    edgeid = jobcard['clipinfo']['edgeid']
    prime_dubya = jobcard['clipinfo']['prime_dubya']
    videoName = os.path.basename(video)
    pathName = os.path.dirname( source + "/" + video)
    star = jobcard['clipinfo']['star']
    
    
    set_dir = jobcard[component]['out_dir']
    if jobcard[component]['suffix'] == None:
        set_suffix = "__"
    else:    
        set_suffix =  jobcard[component]['suffix']
    set_ext =  jobcard[component]['ext']
    set_name = jobcard[component]['name']
    
    
    
    thumb_size = jobcard['thumbnails']['size']
    thumb_dir = jobcard['thumbnails']['out_dir']
    thumb_ext = jobcard['thumbnails']['ext']
    thumb_suffix = jobcard['thumbnails']['suffix']
    
    
    watermark_dir = jobcard['watermark']['out_dir']
    watermark_size = jobcard['watermark']['fontsize']
    watermark_location = jobcard['watermark']['location']
    watermark_template = jobcard['watermark']['template']
    watermark_ext = jobcard['watermark']['ext']
    watermark_suffix = jobcard['watermark']['suffix']
    watermark_color = jobcard['watermark']['color']
    
    
    watermark_text = Template(watermark_template).safe_substitute(STAR=star)
    WorkMatrix = {}
    
    font = config['boxcover']['font']
    
    if jobcard['component']['thumbnails'] == 'produce' or jobcard['component']['thumbnails'] == 'validate':
        make_thumbnail = True
        logger.info("\tMaking Thumbnails")
    else:   
        make_thumbnail = False
        
    if jobcard['component']['watermark'] == 'produce' or jobcard['component']['thumbnails'] == 'validate':
        make_watermark = True
        logger.info("\tMaking Watermarks")
    else:   
        make_watermark = False          
   
    
    # Get video Size 
    Error, SizeOfVideo, Duration, Bitrate  = getvideosize.produce(source, output, component, jobcard, config, noexec)
    
    # We need the size to name the capture directory
    
    destination = output + "/" + projectno + "/" +  prime_dubya +"/" + edgeid 
    
    set_src = destination + "/" + jobcard[component]['name'] + "/" + jobcard[component]['out_dir']
    
    
       # Create Directories if needed
    if not os.path.isdir(destination + "/" + set_name + "/" + set_dir) and not noexec:
        os.makedirs(destination + "/" + set_name + "/" + set_dir,0777)
        logger.info("Creating Directory: " + destination + "/" + set_name + "/" + set_dir)
    else:
        logger.info("Creating Directory: " + destination + "/" + set_name + "/" + set_dir)   
    
    if not os.path.isdir(destination + "/" + set_name  +"/" + thumb_dir) and not noexec and make_thumbnail:
        os.makedirs(destination + "/" + set_name + "/" +thumb_dir,0777)
        logger.info("Creating Thumbnail Directory: " + destination + "/" + set_name + "/" + thumb_dir)
    else:
        logger.info("Creating Thumbnail Directory: " + destination + "/" + set_name + "/" + thumb_dir)    
        
    if not os.path.isdir(destination + "/" + set_name + "/" + watermark_dir) and not noexec and make_watermark:
        os.makedirs(destination + "/"  + set_name + "/" + watermark_dir,0777)
        logger.info("Creating Watermark Directory: " + destination + "/" + set_name + "/" + watermark_dir) 
    else:
        logger.info("Creating Watermark Directory: " + destination + "/" + set_name + "/" + watermark_dir)
                      
        
        
        
    logger.info("Make Stills for Video: " + videoName )
    logger.info("Source Dir:"  + pathName )
    logger.info("Put Stills in Destination:\n  " )
    logger.info("\t\t"+destination)
    

    
    
    
           
   
    CMD = FFMPEG + " -c:v h264_vda -i '"  + video + "' -thread_type slice -hide_banner -vf fps=1/" + str(seconds) + "  -c:v mjpeg '" + destination + "/" + jobcard[component]['name'] +"/" + jobcard[component]['out_dir'] + "/" + edgeid  + "_capture_%03d.jpg'" 
    
    logger.info("Making stills from video:" + video + " Size:" + str(SizeOfVideo) + " Duration:" + str(Duration) + " seconds @ bitrate:" + str(Bitrate) )
    logger.warning("StillCommand:\n  " + CMD )
    
    if noexec:
        logger.info( "No Execute" )
        result=subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        logger.warning("Running Command" )  
        
        result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdoutdata, stderrdata = result.communicate()
        status = result.returncode 
        if status == 0:
            logger.info("\t\t Capture returned Status: " + str(status))
        else:
            logger.warning("\t\t Capture failed with Status:"+ str(status))
            Error = True 
    
     
    logger.info( "Capture on " + videoName + " Completed" )
        
 
 
    #Alternate Method for thumbnails & Larger Images
    
    count = 0
    work = 0
    
    # Start with image 0
    for filename in os.listdir(set_src):
        if filename.endswith(".tif") or filename.endswith(".jpg"):
            myfilename = basename(filename)
            myfile = os.path.splitext(myfilename)[0]
            
            if make_thumbnail:
                logger.info("Making Thumbnail for " + filename)
                CMD = CONVERT + " " + set_src + "/" + filename +" -thumbnail " + str(thumb_size) + " '" + destination +  "/" + jobcard[component]['name'] + "/" + thumb_dir + "/" + myfile +  thumb_suffix + thumb_ext +"'"                  
                logger.warning ( "\tThumbnailCMD\n  " + CMD  )
                if not noexec:    
                    WorkMatrix[work] = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                work = work + 1
                
            if make_watermark:
                logger.info("Making Watermark for " + filename )
                logger.info("Name is " + myfile)
                CMD = CONVERT +" '" + set_src + "/" + filename + "'" + " -background none -font " + str(font) + " -fill " + watermark_color +" -gravity " + watermark_location + " -pointsize " + str(watermark_size) +" -annotate 0 '" + watermark_text + "'" + " -flatten '" + destination + "/" + jobcard[component]['name'] +"/" + watermark_dir + "/" + myfile +  watermark_suffix + watermark_ext +"'"           
                
                logger.warning ( "\tWatermarkCMD\n  " + CMD  )
                if not noexec:    
                    WorkMatrix[work] = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                work = work + 1
        count = count + 1
    # Check if all of the images have finished processing
    if not noexec:
        # Wait for the last convert to complete. 
        for mywork in range(0,work):
            logger.info( "\tChecking on Photo # " + str(mywork) + " to complete" )
            stdoutdata, stderrdata = WorkMatrix[mywork].communicate()
            status = WorkMatrix[mywork].returncode 
            if status == 0:
                logger.info(  "\tPhoto conversion returned Status: " + str(status))
            else:
                logger.warning("\tPhoto conversion failed with status code "+ str(status))
                Error = True
    else:
        logger.info("No run")
        logger.info("Check on Work to see if it finished")
        
        
        
 
    return(Error)


def exists(source, output,  component, jobcard, config, noexec):
    logger.info("Exists - Start")
    
    logger.warning("Not Valid")
    
    logger.info("Exists - End")
    return(Error)



def ignore(source, output,  component, jobcard, config, noexec):
    logger.info("Ignore - Start")
    
    
    
    logger.info("Ignore - End")
    return(Error)