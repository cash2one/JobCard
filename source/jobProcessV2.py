#!/usr/bin/python

#Import Libraries
import yaml
import subprocess
import sys
import os
import time
import argparse
import json
import shlex
import datetime
import shutil


# Parse the Command Line

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true", help="Display detailed debugging information")
group.add_argument("-q", "--quiet", action="store_true")
parser.add_argument("-j", "--jobcard", action="store", help="jobcard.yml file to process")
parser.add_argument("-l","--logfile", action="store", help="Write Logfile if ommitted write to STDOUT")
parser.add_argument("-c","--configfile", default="config.yml", help="use config file, default is config.yml in working dir")
parser.add_argument("-n","--noexec", action="store_true", help="Do not run commands on the OS; echo the command on the OS only" )
args = parser.parse_args()
print args




# Check for minimum requirements
if args.jobcard == None:
    print "Please provide a valid Job card: this is required"
    print parser.parse_args(['-h'])
    exit(1)
    
# If logfile is found open for writing

if args.logfile != None:
    print "Opening Log file: " + args.configfile
    log = open(args.logfile, 'w')        
else:
    print "Logging disabled"    

def logger(message):
        myTime = datetime.datetime.now()
        if args.logfile != None:
            log.write(str(myTime) + "-> " + message + "\n")
        else:
            print str(myTime) + "-> " + str(message)
            

# Check Job card is really there
if os.path.isfile(args.jobcard):
    logger("Job Card Exists: " + args.jobcard)
    job = open(args.jobcard,'r')
    jobcard = yaml.load(job)
else:
    logger("Job card invalid")
    exit(2)


    
#Open Config File

if os.path.isfile(args.configfile):
    logger("Config file exists")
    cfg = open(args.configfile,'r')
    config = yaml.load(cfg)
else:
    logger("Missing Config File")
    exit(2)

# Set Global short cuts
# Set Global Configuration Values

CURL=config['locations']['curl']
CONVERT=config['locations']['convert']
FFMPEG=config['locations']['ffmpeg']
FFPROBE=config['locations']['ffprobe']
FONT=config['boxcover']['font']

#Validate global short cuts exists
if not os.path.isfile(CURL):
    logger("Curl is missing:" + str(CURL))
    exit(3)
if not os.path.isfile(CURL):
    logger("Convert is missing:" + str(CONVERT))
    exit(3)
if not os.path.isfile(FFMPEG):
    logger("ffmpeg is missing:" + str(FFMPEG))
    exit(3) 
if not os.path.isfile(FFPROBE):
    logger("ffprobe is missing:" + str(FFPROBE))
    exit(3)
if not os.path.isfile(FONT):
    logger("Font is missing:" + str(FONT))
    exit(3)      
    

    
#===================================================================#
#                Global Variables                                   #
#===================================================================#
edgeid = jobcard['clipinfo']['edgeid']
Finish = config['default']['finish']
Source = config['default']['source']
Assembly = config['default']['assembly']
Deliveries = config['default']['deliveries']
Project = jobcard['clipinfo']['projectno']
JobMatrix = {}
PartMatrix = {}
ErrorMatrix = {}


#===================================================================#
# Functions                                                         #
#===================================================================#

def makeDirectories(name):
    # Check does the destination exist
    if args.verbose:
        logger("Make Directories function start")
        logger("Create Directory: " + name)
    
    if os.path.isdir(str(name)):
            logger("Destination Directory Exists:" + str(name))
            status = True
    else:
        # Try to create recursively
        if args.noexec:
            if args.verbose:
                logger("Creating Directory: " + str(name))
        else:    
            dir = os.makedirs(str(name),0777)
        status = True
    return status

