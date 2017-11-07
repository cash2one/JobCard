#-*- coding: utf-8 -*-
'''
Created on Sep 30, 2017

@author: colin
'''

#===============================================================================
# Import 
#===============================================================================

import os
import shutil
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
    
    # Set Commands we will need
    CONVERT=config['locations']['convert']
    
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
        item_thumbnail = jobcard[component]['thumbnail'] if "thumbnail" in jobcard[component] else None
        item_watermark = jobcard[component]['watermark'] if "watermark" in jobcard[component] else None
        item_count = jobcard[component]['count'] if "count" in jobcard[component] else None
        item_timed = jobcard[component]['timed'] if "timed" in jobcard[component] else None
        item_size = jobcard[component]['size'] if "size" in jobcard[component] else None
 
        
        # setup clip information
        title = jobcard['clipinfo']['title'] + " " + edgeid  if "title" in jobcard['clipinfo'] else " "
        star = jobcard['clipinfo']['star']['name']  if "name" in jobcard['clipinfo']['star'] else " "
        star2 = jobcard['clipinfo']['star2']['name']  if "name" in jobcard['clipinfo']['star2'] else ''
        supporting = jobcard['clipinfo']['supporting']['name'] if "name" in jobcard['clipinfo']['supporting'] else " "
        shorttitle = jobcard['clipinfo']['shorttitle'] if "shorttitle" in jobcard['clipinfo'] else " "
        
        

        #Setup Box Config Information
        box_title_size=config['boxcover']['title_size'] if "title_size" in config['boxcover'] else 100
        box_star_size= config['boxcover']['star_size'] if "star_size" in config['boxcover'] else 50
        box_support_size= config['boxcover']['support_size'] if "support_size" in config['boxcover'] else 50
        box_shorttitle_size= config['boxcover']['shorttitle_size'] if "shorttitle" in config['boxcover'] else 50
        box_edgeid_size= config['boxcover']['partno_size'] if "partno_size" in config['boxcover'] else 50
        box_font = config['boxcover']['font'] if "font" in config['boxcover'] else '/usr/local/font/Skia.ttf'
        box_alignment= jobcard['boxcover']['alignment'] if "box_alignmnet" else 'right'
        box_font_color= config['boxcover']['font_color'] if "font_color" else 'red'
        
        #Setup Thumbnail information if needed
        if item_thumbnail == True:
            logger.info("Thumbnail creation requeseted")
            thumb_size = jobcard['thumbnails']['size'] if "size" in jobcard['thumbnails'] else 96
            thumb_name = jobcard['thumbnails']['name'] if "name" in jobcard['thumbnails'] else None
            thumb_outdir = jobcard['thumbnails']['out_dir'] if "out_dir" in jobcard['thumbnails'] else None
            thumb_suffix = jobcard['thumbnails']['suffix'] if "suffix" in jobcard['thumbnails'] else None
            thumb_ext = jobcard['thumbnails']['ext'] if "ext" in jobcard['thumbnails'] else '.jpg'
            if not thumb_name == None and not thumb_outdir == None:
                thumb_destination = destination + "/" + str(thumb_name) + "/" + str(thumb_outdir)
            elif not thumb_name == None and thumb_outdir == None:
                thumb_destination = destination + "/" + str(thumb_name)
            elif thumb_name == None and not thumb_outdir == None:
                thumb_destination = destination + "/" + str(thumb_outdir)     
            else:
                thumb_destination = destination 
            logger.info("\tThumbnail Destination: " + str(thumb_destination))   
        else:
            logger.info("Thumbnail Creation - Not Requested")

        # Setup Watermarking
        if item_watermark == True:
            logger.info("Watermark creation requeseted")
            water_font_size = jobcard['watermark']['fontsize'] if "fontsize" in jobcard['watermark'] else 100
            water_template = jobcard['watermark']['template'] if "template" in jobcard['watermark'] else "$STAR © EDGE"
            water_location = jobcard['watermark']['location'] if "location" in jobcard['watermark'] else 'SouthEast'
            water_outdir = jobcard['watermark']['out_dir'] if "out_dir" in jobcard['watermark'] else None
            water_name = jobcard['watermark']['name'] if "name" in jobcard['watermark'] else None
            water_color = jobcard['watermark']['color'] if "color" in jobcard['watermark'] else 'red'
            water_suffix = jobcard['watermark']['suffix'] if "suffix" in jobcard['watermark'] else None
            water_ext = jobcard['watermark']['ext'] if "ext"  in jobcard['watermark'] else '.jpg'
            water_font = config['boxcover']['font'] if "font" in config['boxcover'] else "/usr/local/etc/Skia.ttf"

            
            if not water_name == None and not water_outdir == None:
                water_destination = destination + "/" + str(water_name) + "/" + str(water_outdir)
            elif not water_name == None and water_outdir == None:
                water_destination = destination + "/" + str(water_name)
            elif water_name == None and not water_outdir == None:
                water_destination = destination + "/" + str(water_outdir)     
            else:
                water_destination = destination 
            logger.info("\tWatermark Destination: " + str(water_destination))   
        else:
            logger.info("Watermark not requeted")
        
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
             
    # Create Directories if needed
    if not os.path.isdir(finaldestination) and not noexec:
        os.makedirs(finaldestination,0777)
        logger.info("Creating Directory: " + finaldestination)
    else:
        logger.info("Creating Directory: " + finaldestination)   

    # Create Watermark and Thumbnail directories if needed
    try:
        if not os.path.isdir(thumb_destination) and not noexec and item_thumbnail == True:
            os.makedirs(thumb_destination,0777)
            logger.info("Creating Directory: " + thumb_destination)
        elif item_thumbnail == True:
            logger.info("Creating Directory: " + thumb_destination) 
    except:
        logger.info("No thumbnail directory needed")        
    
    try:
        if not os.path.isdir(water_destination) and not noexec and item_watermark == True:
            os.makedirs(water_destination,0777)
            logger.info("Creating Directory: " + water_destination)
        elif item_watermark == True:
            logger.info("Creating Directory: " + water_destination)  
    except:
         logger.info("No Watermark directory needed")        
   
    # Change Left, Center, Right for Imagemagick Terms
    if box_alignment == 'left':
        title = " " + title
        all_star = " " + star + " & " + star2
        supporting = "  " + supporting
        gravity='Northwest'
    if box_alignment == 'center':
        gravity = 'North'
        all_star = star + " & " + star2
    if box_alignment == 'right':
        gravity='NorthEast'       
        title = title + " "
        all_star = star + " & " + star2 + " "
        supporting =  supporting + "  "

    # Display Text Parameters and Alignment
    logger.info("Box Cover will be created with the following information")
    logger.info("Title: " + str(title))
    logger.info("Short Title: " + str(shorttitle))
    logger.info("Star: " + str(star))
    logger.info("Star2: " + str(star2))
    logger.info("Support: " + str(supporting))
    
    # Modify title and shortitle for creation
    shorttitle_f = shorttitle.replace(" ","\\n")
    title_f = title.replace("'","\\'")

    # Need to set resize to max edge
    max_size = max(item_height, item_width)
    if item_width == max_size:
        logger.info("Image Landscape mode")
        resizeto = str(item_width) + "x"
    elif item_height == max_size:
        logger.info("Image Portrait mode")
        resizeto = "x" + str(item_height)    

    # Make image the correct size or add black background if needed. 
    RESIZE_CMD = CONVERT + " -size 3724x5616 canvas:black '" + str(item_source) + "' -gravity center -resize " + str(resizeto) + "  -flatten '" + finaldestination +  "/" + str(edgeid)  + str(item_suffix) + "_source" + item_ext +"'"
    RESIZE_IMG = "'" + finaldestination +  "/" + str(edgeid)  + str(item_suffix) + "_source" + item_ext +"'"
    BOX_PSD = "'"  + finaldestination +  "/" + str(edgeid)  + str(item_suffix) + ".psd'"
    BOX_IMG = "'" + finaldestination +  "/" + str(edgeid)  + str(item_suffix) + item_ext +"'"
    
    logger.info("Resize Command:\n\t" + str(RESIZE_CMD))
    
    CMD = CONVERT + " -verbose -size " + str(item_width) + "x" + str(item_height) + " -font " + str(box_font) + " -pointsize " + str(box_title_size)
    CMD = CMD + " -fill " + str(box_font_color) + " \( \( -gravity " + gravity + " -background transparent -pointsize  " + str(box_title_size) + "  label:\"" + title_f +"\"" + " -pointsize " + str(box_star_size)
    CMD = CMD + " -annotate +0+250 '" + str(all_star) + "'" + " -pointsize " + str(box_support_size) + " -annotate +0+450 '" +  str(supporting) + "' -splice 0x16 \)"
    CMD = CMD + " \( +clone -background black -shadow 20x-9+0+0 \) -background transparent +swap -layers merge +repage \)  \( \( -gravity West -background transparent -pointsize " 
    CMD = CMD + str(box_shorttitle_size) + " label:'" + str(shorttitle_f) + "'  -splice 50x0 \)  \( +clone -background black -shadow 20x-9+0+0 \) -background transparent +swap -layers merge +repage \) \( -gravity SouthWest "+ " -pointsize " +str(box_edgeid_size) + " -background transparent label:"
    CMD = CMD + str(edgeid) +" -splice 100x0 \) " + "  \( \( -gravity SouthEast -background transparent label:'EDGE   \n' -splice 0x18  -pointsize 50  -annotate +50+192 '  _____________________   ' -splice 0x18 -pointsize 100 -annotate +50+120 'interactive  '   \) "
    CMD = CMD + " \( +clone -background black -shadow 60x18+0+0 \) -background transparent +swap -layers merge +repage \) \(  -label 'image' -background transparent -mosaic label:blank "
    CMD = CMD + "'" + str(RESIZE_IMG) + "' \) \(  -clone 0--1 -mosaic  \) -trim -reverse " + BOX_PSD + "; " + CONVERT + " " + BOX_PSD + " -flatten " + str(BOX_IMG)
    
     
    
    logger.warning("Box Cover Command\n\t" + CMD)

    
    logger.info("Produce - End")
    return(Error)


