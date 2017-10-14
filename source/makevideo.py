'''
Created on Sep 30, 2017

@author: colin
'''

#===============================================================================
# Import 
#===============================================================================

import os
from string import Template
import subprocess
import logging
import description
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
        # Define Parameters
    video =  source + "/" +jobcard['video']['src']
    seconds = jobcard['capture']['frame_every']
    projectno = jobcard['clipinfo']['projectno']
    edgeid = jobcard['clipinfo']['edgeid']
    prime_dubya = jobcard['clipinfo']['prime_dubya']
    videoName = os.path.basename(video)
    pathName = os.path.dirname( source + "/" + video)
    destination = output + "/" + projectno + "/" +  prime_dubya +"/" + edgeid + "/" + jobcard[component]['out_dir']
    
    # Setup Codecs from Config File
    # To Deal with hardware based codecs later and machine differences.
    
    mp4_encoder = config['codec']['mp4_encode']
    mp4_decoder = config['codec']['mp4_decode']
    mp4_simple = config['codec']['mp4_simple']
        
    # Fix the title for any apostrophe
    
    title = jobcard['clipinfo']['title'] + " " + edgeid
    titlef = title.replace("'", "'\\\\\\\\\\\\\''")
    
    # Change spaces in short title to \n
    shorttitle = jobcard['clipinfo']['shorttitle']
    
    width = jobcard[component]['size_width']
    height = jobcard[component]['size_height']
    kbps = jobcard[component]['size_kbps'] 
    back_color = config['compliance']['preview_color']
    x = config['compliance']['preview_x']
    y = config['compliance']['preview_y']
    font_color = config['compliance']['preview_font_color']
    font_size = config['compliance']['preview_font_size']
    font = config['compliance']['compliance_font']
    
    
    
    if not os.path.isdir(destination ) and not noexec:
        os.makedirs(destination,0777)
        logger.info("Creating Directory: " + destination)
    
    Error = False
    FFMPEG=config['locations']['ffmpeg']
    # Make Preview
    
    logger.info("Creating Preview for " + component)
    
    CMD = FFMPEG + " -y -f lavfi -r 30 -i color=" + back_color +":"+ str(width) + "x" + str(height) + " -f lavfi -i anullsrc -filter_complex  "
    # Make Title Line
    CMD = CMD + "\"drawtext=enable='between(t,00,10)':fontfile=" + font + ":text=\'" + titlef +  "\':x=(w-text_w)/2" + ":y=" + str(y) +":fontcolor=" + font_color  + ":fontsize=" + str(font_size)
    # Sub Title
    CMD = CMD +  ",drawtext=enable='between(t,00,10)':fontfile=" + font + ":text=\'Starring " + "\':x=(w-text_w)/2" +":y=" + str(y+100) +":fontcolor=" + font_color + ":fontsize=" + str(font_size)
    
    CMD = CMD +  ",drawtext=enable='between(t,00,10)':fontfile=" + font + ":text=\'" + jobcard['clipinfo']['star'] + " and " + jobcard['clipinfo']['supporting'] + "\':x=(w-text_w)/2" +":y=" + str(y+200) +":fontcolor=" + font_color + ":fontsize=" + str(font_size)
    
    CMD = CMD +  ",drawtext=enable='between(t,00,10)':fontfile=" + font + ":text=\'IN " + "\':x=(w-text_w)/2" +":y=" + str(y+300) +":fontcolor=" + font_color + ":fontsize=" + str(font_size)
    
    # Keywords
    CMD = CMD +  ",drawtext=enable='between(t,00,10)':fontfile=" + font + ":text=\'" + shorttitle + "\':x=(w-text_w)/2:y=" + str(y+400) +":fontcolor=" + font_color + ":fontsize=" + str(font_size)
    
    CMD = CMD +  ",drawtext=enable='between(t,00,10)':fontfile=" + font + ":text=\'Release Date [" + jobcard['clipinfo']['releasedate'] + "]\':x=(w-text_w)/2:y=" + str(y+500) +":fontcolor=" + font_color + ":fontsize=" + str(font_size/2)
    CMD = CMD +  ",drawtext=enable='between(t,00,10)':fontfile=" + font + ":text=\'Production Date [" + jobcard['clipinfo']['productiondate'] + "]\':x=(w-text_w)/2:y=" + str(y+550) +":fontcolor=" + font_color + ":fontsize=" + str(font_size/2)

    # Wrap end of command
    CMD = CMD + "\" -c:v " + mp4_simple + " -b:v " + str(kbps) + "k -pix_fmt yuv420p -video_track_timescale 15360 -c:a aac -strict -2 -ar 48000 -ac 2 -sample_fmt fltp -t 12 '" + destination + "/" + edgeid + "_" + str(width) + "x" + str(height) + "x" + str(kbps) + "_" + "preview" + ".mp4'" 

    logger.warning("Preview Command for "+ component + "\n\t" + CMD)
    
    if not noexec:
        result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdoutdata, stderrdata = result.communicate()
        status = result.returncode 
        if status == 0:
            logger.info("\t\t Preview returned Status: " + str(status))
        else:
            logger.warning("\t\t Preview failed with Status:"+ str(status))
            Error = True

     # Make Compliance
     # Use the template for description but put it in the video directory.
     # Using video_text component
    back_color = config['compliance']['compliance_color']
    font_size = config['compliance']['compliance_text_size']
    font_color = config['compliance']['compliance_text_color']
    font_compliance = config['compliance']['compliance_font']
    
    description.produce(source, output, 'compliance_txt', jobcard, config, noexec)
    text_suffix = jobcard['compliance_txt']['suffix']
    
    CMD = FFMPEG + " -y -f lavfi -r 60 -i color=" + back_color + ":" +str(width) + "x" + str(height) + " -f lavfi -i anullsrc -vf drawtext=\"fontfile=" + font_compliance + ":fontcolor=" + font_color + ": fontsize=" + str(font_size) + ":textfile='" + destination +"/" + edgeid  + text_suffix +"'" + ":x=50:y=50,fade=t=in:st=00:d=2,fade=t=out:st=58:d=2\" -c:v mpeg4 -b:v " + str(kbps) + "k  -pix_fmt yuv420p -video_track_timescale 15360 -c:a aac -strict -2 -ar 48000 -ac 2 -sample_fmt fltp -t 60 '" + destination + "/" + edgeid + "_" + str(width) + "x" + str(height) + "x" + str(kbps) +  "_compliance.mp4'"

    logger.warning("Compliance Command\n\t" + CMD)
        
    if not noexec:
        result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdoutdata, stderrdata = result.communicate()
        status = result.returncode 
        if status == 0:
            logger.info("\t\t Compliance returned Status: " + str(status))
        else:
            logger.warning("\t\t Compliance failed with Status:"+ str(status))
            Error = True
    
    CMD = FFMPEG + " -y -i '" + video + "' -threads 8 -hide_banner -vf scale=" + str(width) + "x" + str(height) + " -c:v "+ mp4_encoder +" -b:v " + str(kbps) + "k -bufsize " + str(kbps*1000) +" -nal-hrd cbr -c:a aac -strict -2 '" + destination + "/" + edgeid + "_" + str(width) + "x" + str(height) + "x" + str(kbps) + "_transcoded.mp4'"

    logger.warning("Transcode Command\n\t" + CMD)
    if not noexec:
        result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdoutdata, stderrdata = result.communicate()
        status = result.returncode 
        if status == 0:
            logger.info("\t\t Compliance returned Status: " + str(status))
        else:
            logger.warning("\t\t Compliance failed with Status:"+ str(status))
            Error = True
    
    
    logger.info("Putting it all together PREVIEW + TRANSCODE + COMPLIANCE")
    
    CMD = FFMPEG + " -i '" + destination + "/" + edgeid + "_" + str(width) + "x" + str(height) + "x" + str(kbps) + "_preview.mp4'  -i '" + destination + "/" + edgeid + "_" + str(width) + "x" + str(height) + "x" + str(kbps) + "_transcoded.mp4' -i '"  + destination + "/" + edgeid + "_" + str(width) + "x" + str(height) + "x" + str(kbps)  + "_compliance.mp4' " 
    CMD = CMD + "-filter_complex 'concat=n=3:v=1:a=1'  -c:v " + mp4_encoder +" -b:v " + str(kbps) +"k -bufsize 1500000  -c:a aac -strict -2  -y '"   + destination + "/" + edgeid + "_" + str(width) + "x" + str(height) + "x" + str(kbps) + "_assembled.mp4'"
 
    logger.warning("Concat Command\n\t" + CMD)
    if not noexec:
        result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdoutdata, stderrdata = result.communicate()
        status = result.returncode 
        if status == 0:
            logger.info("\t\t Concat returned Status: " + str(status))
        else:
            logger.warning("\t\t Concat failed with Status:"+ str(status))
            Error = True
    
    logger.info("Adding Metadata to the Video and Re-transcoding")
    
    quote = "\""
    
    invideo = destination + "/" + edgeid + "_" + str(width) + "x" + str(height) + "x" + str(kbps) + "_assembled.mp4"
    
    title = quote + jobcard['clipinfo']['title'] + " " + edgeid + quote
    author = quote + jobcard['clipinfo']['star'] + quote
    composer = quote + "Edge Interactive" + quote
    album = quote + jobcard['clipinfo']['supporting'] + quote
    proddate = quote + jobcard['clipinfo']['productiondate'] + quote
    release = quote + jobcard['clipinfo']['releasedate'] + quote
    comment = quote + jobcard['clipinfo']['keywords'] + quote
    genre = quote + "Adult"  + quote
    copyright_t = quote + "This production is produced 8/9/17 and copyright 2017 Edge Interactive Publishing Inc. All rights reserved. No right is granted for reproduction of these images other than for the personal use by the purchaser of this disk." + quote
    mydescription = quote +  jobcard['clipinfo']['description'] + quote
    synopsis = quote + jobcard['clipinfo']['description'] + quote
    show = quote + jobcard['clipinfo']['shorttitle'] + quote
    episode_id = quote + edgeid + quote
    network = quote + jobcard['clipinfo']['licensor'] + quote
    track = quote + jobcard['clipinfo']['shorttitle'] + quote
    actors = quote + jobcard['clipinfo']['star'] + " and " + jobcard['clipinfo']['supporting'] + quote
    outvideo = edgeid + "_" + str(width) + "x" + str(height) + "x" + str(kbps) + ".mp4"
    
    CMD = FFMPEG + " -i '" + invideo + "' -metadata title=" + title + " -metadata author=" + author + " -metadata composer=" + composer + " -metadata album=" + album + " -metadata date=" + proddate + " -metadata purchase_date=" + release
    CMD = CMD + " -metadata track=" + track + " -metadata artist=" + actors +" -metadata comment=" + comment + " -metadata genre=" + genre + " -metadata copyright=" + copyright_t + " -metadata description=" + mydescription + " -metadata synopsis=" + synopsis
    CMD = CMD + " -metadata show=" + show + " -metadata episode_id=" + episode_id + " -metadata network=" + network + " -metadata media_type=9 -y -c:v "+ mp4_encoder +" -b:v " + str(kbps) +"k '" + destination + "/" + outvideo + "'"

    logger.warning("Metadata Command\n\t" + CMD)
    if not noexec:
        result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdoutdata, stderrdata = result.communicate()
        status = result.returncode 
        if status == 0:
            logger.info("\t\t Compliance returned Status: " + str(status))
        else:
            logger.warning("\t\t Compliance failed with Status:"+ str(status))
            Error = True
    
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