def getVideoSize(video):
    CMD= FFPROBE + " -v error -of flat=s=_ -select_streams v:0 -show_entries stream=height,width,bit_rate,duration '" + video + "'"
    videoName = os.path.basename(video)
    pathName = os.path.dirname( Source + "/" + video)
    
    if args.verbose:
        logger("Get the Video Size Information for Video: " + videoName)
        logger('Source Dir:' + pathName)
        logger("getVideoSizeCMD:\n  " + CMD)
    

    pCMD = shlex.split(CMD)
    
    if args.noexec:
        result=subprocess.check_output("echo")
        sizeofVideo="1920x1080"
        Duration="60"
        BitRate="1500000"
    else:    
        result=subprocess.check_output(pCMD)
        cWidth = result.splitlines(True)[0]
        cHeight = result.splitlines(True)[1]
        cDuration = result.splitlines(True)[2]
        cBit_Rate = result.splitlines(True)[3]
        lWidth = cWidth.split("=")[1]
        lHeight = cHeight.split("=")[1]
        lDuration = cDuration.split("=")[1]
        lBitRate = cBit_Rate.split("=")[1]
        Width = lWidth.replace('\n','')
        Height = lHeight.replace('\n','')
        Duration = lDuration.replace('\n','')
        BitRate = lBitRate.replace('\n','')
        Duration = Duration.replace('"','')
        BitRate = BitRate.replace('"','')
        sizeofVideo =  str(Width) + "x" + str(Height)  
        
    logger("Video Source: Size: " + sizeofVideo + " Duration:" + Duration + " BitRate:" + BitRate + " bs" )
 
    return(sizeofVideo,Duration,BitRate)

def CAPTURE(component,jobflag):
    # Define Parameters
    video =  Source + "/" +jobcard['video']['source_video']
    seconds = jobcard['capture']['frame_every']
    destination = Assembly + "/" + Project + "/" + edgeid + "/" + jobcard['capture']['out_dir']
    videoName = os.path.basename(video)
    pathName = os.path.dirname( Source + "/" + video)
        
    if args.verbose:
        logger("Make Stills for Video: " + videoName)
        logger('Source Dir:' + pathName)
        logger("Put Stills in Destination:\n  " + destination)
    
    makeDirectories(destination)
    
    # Get video Size
    SizeOfVideo, Duration, Bitrate = getVideoSize( video )
             
   
    CMD = FFMPEG + " -c:v h264_vda -i '"  + video + "' -thread_type slice -hide_banner -vf fps=1/" + str(seconds) + "  -c:v mjpeg '" + destination + "/" + edgeid + "_" + SizeOfVideo + "_capture_%03d.jpg'" 
    
    if args.verbose:   
       logger("StillCommand:\n  " + CMD)
    
    if args.noexec:
        logger("No Execute")
        result=subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        logger("Running Command")   
        result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    
    if args.verbose: 
        logger("Capture on " + videoName + " Completed")    
    return(result)

def makeBoxCover(component,jobflag):
    image=jobcard['box_cover']['cover']
    title=jobcard['clipinfo']['title']
    star=jobcard['clipinfo']['star']
    supporting = jobcard['clipinfo']['supporting']
    keywords = jobcard['clipinfo']['shorttitle']
    EdgeID=edgeid
    title_size=config['boxcover']['title_size']
    star_size= config['boxcover']['star_size']
    support_size= config['boxcover']['support_size']
    keyword_size= config['boxcover']['keyword_size']
    EdgeID_size= config['boxcover']['partno_size']
    FONT = config['boxcover']['font']
    alignment= jobcard['box_cover']['alignment']
    color= config['boxcover']['font_color']
    destination = Assembly + "/" + Project + "/" + edgeid + "/" + jobcard['box_cover']['out_dir']
    sourcedir =  config['default']['source']
    makeDirectories(destination)
      
    if args.verbose:
            logger( "Title:" + str(title) + " : size " + str(title_size))
            logger( "Star:" +  str(star) + " : size " + str(star_size))
            logger( "Supporting:" +  str(supporting) + " : size " + str(support_size))
            logger( "Keywords:" +  str(keywords) + " : size " + str(keyword_size))
            logger( "Part Num:" +  str(EdgeID) + " : size " + str(EdgeID_size))
            logger( "Title Alignment:" + str(alignment))
            logger( "Text Color:" + str(color))
            logger( "Font:" + str(FONT))
   