def exists(source, output,  component, jobcard, config, noexec):
    result = ''
    logger.info("Exists - Start")
    
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
    
    # Set Commands we will need
    CONVERT=config['locations']['convert']
    
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
        item_thumbnail = jobcard[component]['thumbnail'] if "thumbnail" in jobcard[component] else None
        item_watermark = jobcard[component]['watermark'] if "watermark" in jobcard[component] else None
        item_count = jobcard[component]['count'] if "count" in jobcard[component] else None
        item_timed = jobcard[component]['timed'] if "timed" in jobcard[component] else None
        item_size = jobcard[component]['size'] if "size" in jobcard[component] else None
 
        
        #Setup Thumbnail information if needed
        if item_thumbnail == True:
            logger.info("Thumbnail creation requeseted")
            thumb_size = jobcard['thumbnails']['size'] if "size" in jobcard['thumbnails'] else 96
            thumb_name = jobcard['thumbnails']['name'] if "name" in jobcard['thumbnails'] else None
            thumb_outdir = jobcard['thumbnails']['out_dir'] if "out_dir" in jobcard['thumbnails'] else None
            thumb_suffix = jobcard['thumbnails']['suffix'] if "suffix" in jobcard['thumbnails'] else None
            thumb_ext = jobcard['thumbnails']['ext'] if "ext" in jobcard['thumbnails'] else '.jpg'
            if not thumb_name == None and not thumb_outdir == None:
                thumb_destination = destination + "/" + str(thumb_name) + "/" + str(thumb_outdir)
            elif not thumb_name == None and thumb_outdir == None:
                thumb_destination = destination + "/" + str(thumb_name)
            elif thumb_name == None and not thumb_outdir == None:
                thumb_destination = destination + "/" + str(thumb_outdir)     
            else:
                thumb_destination = destination 
            logger.info("\tThumbnail Destination: " + str(thumb_destination))   
        else:
            logger.info("Thumbnail Creation - Not Requested")

        # Setup Watermarking
        if item_watermark == True:
            logger.info("Watermark creation requeseted")
            water_font_size = jobcard['watermark']['fontsize'] if "fontsize" in jobcard['watermark'] else 100
            water_template = jobcard['watermark']['template'] if "template" in jobcard['watermark'] else "$STAR © EDGE"
            water_location = jobcard['watermark']['location'] if "location" in jobcard['watermark'] else 'SouthEast'
            water_outdir = jobcard['watermark']['out_dir'] if "out_dir" in jobcard['watermark'] else None
            water_name = jobcard['watermark']['name'] if "name" in jobcard['watermark'] else None
            water_color = jobcard['watermark']['color'] if "color" in jobcard['watermark'] else 'red'
            water_suffix = jobcard['watermark']['suffix'] if "suffix" in jobcard['watermark'] else None
            water_ext = jobcard['watermark']['ext'] if "ext"  in jobcard['watermark'] else '.jpg'
            if not water_name == None and not water_outdir == None:
                water_destination = destination + "/" + str(water_name) + "/" + str(water_outdir)
            elif not water_name == None and water_outdir == None:
                water_destination = destination + "/" + str(water_name)
            elif water_name == None and not water_outdir == None:
                water_destination = destination + "/" + str(water_outdir)     
            else:
                water_destination = destination 
            logger.info("\tWatermark Destination: " + str(water_destination))   
        else:
            logger.info("Watermark not requeted")
        
    except:
         logger.warning("Not all variables set properly")   
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
             
    # Create Directories if needed
    if not os.path.isdir(finaldestination) and not noexec:
        os.makedirs(finaldestination,0777)
        logger.info("Creating Directory: " + finaldestination)
    else:
        logger.info("Creating Directory: " + finaldestination)   

    # Create Watermark and Thumbnail directories if needed
    try:
        if not os.path.isdir(thumb_destination) and not noexec and item_thumbnail == True:
            os.makedirs(thumb_destination,0777)
            logger.info("Creating Directory: " + thumb_destination)
        elif item_thumbnail == True:
            logger.info("Creating Directory: " + thumb_destination) 
    except:
        logger.info("No thumbnail directory needed")        
    
    try:
        if not os.path.isdir(water_destination) and not noexec and item_watermark == True:
            os.makedirs(water_destination,0777)
            logger.info("Creating Directory: " + water_destination)
        elif item_watermark == True:
            logger.info("Creating Directory: " + water_destination)  
    except:
         logger.info("No Watermark directory needed")        
   

    # Display Text Parameters and Alignment
    logger.info("Box Cover will be copied with the following information")
    BOX_PSD = "'"  + finaldestination +  "/" + str(edgeid)  + str(item_suffix) + ".psd'"
    BOX_IMG = "'" + finaldestination +  "/" + str(edgeid)  + str(item_suffix) + item_ext +"'"
    
    logger.info("Copy PSD file if exists")
    if os.path.isfile(BOX_PSD) and not noexec:
        logger.info("Copy PSD file")
        result = shutil.copyfile(BOX_PSD, finaldestination)
        logger.info(result)
    else:
        logger.warn("NO PSD File exists")
        
    if os.path.isfile(BOX_IMG) and not noexec: 
        logger.info("Copy JPG Box cover")
        result = shutil.copyfile(BOX_IMG, finaldestination)
        logger.info(result)
    else:
        logger.warn("No Box Cover Exists")
        Error = True
    
        
              
            
    
    
    
    logger.info("Exists - End")
    return(Error)



def ignore(source, output,  component, jobcard, config, noexec):
    logger.info("Ignore - Start")
    
    logger.warn("Component: " + str(component) + "is being ignored")
    
    logger.info("Ignore - End")
    return(Error)