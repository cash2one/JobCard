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
import subprocess
import maketext
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
    # Globals 
    CONVERT=config['locations']['convert']
    FFMPEG=config['locations']['ffmpeg']
    FFPROBE=config['locations']['ffprobe']
    MOGRIFY=config['locations']['mogrify']
    ATOMICPARSLEY=config['locations']['atomicparsley']
    
    Error = False

    # Start
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
        item_width = jobcard[component]['size_width'] if "size_width" in jobcard[component] else 720
        item_height = jobcard[component]['size_height'] if "size_height" in jobcard[component] else 320
        item_kbps =  jobcard[component]['size_kbps'] if "size_kbps" in jobcard[component] else 1500
        item_outdir = jobcard[component]['out_dir'] if "out_dir" in jobcard[component] else None
        item_suffix = jobcard[component]['suffix'] if "suffix" in jobcard[component] else None
        item_ext = jobcard[component]['ext'] if "ext" in jobcard[component] else None
        item_name = jobcard[component]['name'] if "name" in jobcard[component] else None
        #item_thumbnail = jobcard[component]['thumbnail'] if "thumbnail" in jobcard[component] else None
        item_watermark = jobcard[component]['watermark'] if "watermark" in jobcard[component] else None
        item_count = jobcard[component]['count'] if "count" in jobcard[component] else None
        item_timed = jobcard[component]['timed'] if "timed" in jobcard[component] else None
        item_size = jobcard[component]['size'] if "size" in jobcard[component] else None
        item_capture = jobcard[component]['capture'] if "capture" in jobcard[component] else False
        templates = config['default']['templates'] if "templates" in config['default'] else ""
        item_boxcover = jobcard['component']['boxcover'] if "boxcover" in  jobcard['component'] else None
        if item_boxcover == "produce" or item_boxcover == "exsist":
            item_boxcover_img =  source + "/" + str(jobcard['boxcover']['src']) if "src" in jobcard['boxcover'] else ""
            
        
        if item_capture:
            capture_thumbnail = jobcard['capture']['thumbnail'] if "thumbnail" in jobcard['capture'] else False
            capture_watermark = jobcard['capture']['watermark'] if "watermark" in jobcard['capture'] else False
        else:
            capture_thumbnail = False
            capture_watermark = False
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
        clip_supporting_name = jobcard['clipinfo']['supporting']['name'] if "name" in jobcard['clipinfo']['supporting'] else ''
        clip_star2 = True if "star2" in jobcard['clipinfo'] else False
        if clip_star2:
            logger.info("Loading Star 2")
            clip_star2_name = jobcard['clipinfo']['star2']['name'] if "name" in jobcard['clipinfo']['star2'] else ''
        
        
        preview_color = config['compliance']['preview_font_color'] if 'preview_font_color' in config['compliance'] else 'black'
        preview_back = config['compliance']['preview_color'] if 'preview_color' in config['compliance'] else 'blue'
        preview_font = config['compliance']['preview_font'] if 'preview_font' in config['compliance'] else '/usr/local/etc/Arial.ttf'
        preview_x = config['compliance']['preview_x'] if 'preview_x' in config['compliance'] else 100
        preview_y = config['compliance']['preview_y'] if 'preview_y'  in config['compliance'] else 100
        preview_fontsize = config['compliance']['preview_font_size'] if 'preview_font_size' in config['compliance'] else 50
        preview_suffix = config['compliance']['preview_suffix'] if 'preview_suffix' in config['compliance'] else '_preview'
        preview_ext = config['compliance']['preview_ext'] if 'preview_ext' in config['compliance'] else '.mp4'
        # Remember to look for absolute
        compliance_template = config['compliance']['template'] if 'template' in config['compliance'] else None
        compliance_back = config['compliance']['compliance_color'] if 'compliance_color' in config['compliance'] else 'black'
        compliance_color = config['compliance']['compliance_text_color'] if 'compliance_text_color' in config['compliance'] else 'green' 
        compliance_textsize = config['compliance']['compliance_text_size'] if 'compliance_text_size' in config['compliance'] else 50
        compliance_suffix = config['compliance']['compliance_suffix'] if 'compliance_suffix' in config['compliance'] else '_preview'
        compliance_ext = config['compliance']['compliance_ext'] if 'compliance_ext' in config['compliance'] else '.mp4'
        compliance_font = config['compliance']['compliance_font'] if 'compliance_font' in config['compliance'] else '/usr/local/etc/Arial.ttf'
        compliance_fontsize = config['compliance']['compliance_font_size'] if 'compliance_font_size' in config['compliance'] else 50
        
        text_name = jobcard['compliance_txt']['name'] if "name" in jobcard['compliance_txt'] else None
        text_outdir = jobcard['compliance_txt']['out_dir'] if "out_dir" in jobcard['compliance_txt'] else None
        text_suffix = jobcard['compliance_txt']['suffix'] if "suffix" in jobcard['compliance_txt'] else "_compliance"
        text_ext = jobcard['compliance_txt']['ext'] if "ext" in jobcard['compliance_txt'] else ".txt"

        
        mp4_decode = config['codec']['mp4_decode'] if "mp4_decode" in config['codec'] else "h264_vda"
        mp4_encode = config['codec']['mp4_encode'] if "mp4_encode" in config['codec'] else "h264_libx264" 
        mp4_simple = config['codec']['mp4_simple'] if "mp4_simple" in config['codec'] else "mpeg4"
        mp4_jpeg = config['codec']['mp4_jpeg'] if "mp4_jpeg" in config['codec'] else "mjpeg"
        mp4_accel = config['codec']['mp4_accel'] if "mp4_accel" in config['codec'] else ""
        mp4_threads = config['codec']['mp4_threads'] if "mp4_threads" in config['codec'] else "-threads 2"
        mp4_scalefilter = config['codec']['mp4_scalefilter'] if "mp4_scalefilter" in config['codec'] else "scale"

        
        video_scale = str(item_width) + ":" + str(item_height)
        video_bufsize = int(str(item_kbps)) * 1000
        
        #setup final destination in complex situations
        if not item_name == None and not item_outdir == None:
            finaldestination = destination + "/" + str(item_name) + "/" + str(item_outdir)
        elif not item_name == None and item_outdir == None:
            finaldestination = destination + "/" + str(item_name)
        elif item_name == None and not item_outdir == None:
            finaldestination = destination + "/" + str(item_outdir)     
        else:
            finaldestination = destination
        
        if not text_name == None and not text_outdir == None:
            text_location = destination + "/" + str(text_name) + "/" + str(text_outdir)
        elif not text_name == None and  text_outdir == None:
            text_location =  destination + "/" + str(text_name)
        elif text_name == None and not text_outdir == None:
            text_location = destination + "/" + str(text_outdir)
        else:
            text_location = destination    
        
        # Setup Capture
        if item_capture == True:
            logger.info("Capture creation requeseted")
            capture_frame_every = jobcard['capture']['frame_every'] if "frame_every" in jobcard['capture'] else 30
            capture_outdir = jobcard['capture']['out_dir'] if "out_dir" in jobcard['capture'] else None
            capture_name = jobcard['capture']['name'] if "name" in jobcard['capture'] else None
            capture_suffix = jobcard['capture']['suffix'] if "suffix" in jobcard['capture'] else None
            capture_ext = jobcard['capture']['ext'] if "ext"  in jobcard['capture'] else '.jpg'
            if not capture_name == None and not capture_outdir == None:
                capture_destination = finaldestination + "/" + str(component) + "_" +  str(capture_name) + "/" + str(capture_outdir)
            elif not capture_name == None and capture_outdir == None:
                capture_destination = finaldestination + "/" + str(component) + "_"+ str(capture_name) 
            elif capture_name == None and not capture_outdir == None:
                capture_destination = finaldestination + "/" + str(component) + "_"+ str(capture_outdir)     
            else:
                capture_destination = destination + "/" + str(component) + "_" + str(capture_name) 
            logger.info("\tCapture Destination: " + str(capture_destination))   
        else:
            logger.info("Capture not requeted")
            # Capture Destination to invalid setting
            capture_destination ="NOTVALID"

        #Setup Thumbnail information if needed
        if capture_thumbnail == True and item_capture == True:
            logger.info("Thumbnail creation on captured images requeseted")
            thumb_size = jobcard['thumbnails']['size'] if "size" in jobcard['thumbnails'] else 96
            thumb_name = jobcard['thumbnails']['name'] if "name" in jobcard['thumbnails'] else None
            thumb_outdir = jobcard['thumbnails']['out_dir'] if "out_dir" in jobcard['thumbnails'] else None
            thumb_suffix = jobcard['thumbnails']['suffix'] if "suffix" in jobcard['thumbnails'] else None
            thumb_ext = jobcard['thumbnails']['ext'] if "ext" in jobcard['thumbnails'] else '.jpg'
            if not thumb_name == None and not thumb_outdir == None:
                thumb_destination = finaldestination + "/" + str(component) + "_" + str(capture_name) + "/" + str(thumb_name) + "/" + str(thumb_outdir)
            elif not thumb_name == None and thumb_outdir == None:
                thumb_destination = finaldestination + "/" + str(component) + "_" + str(capture_name) + "/"+ str(thumb_name)
            elif thumb_name == None and not thumb_outdir == None:
                thumb_destination = finaldestination + "/" + str(component) + "_" + str(capture_name) + "/" + str(thumb_outdir)     
            else:
                thumb_destination = finaldestination + "/" + str(component) + "_" + str(capture_name) 
            logger.info("\tThumbnail Destination: " + str(thumb_destination))   
        else:
            logger.info("Thumbnail Creation - Not Requested")
            thumb_destination =""
            

        # Setup Watermarking
        if item_watermark == True:
            logger.info("Watermark creation requeseted")
            water_font_size = jobcard['watermark']['fontsize'] if "fontsize" in jobcard['watermark'] else 100
            water_video_font_size = jobcard['watermark']['videofontsize'] if "videofontsize" in jobcard['watermark'] else 100
            water_template = jobcard['watermark']['template'] if "template" in jobcard['watermark'] else "$EDGEID © EDGE"
            water_location = jobcard['watermark']['location'] if "location" in jobcard['watermark'] else 'SouthEast'
            water_outdir = jobcard['watermark']['out_dir'] if "out_dir" in jobcard['watermark'] else None
            water_name = jobcard['watermark']['name'] if "name" in jobcard['watermark'] else None
            water_color = jobcard['watermark']['color'] if "color" in jobcard['watermark'] else 'red'
            water_suffix = jobcard['watermark']['suffix'] if "suffix" in jobcard['watermark'] else None
            water_ext = jobcard['watermark']['ext'] if "ext"  in jobcard['watermark'] else '.jpg'
            water_font = config['boxcover']['font'] if "font" in config['boxcover'] else "/usr/local/etc/Skia.ttf"
            if clip_star2:
                watermark_text = Template(water_template).safe_substitute(STAR=clip_star_name, STAR2=clip_star2_name, EDGEID=edgeid)
            else:
                watermark_text = Template(water_template).safe_substitute(STAR=clip_star_name, EDGEID=edgeid)

            #watermark_cmd = "-vf drawtext=\"$FONT text=\'$TEMPLATE\': fontcolor=$COLOR: fontsize=$FONTSIZE: box=1: boxcolor=black: x=w-tw-5:y=h-th-5\""
            watermark_cmd = "drawtext=\"text=\'$TEMPLATE\':x=w-tw-5:y=h-th-5:fontfile=$FONT:fontsize=$FONTSIZE:fontcolor=$COLOR:shadowcolor=black:shadowx=2:shadowy=2:box=1:boxcolor=white\""
            watermark = Template(watermark_cmd).safe_substitute(FONT=water_font, TEMPLATE=watermark_text, COLOR=water_color, FONTSIZE=water_video_font_size)
        else:
            logger.info("Watermark not requested")    
            water_destination =""
            
        if item_watermark == True and item_capture == True:           
            if not water_name == None and not water_outdir == None:
                water_destination = finaldestination + "/" + str(component) + "_" + str(capture_name) + "/" + str(water_name) + "/" + str(water_outdir)
            elif not water_name == None and water_outdir == None:
                water_destination = finaldestination + "/" + str(component) + "_" + str(capture_name) + "/" + str(water_name)
            elif water_name == None and not water_outdir == None:
                water_destination = finaldestination + "/" + str(component) + "_" + str(capture_name) + "/" + str(water_outdir)     
            else:
                water_destination = finaldestination + "/" + str(component) + "_" + str(capture_name) 
            logger.info("\tWatermark Destination: " + str(water_destination))           
                   
        else:
            logger.info("Watermark Only on Video File")
        

    except Exception as e:  
        logger.warning("Not all variables set properly; exception " + str(e))   
    # Test Source for relative or absoulte path
    
    if item_src[0] != "/":                       
        logger.debug("Relative Path")    
        item_source = source + "/" + item_src
    else:
        logger.debug("Absolute Path")
        item_source = jobcard[component]['src']  
    
    #Check Compliance Template for relative location
   
    if compliance_template[0] != "/":
        logger.debug("Compliant Template - relative Path") 
        compliance_template = str(templates) + "/" + str(compliance_template)
    else:
        logger.debug("Compliant Template - absolute Path") 
        
    logger.info("Compliance Template: " + str(compliance_template) )  
     
     
     
     
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
    logger.info("\tItem Watermark: " + str(item_watermark))
    logger.info("\tItem Count: " + str(item_count))
    logger.info("\tItem Timed: " + str(item_timed))
    logger.info("\tItem Size: " + str(item_size))  
    logger.info("\tCapture: " + str(item_capture))
    
   
    if item_capture:
        logger.info("\t\tThumbnail on Capture Images: " + str(capture_thumbnail)) 
        logger.info("\t\tWatermark on Capture Images: " + str(capture_watermark)) 
        logger.info("\t\tCapture still images every: " + str(capture_frame_every) + " seconds")      
        if not os.path.isdir(capture_destination) and not noexec and item_capture == True:
            os.makedirs(capture_destination,0777)
            logger.info("Creating Directory [Capture Destination]:\t" + capture_destination)
        else:
            logger.info("Creating Directory [Capture Destination]:\t" + capture_destination)       
             
    # Create Directories if needed
    if not os.path.isdir(finaldestination) and not noexec:
        os.makedirs(finaldestination,0777)
        logger.info("Creating Directory [Final Destination]:\t" + finaldestination)
    else:
        logger.info("Creating Directory:[Final Destination]:\t" + finaldestination)  
        
    
    if item_watermark == True:
        if not os.path.isdir(water_destination) and not noexec and capture_watermark == True:
            os.makedirs(water_destination,0777)
            logger.info("Creating Directory [Watermark Destination]:\t" + water_destination)
        else:
            logger.info("Creating Directory [Watermark Destination]:\t" + water_destination)  
    if capture_thumbnail == True:
        if not os.path.isdir(thumb_destination) and not noexec and capture_thumbnail == True:
            os.makedirs(thumb_destination,0777)
            logger.info("Creating Directory [Thumbnail Destination]:\t" + thumb_destination)
        else:
            logger.info("Creating Directory [Thumbnail Destination]:\t" + thumb_destination)  



    # Phase 1 - Do movie captures if requested. 
    if item_capture == True:
        CMD_TEMPLATE = "$FFMPEG -c:v $DECODEC -i '$VIDEO' -thread_type slice -hide_banner -vf fps=1/$FRAME -c:v mjpeg '$DESTINATION/$EDGEID${SUFFIX}_%03d$EXT' "
        CMD = Template(CMD_TEMPLATE).safe_substitute(FFMPEG=FFMPEG, VIDEO=item_source, DECODEC=mp4_decode, ENCODEC=mp4_jpeg, FRAME=capture_frame_every, DESTINATION=capture_destination, EDGEID=edgeid, SUFFIX=capture_suffix, EXT=capture_ext)
        logger.info("Capture Command:\n\t" + str(CMD))
        if noexec:
            logger.info( "No Execute" )
            capture_result=subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            logger.warning("Running Command" )  
            capture_result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)       
            logger.info( "Capture on " + item_src + "Started" )

    # Phase 2 - Transcode Video
    
    if item_watermark == False:
        CMD_TEMPLATE = "$FFMPEG  -threads 64  $MP4_ACCEL  -c:v $DECODEC -y -i '$VIDEO'  -vf $SCALEFILTER=$SCALE,setdar=dar=16/9  -b:v ${KBPS}k -maxrate ${KBPS}k -bufsize $BUFSIZE  -preset fast  -c:v $ENCODEC '$DESTINATION/${EDGEID}_${WIDTH}x${HEIGHT}x${KBPS}_vid${EXT}'"
        watermark = ""
    else:
        logger.info("Watermarking the video" + str(watermark.encode('utf-8')))
        CMD_TEMPLATE = "$FFMPEG  -threads 64  $MP4_ACCEL  -c:v $DECODEC -y -i '$VIDEO' -vf $WATERMARK -vf $SCALEFILTER=$SCALE,setdar=dar=16/9  -b:v ${KBPS}k -maxrate ${KBPS}k -bufsize $BUFSIZE  -preset fast  -c:v $ENCODEC '$DESTINATION/${EDGEID}_${WIDTH}x${HEIGHT}x${KBPS}_vid${EXT}'"
    
    CMD = Template(CMD_TEMPLATE).safe_substitute(FFMPEG=FFMPEG,HWACCEL=mp4_accel, WATERMARK=str(watermark.encode('utf-8')), VIDEO=item_source, DECODEC=mp4_decode, ENCODEC=mp4_encode,MP4_ACCEL=mp4_accel, SCALEFILTER=mp4_scalefilter, SCALE=video_scale, HEIGHT=item_height, WIDTH=item_width, KBPS=item_kbps, BUFSIZE=video_bufsize, DESTINATION=finaldestination, EDGEID=edgeid, SUFFIX=item_suffix, EXT=item_ext)

    logger.warning("Transcode Command\n\t" + CMD)
    if  noexec:
        transcode_result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        logger.warning("Running Command" )  
        transcode_result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)       
        logger.info( "Transcode" + item_src + "Started" )
    
    # Phase 3 - Create Preview
    # Modify title and shortitle for creation
    shorttitle_f = clip_shorttitle.replace(" ","\\n")
    title_f = clip_title.replace("'","\\'")

    logger.info("Creating Preview for " + component)
    
    logger.info("Creating Preview for " + component)
    
    CMD = FFMPEG + " -y -f lavfi -r 29.97 -i color=" + preview_back +":"+ str(item_width) + "x" + str(item_height) + " -f lavfi -i anullsrc -filter_complex  "
    # Make Title Line
    CMD = CMD + "\"fade=t=in:st=00:d=0.5,fade=t=out:st=04:d=1,drawtext=enable='between(t,.5,04)':fontfile=" + preview_font + ":text=\'" + title_f +  "\':x=(w-text_w)/2" + ":y=" + str(preview_y) +":fontcolor=" + preview_color  + ":fontsize=" + str(preview_fontsize)
    # Sub Title
    CMD = CMD +  ",drawtext=enable='between(t,.5,04)':fontfile=" + preview_font + ":text=\'Starring " + "\':x=(w-text_w)/2" +":y=" + str(preview_y+100) +":fontcolor=" + preview_color + ":fontsize=" + str(preview_fontsize)
    
    CMD = CMD +  ",drawtext=enable='between(t,.5,04)':fontfile=" + preview_font + ":text=\'" + clip_star_name + " and " + clip_supporting_name + "\':x=(w-text_w)/2" +":y=" + str(preview_y+200) +":fontcolor=" + preview_color + ":fontsize=" + str(preview_fontsize)
    
    CMD = CMD +  ",drawtext=enable='between(t,.5,04)':fontfile=" + preview_font + ":text=\'IN " + "\':x=(w-text_w)/2" +":y=" + str(preview_y+300) +":fontcolor=" + preview_color + ":fontsize=" + str(preview_fontsize)
    
    # Keywords
    CMD = CMD +  ",drawtext=enable='between(t,.5,04)':fontfile=" + preview_font + ":text=\'" + clip_shorttitle + "\':x=(w-text_w)/2:y=" + str(preview_y+400) +":fontcolor=" + preview_color + ":fontsize=" + str(preview_fontsize)
    
    CMD = CMD +  ",drawtext=enable='between(t,.5,04)':fontfile=" + preview_font + ":text=\'Release Date " + jobcard['clipinfo']['releasedate'] + "\':x=(w-text_w)/2:y=" + str(preview_y+500) +":fontcolor=" + preview_color + ":fontsize=" + str(preview_fontsize*.6)
    CMD = CMD +  ",drawtext=enable='between(t,.5,04)':fontfile=" + preview_font + ":text=\'Production Date " + jobcard['clipinfo']['productiondate'] + "\':x=(w-text_w)/2:y=" + str(preview_y+550) +":fontcolor=" + preview_color + ":fontsize=" + str(preview_fontsize*.6)

    # Wrap end of command
    CMD = CMD + "\" -c:v " + mp4_simple + " -b:v " + str(item_kbps) + "k -pix_fmt yuv420p -video_track_timescale 15360 -c:a aac -strict -2 -ar 48000 -ac 2 -sample_fmt fltp -t 05 '" + finaldestination + "/" + edgeid + "_" + str(item_width) + "x" + str(item_height) + "x" + str(item_kbps) + str(preview_suffix) + str(preview_ext) +"'" 

    logger.info("Preview Command: \n\t" + str(CMD))
    if noexec:
        preview_result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        logger.warning("Running Command" )  
        preview_result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)       
        logger.info( "Preview" + item_src + "Started" )
    
    # Phase 4 Create Compliance Trailer
    #Create a text file
    maketext.produce(source, output, 'compliance_txt', jobcard, config, noexec)
    
    #Normalize the text size based on 1920x1080
    normalize = float(float(item_height) / float(1080))
    logger.info("Normalize the size by " + str(normalize))
    normalized_font = int(float(compliance_textsize) * normalize)
    logger.info("Normalized size " + str(normalized_font))
    
    logger.info("Text File Location:" + text_location + "/" + edgeid + text_suffix + text_ext )
    CMD = FFMPEG + " -y -f lavfi -r 29.97 -i color=" + compliance_back + ":" +str(item_width) + "x" + str(item_height) + " -f lavfi -i anullsrc -vf drawtext=\"fontfile=" + compliance_font + ":fontcolor=" + compliance_color + ": fontsize=" + str(normalized_font) + ":textfile='" + text_location  + "/" + edgeid + text_suffix + text_ext + "'" + ":x=50:y=50,fade=t=in:st=00:d=3.5,fade=t=out:st=08:d=2\" -c:v mpeg4 -b:v " + str(item_kbps) + "k  -pix_fmt yuv420p -video_track_timescale 15360 -c:a aac -strict -2 -ar 48000 -ac 2 -sample_fmt fltp -t 10 '" + finaldestination + "/" + edgeid + "_" + str(item_width) + "x" + str(item_height) + "x" + str(item_kbps) + compliance_suffix + compliance_ext + "'"

    logger.info("Compliance Command:\n\t" + str(CMD))
    if noexec:
        compliance_result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        logger.warning("Running Command" )  
        compliance_result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)       
        logger.info( "Compliance" + item_src + "Started" )

    
    # Phase 5 - Concat the Preview - Transcode - Compliance VIdeos
    # Requires Preview, Compliance, and Transcode to complete
    logger.info("Check if Preview Completed")
    stdoutdata, stderrdata = preview_result.communicate()
    preview_status = preview_result.returncode 
    if preview_status == 0:
        logger.info("\t\t Preview Completed, returned Status: " + str(preview_status))
    else:
        logger.error("\t\t Preview failed, with Status:"+ str(preview_status))
        Error = True

    logger.info("Check if Compliance Completed")
    stdoutdata, stderrdata = compliance_result.communicate()
    compliance_status = compliance_result.returncode 
    if compliance_status == 0:
        logger.info("\t\tCompliance Completed, returned Status: " + str(compliance_status))
    else:
        logger.error("\t\tCompliance failed, with Status:"+ str(compliance_status))
        Error = True

    logger.info("Check if Transcode Completed")
    stdoutdata, stderrdata = transcode_result.communicate()
    transcode_status = transcode_result.returncode 
    if transcode_status == 0:
        logger.info("\t\t Transcode returned Status: " + str(transcode_status))
    else:
        logger.error("\t\t Transcode failed with Status:"+ str(transcode_status))
        Error = True

    CMD = FFMPEG + "  -i '" + finaldestination + "/" + edgeid + "_" + str(item_width) + "x" + str(item_height) + "x" + str(item_kbps) + preview_suffix + preview_ext + "'  -i '" + finaldestination + "/" + edgeid + "_" + str(item_width) + "x" + str(item_height) + "x" + str(item_kbps) + "_vid" + item_ext + "' -i '"  + finaldestination + "/" + edgeid + "_" + str(item_width) + "x" + str(item_height) + "x" + str(item_kbps)  + compliance_suffix + compliance_ext + "' " 
    CMD = CMD + "-filter_complex 'concat=n=3:v=1:a=1'  -c:v " + mp4_encode +" -b:v " + str(item_kbps) +"k -bufsize 1500000  -c:a aac -strict -2  -y '"   + finaldestination + "/" + edgeid + "_" + str(item_width) + "x" + str(item_height) + "x" + str(item_kbps) + "_assembled.mp4'"
 
    logger.warning("Concat Command\n\t" + CMD)
    if not noexec:
        concat_result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info("Check if Concat Completed")
        stdoutdata, stderrdata = concat_result.communicate()
        concat_status = concat_result.returncode 
        if concat_status == 0:
            logger.info("\t\tConcat returned Status: " + str(concat_status))
        else:
            logger.error("\t\tConcat failed with Status:"+ str(concat_status))
            Error = True
    else:
        concat_result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
    
    # Phase 6 - Add Meta Data to MP4 Video
    # Requires Concat to Complete
    
    source_video = finaldestination + "/" + edgeid + "_" + str(item_width) + "x" + str(item_height) + "x" + str(item_kbps) + "_assembled.mp4"
    logger.info("Adding Meta data to " + str(source_video))
    
    # Create Metadata
    quote = "\""
    title =  quote + clip_title + " " + edgeid + quote
    artist = quote + clip_star_name + quote
    composer = quote + "Edge Interactive" + quote
    album =  quote + clip_supporting_name + quote
    #proddate = quote + clip_productiondate + quote
    #release = quote + clip_releasedate + quote
    comment = quote + clip_keywords + quote
    genre = quote + "Adult"  + quote
    copyright_t = quote + "This production is produced 8/9/17 and copyright 2017 Edge Interactive Publishing Inc. All rights reserved. No right is granted for reproduction of these images other than for the personal use by the purchaser of this disk." + quote
    mydescription =  quote + clip_description + quote   
    show = quote + clip_shorttitle + quote
    episode_id = quote + edgeid + quote
    network =  quote + clip_licensor + quote
    keyword = quote + clip_shorttitle + quote
    actors = quote + clip_star_name + " and " + clip_supporting_name + quote
    advisory = "explicit"
    
    meta_video =  edgeid + "_" + str(item_width) + "x" + str(item_height) + "x" + str(item_kbps) + str(item_ext)
    
        
    CMD = ATOMICPARSLEY + " '" + source_video + "' --title=" + title + " --artist=" + artist + " --composer=" + composer + " --album=" + album 
    CMD = CMD + " --keyword=" + keyword + " --artist=" + actors +" --comment=" + comment + " --genre=" + genre + " --copyright=" + copyright_t + " --description=" + mydescription 

    if item_boxcover == "produce" or item_boxcover == "exists":
        CMD = CMD + " --TVShowName=" + show + " --TVEpisode=" + episode_id + " --TVNetwork=" + network + "–artwork '" + item_boxcover_img + "' --output '" + finaldestination + "/" + meta_video + "'"
    else:
        CMD = CMD + " --TVShowName=" + show + " --TVEpisode=" + episode_id + " --TVNetwork=" + network +  " --output '" + finaldestination + "/" + meta_video + "'"



    logger.warning("Metadata Command\n\t" + CMD)
    if noexec:
        metadata_result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        logger.warning("Running Command" )  
        metadata_result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)       
        logger.info( "Metadata" + item_src + "Started" )   
    
    # Phase 7 - Clean up / Thumbnails and Watermarks
    # Requires Capture to complete
    if item_capture:
        logger.info("Waiting for Capture to Complete so we can create thumbnails and watermarks if needed")
        stdoutdata, stderrdata = capture_result.communicate()
        capture_status = capture_result.returncode 
        if capture_status == 0:
            logger.info("\t\tCapture Completed, returned Status: " + str(capture_status))
        else:
            logger.error("\t\tCapture failed with Status:"+ str(capture_status))
            Error = True
 
    if capture_thumbnail == True:
        logger.info("Creating Thumbnails of captured images")
        CMD_TEMPLATE = "$MOGRIFY -resize $SIZE -background white -gravity center -extent $SIZE -format jpg -quality 75 -path $THUMBDIR ${CAPTURE}/*${EXT}"            
        CMD = Template(CMD_TEMPLATE).safe_substitute(MOGRIFY=MOGRIFY, SIZE=thumb_size, THUMBDIR=thumb_destination, CAPTURE=capture_destination, EXT=thumb_ext)
        logger.info("Thumbnail Command:\n\t" + CMD)
        if not noexec:
            thumbnail_result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logger.info("Check if Concat Completed")
            stdoutdata, stderrdata = thumbnail_result.communicate()
            thumbnail_status = thumbnail_result.returncode 
            if concat_status == 0:
                logger.info("\t\tThumbnail Completed, returned Status: " + str(thumbnail_status))
            else:
                logger.error("\t\tThumbnail failed, with Status:"+ str(thumbnail_status))
                Error = True
        else:
            concat_result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
    # Create Watermarked Images if requested       
    WorkResult = {} 
    if capture_watermark == True:
        for filename in os.listdir(capture_destination):
            if filename.endswith(".jpg"):
                logger.info("Image to Waterkark: " + str(filename))
                CMD = CONVERT +" '" + capture_destination + "/" + filename + "'  -background none -font " + str(water_font) + " -fill " + water_color + " -gravity " + water_location +" -pointsize " + str(water_font_size) +" -annotate 0 '" + str(watermark_text.encode('utf-8')) + "'" + " -flatten '" + water_destination +"/" + filename + "'"
                logger.info("Watermark Command:\n\t" + str(CMD))
                if noexec:
                    logger.warn("Not executing Command")
                else:
                    WorkResult[filename] = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)    
                
            
   
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