# Adjust for Job Flag
    # Case 1 -- exists
    if jobflag == 'exists':
        # Copy the file
        
        #Get end filename:
        filename = os.path.basename(image)
        
        
        CMD = "convert '" + Source + "/" + image + "' -resize " + str(config['boxcover']['box_width']) + "x" + str(config['boxcover']['box_height']) + " -set filename:mysize '%wx%h' " + edgeid + "_cover'_%[filename:mysize].jpg'"
        
        if args.noexec:
            logger("     Copy Box Cover " +Source + "/" + image + " ==> " + edgeid + "_box_cover.jpg")
            logger("Copy and Resize Image " + image)
            logger("ConvertCMD \n  " + CMD)
            result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
            
        
    elif jobflag == 'produce':
        # Run the production
            ### Note We need Error Checking in here too
        logger("    Create Box Cover")
        if alignment == 'left':
            gravity='Northwest'
        if alignment == 'center':
            gravity = 'North'
        if alignment == 'right':
            gravity='NorthEast'        
        
        #Make keywords split by line
        
        keywords_f = keywords.replace(" ","\\n")
        title_f = title.replace("'","\\'")
        
        BoxCoverCommand = CONVERT + " -verbose -size " + str(config['boxcover']['box_width']) + "x" + str(config['boxcover']['box_height']) + " -font " + str(FONT) + " -pointsize " + str(title_size)
        BoxCoverCommand = BoxCoverCommand + " -fill " + str(color) + " \( \( -gravity " + gravity + " -background transparent -pointsize  " + str(title_size) + "  label:\"" + title_f +"\"" + " -pointsize " + str(star_size)
        BoxCoverCommand = BoxCoverCommand + " -annotate +0+250 '" + str(star) + "'" + " -pointsize " + str(support_size) + " -annotate +0+450 '" +  str(supporting) + "' -splice 0x18 \)"
        BoxCoverCommand = BoxCoverCommand + " \( +clone -background black -shadow 20x-9+0+0 \) -background transparent +swap -layers merge +repage \)  \( \( -gravity West -background transparent -pointsize " 
        BoxCoverCommand = BoxCoverCommand + str(keyword_size) + " label:'" + str(keywords_f) + "'  -splice 50x0 \)  \( +clone -background black -shadow 20x-9+0+0 \) -background transparent +swap -layers merge +repage \) \( -gravity SouthWest "+ " -pointsize " +str(EdgeID_size) + " -background transparent label:"
        BoxCoverCommand = BoxCoverCommand + str(EdgeID) +" -splice 100x0 \) " + "  \( \( -gravity SouthEast -background transparent label:'EDGE   \n' -splice 0x18  -pointsize 50  -annotate +50+192 '  _____________________   ' -splice 0x18 -pointsize 100 -annotate +50+120 'interactive  '   \) "
        BoxCoverCommand = BoxCoverCommand + " \( +clone -background black -shadow 60x18+0+0 \) -background transparent +swap -layers merge +repage \) \(  -label 'image' -background transparent -mosaic label:blank "
        BoxCoverCommand = BoxCoverCommand + "'" +str(sourcedir) + "/" + str(image) + "' \) \(  -clone 0--1 -mosaic  \) -trim -reverse '" + str(destination) + "/" + str(EdgeID) + str(config['boxcover']['suffix']) + ".psd'; " + CONVERT + " -flatten '" + destination + "/" + EdgeID + config['boxcover']['suffix'] + ".psd' '" + destination + "/" +EdgeID + config['boxcover']['suffix'] +".jpg'"
        
        if args.verbose:
            logger("    makeBoxCommand:\n" + BoxCoverCommand )
        
        if args.noexec:
            result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:    
            result = subprocess.Popen( BoxCoverCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    
    else:
            #Ignore
            logger("     Do Nothing: Box Cover")
            result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)    
    
    # Run Command in background
    if args.verbose: 
        logger("Box Cover Create on " + image + " Completed")   
    return(result) 

def makeVideoInfo(component,jobflag):
    video =  Source + "/" +jobcard['video']['source_video']
    destination = Assembly + "/" + Project + "/" + edgeid + "/" + jobcard['videoinfo']['out_dir']
    videoName = os.path.basename(video)
    pathName = os.path.dirname( Source + "/" + video)
    
    for format in ['csv', 'json', 'xml']:
        if args.verbose:
            logger("Output Video Information in " + format )
            logger("Output Location:\n" + pathName)
        
        probeCommand = FFPROBE + " -v error -show_format -show_streams -print_format " + format + " '" +  video + "' > '" + destination +"/" + edgeid + "-info" +"."+ format +"'"
        if args.verbose:
            logger("MakeVideoInfo:\n" + probeCommand)
        if args.noexec:
            result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
        else:    
            result = subprocess.Popen(probeCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    logger("MakeVideoInfo:" + videoName + " Completed")
    return(result)

def makePromoImg(component,jobflag):
    if not (jobflag == 'produce' or jobflag == 'exists'):
        if args.verbose:
            logger("Make Promo Image: Ignoring")
        result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  
        return(result)
    else:
        destination = Assembly + "/" + Project + "/" + edgeid + "/" + jobcard[component]['out_dir']
        makeDirectories(destination)  
        count = 0
    # If Produce
        if jobflag == 'produce':
            logger("Produce")
            sourcedir = Source + "/"  + jobcard['promoimg']['dir']
            if args.verbose:
                logger("makePromoIMG: Produce")
            if not os.path.isdir(sourcedir):
                if args.verbose:
                    logger("makePromoIMG: Directory does not exist: " + sourcedir)
                    ErrorMatrix['makePromoIMG'] = "directory " + sourcedir + " does not exist"
                    result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  
                    return(result)             
                
            for filename in os.listdir(sourcedir):
                if filename.endswith(".tif") or filename.endswith(".jpg"): 
                    CMD =  CONVERT + " '" + sourcedir + "/" + filename + "' -resize " + str(config['promoimg']['promo_width']) + "x" + str(config['promoimg']['promo_height']) + " -set filename:mysize '%wx%h' '" + destination + "/" +  edgeid + "_promo_%[filename:mysize]_"+ str(count).zfill(3) + ".jpg'" 
                    if args.verbose:
                        logger("makePromoIMG CMD:\n  " + CMD)
                    if not args.noexec:
                        result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
                    count = count + 1    
                else:
                    logger("Ignoring file:" +filename)    
        else:
           # If exsists
            logger("Exists")
            sourcedir = Finish + "/"  + jobcard['promoimg']['dir']
            if args.verbose:
                logger("makePromoIMG: Exists")
            if not os.path.isdir(sourcedir):
                if args.verbose:
                    logger("makePromoIMG: Directory does not exist: " + sourcedir)
                    ErrorMatrix['makePromoIMG'] = "directory " + sourcedir + " does not exist"
                    result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  
                    return(result)             
                
            for filename in os.listdir(sourcedir):
                if filename.endswith(".tif") or filename.endswith(".jpg"): 
                    CMD = CONVERT + " '" + sourcedir + "/" + filename + "'  -set filename:mysize '%wx%h' '" + destination + "/" + edgeid + "_promo_%[filename:mysize]_"+ str(count).zfill(3) + ".jpg'"                    
                    if args.verbose:
                        logger("makePromoIMG CMD:\n  " + CMD)
                    if not args.noexec:
                        result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    count = count + 1       
                else:
                    logger("Ignoring file:" +filename)  
    
    result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  
    return(result)
                    
def makePhotoSet(component,jobflag):
    if not (jobflag == 'produce' or jobflag == 'exists'):
        if args.verbose:
            logger("Make Photo set: Ignoring")
        result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  
        return(result)
    else:
    
    # If Produce
        if jobflag == 'produce':
            destination = Assembly + "/" + Project + "/" + edgeid + "/" + jobcard[component]['out_dir']
            sourcedir = Source + "/" + jobcard[component]['dir']
            if args.verbose:
                logger("makePhotoSet: Produce")
            if not os.path.isdir(sourcedir):
                if args.verbose:
                    logger("Make Photo set: Directory does not exist: " + sourcedir)
                    ErrorMatrix['makePhotoSet'] = "directory " + sourcedir + " does not exist"
                    result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  
                    return(result) 
                
            makeDirectories(destination)
            count = 0
            for filename in os.listdir(sourcedir):
                if filename.endswith(".tif") or filename.endswith(".jpg"): 
                    if args.verbose:
                        logger("copying file " + filename + " to " + destination) 
                    CMD = CONVERT +" '" + sourcedir + "/" + filename + "' -resize " + str(jobcard[component]['set_width']) + "x" + str(jobcard[component]['set_height']) + " -set filename:mysize '%wx%h' '" + destination + "/" + edgeid + "_%[filename:mysize]_"+ str(count).zfill(3) + ".jpg'" 
                    if args.verbose:
                        logger("makePhotoSetCMD\n  " + CMD )
                    if not args.noexec:    
                        result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    count = count + 1    
                else:
                    if args.verbose:
                        logger("ignoring file " + filename )
        else:
            # Exists
            destination = Assembly + "/" + Project + "/" + edgeid + "/" + jobcard[component]['out_dir']
            sourcedir = Finish + "/" + jobcard[component]['dir']
            if args.verbose:
                logger("makePhotoSet: Exists")
            if not os.path.isdir(sourcedir):
                if args.verbose:
                    logger("Make Photo set: Directory does not exist: " + sourcedir)
                    ErrorMatrix['makePhotoSet'] = "directory " + sourcedir + " does not exist"
                    result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  
                    return(result) 
                
            makeDirectories(destination)
            count = 0
            for filename in os.listdir(sourcedir):
                if filename.endswith(".tif") or filename.endswith(".jpg"): 
                    if args.verbose:
                        logger("copying file " + filename + " to " + destination )
                    CMD = CONVERT + " '" + sourcedir + "/" + filename + "' -resize " + str(jobcard[component]['set_width']) + "x" + str(jobcard[component]['set_height']) + "  '" + destination + "/" + edgeid + "_" +str(jobcard[component]['set_width']) + "x" + str(jobcard[component]['set_height']) +"_" + str(count).zfill(3) + ".jpg'" 
                    if args.verbose:
                        logger("makePhotoSetCMD\n  " + CMD)
                    if not args.noexec:
                        result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                    count = count + 1    
                else:
                    if args.verbose:
                        logger("ignoring file " + filename )
    
    result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)    
    return(result)

def PREVIEW(component, jobflag):
    video =  Source + "/" +jobcard['video']['source_video'] 
    destination = Assembly + "/" + jobcard['clipinfo']['projectno']  + "/" + edgeid + "/" + jobcard[component]['out_dir']
    width = jobcard[component]['size_width']
    height = jobcard[component]['size_height']
    kbps = jobcard[component]['size_kbps'] * 1000
    back_color = config['compliance']['preview_color']
    x = config['compliance']['preview_x']
    y = config['compliance']['preview_y']
    font_color = config['compliance']['preview_font_color']
    font_size = config['compliance']['preview_font_size']
    font = config['compliance']['compliance_font']
    
    makeDirectories(destination)
    
    # Fix the title for any apostrophe
    
    title = jobcard['clipinfo']['title'] + " " + edgeid
    titlef = title.replace("'", "'\\\\\\\\\\\\\''")
    
    # Change spaces in short title to \n
    shorttitle = jobcard['clipinfo']['shorttitle']
    
    
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
    
    # Wrap end of command
    CMD = CMD + "\" -c:v mpeg4 -b:v " + str(kbps) + " -pix_fmt yuv420p -video_track_timescale 15360 -c:a aac -ar 48000 -ac 2 -sample_fmt fltp -t 12 '" + destination + "/" + edgeid + "_" + str(width) + "x" + str(height) + "_" + "preview" + ".mp4'" 
    
   
    if args.verbose: 
        logger("  PreviewCommand:\n  " + CMD)
    if args.noexec:
        results = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:    
        results = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    return (results) ;
    
def makeComplianceTrailer(outdir,kbps,width,height):
    #Make short variables to make life easier
    
    template = config['compliance']['template']
    back_color = config['compliance']['compliance_color']
    font_size = config['compliance']['compliance_text_size']
    font_color = config['compliance']['compliance_text_color']
    font_compliance = config['compliance']['compliance_font']
    
    compliance_template = open(template,"r")
    compliance_file = open (outdir + "/" + edgeid + "_" + "compliance.txt","w")
    compliance_file.write(jobcard['clipinfo']['title'] + " - " + jobcard['clipinfo']['edgeid'] + "\n\n")
    compliance_file.write("Edge ID: " + jobcard['clipinfo']['edgeid']+ "\n\n")
    compliance_file.write("Starring: " + jobcard['clipinfo']['star']+ "\n\n")
    compliance_file.write("Supporting cast: " + jobcard['clipinfo']['supporting']+ "\n\n")
    compliance_file.write("Keywords: " + jobcard['clipinfo']['keywords']+ "\n\n")
    compliance_file.write("Production Date: " + jobcard['clipinfo']['productiondate']+ "\n\n")
    compliance_file.write("Licensor: " + jobcard['clipinfo']['licensor']+ "\n\n")
    compliance_file.write("\n\n\n")
 
    for line in compliance_template:
         compliance_file.write(line)
    
    compliance_file.close()
    compliance_template.close()
 
    complianceCommand = FFMPEG + " -y -f lavfi -r 30 -i color=" + back_color + ":" +str(width) + "x" + str(height) + " -f lavfi -i anullsrc -vf drawtext=\"fontfile=" + font_compliance + ":fontcolor=" + font_color + ": fontsize=" + str(font_size) + ":textfile='" + outdir +"/" + edgeid  +  "_" + "compliance.txt'" + ":x=50:y=50,fade=t=in:st=00:d=2,fade=t=out:st=28:d=2\" -c:v mpeg4 -b:v " + str(kbps) + "  -pix_fmt yuv420p -video_track_timescale 15360 -c:a aac -ar 48000 -ac 2 -sample_fmt fltp -t 30 '" + outdir + "/" + edgeid + "_" + str(width) + "x" + str(height) +  "_compliance.mp4'"
    if args.verbose: 
        logger("  ComplianceCommand:\n  " +  complianceCommand )
        
    if args.noexec:
        ComplianceOutput = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:    
        ComplianceOutput = subprocess.Popen(complianceCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 

    return(ComplianceOutput);

def makeTranscode(video, EdgeID,destination, width, height, kbps):
    
    transcodeCommand = FFMPEG + " -y -i '" + video + "' -threads 8 -hide_banner -vf scale=" + str(width) + "x" + str(height) + " -c:v h264_videotoolbox -b:v " + str(kbps) + "k -bufsize " + str(kbps*1000) +" -nal-hrd cbr -c:a aac -strict -2 '" + destination + "/" + EdgeID + "_" + str(width) + "x" + str(height) + "x" + str(kbps) + ".mp4'"
    if args.verbose: 
        logger("  TranscodeCommand:\n  " + transcodeCommand)
    
    if args.noexec:
        transcodeOutput = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:    
        transcodeOutput = subprocess.Popen(transcodeCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    
    
    return(transcodeOutput);

def makeConcatVideo(component,jobflag):
    
    destination = Assembly + "/" + jobcard['clipinfo']['projectno']  + "/" + edgeid + "/" + jobcard[component]['out_dir'] 
    width = jobcard[component]['size_width']
    height = jobcard[component]['size_height']
    kbps = jobcard[component]['size_kbps'] 
    
    
    CMD = FFMPEG + " -i '" + destination + "/" + edgeid + "_" + str(width) + "x" + str(height) + "_preview.mp4'  -i '" + destination + "/" + edgeid + "_" + str(width) + "x" + str(height) + "x" + str(kbps) + ".mp4' -i '"  + destination + "/" + edgeid + "_" + str(width) + "x" + str(height)  + "_compliance.mp4' " 
    CMD = CMD + "-filter_complex 'concat=n=3:v=1:a=1'  -c:v h264_videotoolbox -b:v " + str(kbps) +"k -bufsize 1500000 -nal-hrd cbr -c:a aac -strict -2 '"   + destination + "/" + edgeid + "_" + str(width) + "x" + str(height) + "x" + str(kbps) + "_finished.mp4'"
    
    if args.verbose: 
        logger("  ConcatCommand:\n  " + CMD)
    
    if args.noexec:
        results = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:    
        results = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    
    
    return(results)

def makeVideo(component,jobflag):
    # component is component1 or component2
    video =  Source + "/" +jobcard['video']['source_video'] 
    destination = Assembly + "/" + jobcard['clipinfo']['projectno']  + "/" + edgeid + "/" + jobcard[component]['out_dir']
    width = jobcard[component]['size_width']
    height = jobcard[component]['size_height']
    kbps = jobcard[component]['size_kbps'] * 1000
    makeDirectories(destination)
    outdir = destination
    PartMatrix ={}
    
    if args.verbose:
        logger( "Make Video:")
        logger( "Video:" + video )
        logger("Output Dir=" + str(outdir)  )
        logger("Output Width=" +   str(width) + " Output Height=" + str(height) + " Output Kbps=" + str(kbps) )
    
    # Make Preview
    
    PartMatrix['preview'] = PREVIEW(component,jobflag)
    # Make Compliance
    
    PartMatrix['compliance'] = makeComplianceTrailer(outdir,kbps,jobcard[component]['size_width'], jobcard[component]['size_height'])
    
    # Make Transcode
    # Verify that preview and complaiance have finished.
    
    if args.verbose:
        logger("  Verify that preview and compliance have finished")
     
     # Verify Preview
    stdoutdata, stderrdata = PartMatrix['preview'].communicate()
    PartStatus = PartMatrix['preview'].returncode   
    
    if args.verbose:
        logger("  Preview Completed with return code " + str(PartStatus))
    
    #Verify Compliance
    stdoutdata, stderrdata = PartMatrix['compliance'].communicate()
    PartStatus = PartMatrix['compliance'].returncode   
    
    if args.verbose:
        logger("  compliance Completed with return code " + str(PartStatus))    
        
    # Later make sure return code is "0"
    
    PartMatrix['transcode']  = makeTranscode(video, edgeid , outdir, jobcard[component]['size_width'], jobcard[component]['size_height'], jobcard[component]['size_kbps'])
    
    # Verify parts are build in correct order (preview, compliance, transcode, concat)
    #Verify Transcode Finishes first
    stdoutdata, stderrdata = PartMatrix['transcode'].communicate()
    PartStatus = PartMatrix['transcode'].returncode 
    if args.verbose:
        logger("  Transcode Completed with return code " + str(PartStatus))    
 
    
    # Start Concat
    PartMatrix['concat'] = makeConcatVideo(component,jobflag)


    #Verify Concat Completes before next process starts
    stdoutdata, stderrdata = PartMatrix['concat'].communicate()
    PartStatus = PartMatrix['concat'].returncode 
    if args.verbose:
        logger("  Concat Completed with return code " + str(PartStatus))    
    
    
    
    result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    return(result)

def writeMP4Metadata(video):
    destination = Assembly + "/" + jobcard['clipinfo']['projectno'] + "/" + edgeid + "/" + jobcard[component]['out_dir']
    outvideo = "test.mp4"
    quote = "\""
    title = quote + jobcard['clipinfo']['title'] + " " + edgeid + quote
    author = quote + jobcard['clipinfo']['star'] + quote
    composer = quote + "Edge Interactive" + quote
    album = quote + jobcard['clipinfo']['supporting'] + quote
    year = quote + jobcard['clipinfo']['productiondate'] + quote
    comment = quote + "Release Date" + jobcard['clipinfo']['releasedate'] + quote
    genre = quote + "Adult" + jobcard['clipinfo']['shorttitle'] + quote
    copyright = quote + jobcard['clipinfo']['productiondate'] + quote
    description = quote +  jobcard['clipinfo']['description'] + quote
    synopsis = quote + jobcard['clipinfo']['description'] + quote
    show = quote + jobcard['clipinfo']['shorttitle'] + quote
    episode_id = quote + edgeid + quote
    network = quote + jobcard['clipinfo']['licensor'] + quote
    track = quote + jobcard['clipinfo']['shorttitle'] + quote
    
    logger("Writing MP4 metadata")
    CMD = FFMPEG + " -i '" + destination + "/" + video + "' -metadata title=" + title + " -metadata author=" + author + "-metadata composer=" + composer + " -metadata album=" + album + " -metadata year=" + year
    CMD = CMD + " -metadata track=" + track + " -metadata comment=" + comment + " -metadata genre=" + genre + " -metadata copyright=" + copyright + " -metadata description=" + description + " -metadata synopsis=" + synopsis
    CMD = CMD + " -metadata show=" + show + " -metadata episode_id=" + episode_id + " -metadata network=" + network + " -y '" + destination + "/" + outvideo + "'"
    
    if args.verbose: 
        logger("  ComplianceCommand:\n  " +  CMD )
    if args.noexec:
        result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:    
        result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)     
    return


#===================================================================#
#                Main Code                                          #
#===================================================================#
for product in jobcard['product']:
    logger("Producing Product: " + str(product) )
    
logger("Start Processing Job Card for:" + edgeid)

products = ['capture','box_cover','videoinfo','promoimg','photoset1','video1','video2' ]
product = ['video2']

for component in product:  
    JobFlag = jobcard['component'][component]
    JobFlag = JobFlag.lower()
    component = component.lower()
    logger("Component:" + str(component) + "=>" + JobFlag )
    
    #Use the function defined in the Job Card
    action = config['functions'][component]
    if args.verbose:
        logger("Processing Component:" + str(component))
    method = eval(action)
    JobMatrix[component] = method(component, JobFlag)


print "==============================================="
print "Error Matrix"    
print ErrorMatrix    
     
