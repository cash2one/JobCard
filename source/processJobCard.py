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
    
for product in jobcard['product']:
    logger("Producing :" + str(product) )
    

    
#===================================================================#
# Functions                                                         #
#===================================================================#
def makeDirectories(name):
    # Check does the destination exist
    if args.verbose:
        logger("Make Directories function start")
    
    if os.path.isdir(str(name)):
        if args.verbose:
            logger("Destination Directory Exists:" + str(name))
        status = True
    else:
        # Try to create recursively
        dir = os.makedirs(str(name),0777)
        status = True
    return status

def getVideoSize(video):
    #getSizeCMD="eval $('"+ FFPROBE +" -v error -of flat=s=_ -select_streams v:0 -show_entries stream=height,width '" + video + "' ' ); size=${streams_stream_0_width}x${streams_stream_0_height}; echo $size"  
    getSizeCMD= FFPROBE + " -v error -of flat=s=_ -select_streams v:0 -show_entries stream=height,width,bit_rate,duration '" + video + "'"
    if args.verbose:  
        logger("GetVideoSize" + getSizeCMD)
    pCMD = shlex.split(getSizeCMD)
    
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
        if args.verbose:   
            logger("Video Source: Size: " + sizeofVideo + " Duration:" + Duration + " BitRate:" + BitRate + " bs" )
 
    return(sizeofVideo,Duration,BitRate)

def CAPTURE(component,jobflag):
    # Define Parameters
    video =  Source + "/" +jobcard['video']['source_video']
    seconds = jobcard['capture']['frame_every']
    destination = Finish + "/" + Project + "/" + edgeid + "/" + jobcard['capture']['out_dir']
    makeDirectories(destination)
    
    # Get video Size
    SizeOfVideo, Duration, Bitrate = getVideoSize( video )
             
   
    stillCommand = FFMPEG + " -i '"  + video + "' -thread_type slice -hide_banner -vf fps=1/" + str(seconds) + " '" + destination + "/" + edgeid + "_" + SizeOfVideo + "_capture_%03d.jpg'" 
    
    if args.verbose:   
       logger("StillCommand" + stillCommand)
    
    if args.noexec:
        stillCommandOutput=subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:   
        stillCommandOutput = subprocess.Popen(stillCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
        
    return(stillCommandOutput)
    
def PREVIEW(EdgeID, destination, x, y, width, height, back_color, font_size, font_color, font):
    
    # Fix the title for any apostrophe
    
    title = jobcard['clipinfo']['title']
    title_f = title.replace("'", "'\\\\\\\\\\\\\''")
    
    previewCommand = FFMPEG + " -y -f lavfi -r 30 -i color=" + back_color +":"+ str(width) + "x" + str(height) + " -f lavfi -i anullsrc -filter_complex  "
    # Make Title Line
    previewCommand = previewCommand + "\"drawtext=enable='between(t,00,10)':fontfile=" + font + ":text=\'" + title_f + " " + EdgeID + "\':x=" + str(x) + ":y=" + str(y) +":fontcolor=" + font_color  + ":fontsize=" + str(font_size)
    # Sub Title
    previewCommand = previewCommand + ",drawtext=enable='between(t,00,10)':fontfile=" + font + ":text=\'Starring " +  jobcard['clipinfo']['star'] + "\':x=" + str(x) + ":y=" + str(y+100) +":fontcolor=" + font_color + ":fontsize=" + str(font_size)
    # Keywords
    previewCommand = previewCommand + ",drawtext=enable='between(t,00,10)'    :fontfile=" + font + ":text=\'in " + jobcard['clipinfo']['keywords'] + "\':x=" + str(x) + ":y=" + str(y+200) +":fontcolor=" + font_color + ":fontsize=" + str(font_size)
    # Wrap end of command
    previewCommand = previewCommand + "\" -c:v libx264 -b:v 1000k -pix_fmt yuv420p -video_track_timescale 15360 -c:a aac -ar 48000 -ac 2 -sample_fmt fltp -t 12 '" + destination + "/" + EdgeID + "_" + str(width) + "x" + str(height) + "_" + "preview" + ".mp4'" 
    
   
    if args.verbose: 
        logger("PreviewCommand:" + previewCommand)
    if args.noexec:
        previewOutput = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:    
        previewOutput = subprocess.Popen(previewCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    return (previewOutput) ;
    
def makeComplianceTrailer(outdir,width,height):
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
    compliance_file.write("Production Date: " + jobcard['clipinfo']['ProductionDate']+ "\n\n")
    compliance_file.write("Licensor: " + jobcard['clipinfo']['Licensor']+ "\n\n")
    compliance_file.write("\n\n\n")
 
    for line in compliance_template:
         compliance_file.write(line)
    
    compliance_file.close()
    compliance_template.close()
 
    complianceCommand = FFMPEG + " -y -f lavfi -r 30 -i color=" + back_color + ":" +str(width) + "x" + str(height) + " -f lavfi -i anullsrc -vf drawtext=\"fontfile=" + font_compliance + ":fontcolor=" + font_color + ": fontsize=" + str(font_size) + ":textfile='" + outdir +"/" + edgeid  +  "_" + "compliance.txt'" + ":x=50:y=50,fade=t=in:st=01:d=2,fade=t=out:st=28:d=2\" -c:v libx264 -b:v 1000k -pix_fmt yuv420p -video_track_timescale 15360 -c:a aac -ar 48000 -ac 2 -sample_fmt fltp -t 30 '" + outdir + "/" + edgeid + "_" + str(width) + "x" + str(height) +  "_compliance.mp4'"
    if args.verbose: 
        logger("ComplianceCommand:" +  complianceCommand )
        
    if args.noexec:
        ComplianceOutput = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:    
        ComplianceOutput = subprocess.Popen(complianceCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 

    return(ComplianceOutput);

def makeTranscode(video, EdgeID,destination, width, height, kbps):
    
    transcodeCommand = FFMPEG + " -y -i '" + video + "' -threads 8 -hide_banner -vf scale=" + str(width) + "x" + str(height) + " -b:v " + str(kbps) + "k -bufsize " + str(kbps*1000) +" -nal-hrd cbr -c:a aac -strict -2 '" + destination + "/" + EdgeID + "_" + str(width) + "x" + str(height) + "x" + str(kbps) + ".mp4'"
    if args.verbose: 
        logger("TranscodeCommand:" + transcodeCommand)
    
    if args.noexec:
        transcodeOutput = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:    
        transcodeOutput = subprocess.Popen(transcodeCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    
    
    return(transcodeOutput);
    
def makeFinalVideo():
    
    
    return

def makeVideo(size,jobflag):
    # Size is size1 or size2
    video =  Source + "/" +jobcard['video']['source_video']
    destination = jobcard[size]['out_dir']
    width = jobcard[size]['size_width']
    height = jobcard[size]['size_height']
    kbps = jobcard[size]['size_kbps']
    makeDirectories(Finish + "/" + Project + "/" + edgeid + "/" + destination)
    outdir = Finish + "/" + Project + "/" + edgeid + "/" + destination
    PartMatrix ={}
    
    if args.verbose:
        logger( "Make Video:")
        logger( "Video:" + video )
        logger("Output Dir=" + str(outdir)  )
        logger("Output Width=" +   str(width) + " Output Height=" + str(height) + " Output Kbps=" + str(kbps) )
    
    # Make Preview
    
    PartMatrix['preview'] = PREVIEW(edgeid, outdir, config['compliance']['preview_x'], config['compliance']['preview_y'], jobcard[size]['size_width'], jobcard[size]['size_height'], config['compliance']['header_color'], config['compliance']['header_font_size'], config['compliance']['header_font_color'], config['boxcover']['font'])
    # Make Compliance
    
    PartMatrix['compliance'] = makeComplianceTrailer(outdir,jobcard[size]['size_width'], jobcard[size]['size_height'])
    
    # Make Transcode
    
    PartMatrix['transcode'] = TransCodeOutput = makeTranscode(video, edgeid , outdir, jobcard[size]['size_width'], jobcard[size]['size_height'], jobcard[size]['size_kbps'])
    
    # Make complete new video
    # First Verify that previous parts have completed.
    for component in PartMatrix:
        if args.verbose:
            logger("Checking Component:" + component + " Waiting for job to complete")
        stdoutdata, stderrdata = PartMatrix[component].communicate()
        PartStatus = PartMatrix[component].returncode
        if args.verbose:
            if PartStatus == 0:
                logger("#===========================================#")
                logger("      Part " + component + " " + size + " Completed:" + str(PartStatus))
                logger("#===========================================#")
                logger(stdoutdata)
                logger("#===========================================#")
            else:
                logger("      Job " + component +"  Failed Code:" + str(PartStatus))
                logger("#===========================================#")
                logger(stdoutdata)
                logger(stderrdata)
                logger("#===========================================#")
    
    
    result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
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
    outdir=Finish + "/" + Project + "/" + edgeid + "/" + jobcard['box_cover']['out_dir']
    sourcedir =  config['default']['source']
    makeDirectories(outdir)
      
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
        
        
        if args.noexec:
            logger("     Copy Box Cover " +Source + "/" + image + " ==> " + filename)
        else:
            shutil.copy (Source + "/" + image, filename)
            
        result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif jobflag == 'produce':
        # Run the production
            ### Note We need Error Checking in here too
        logger("     Create Box Cover")
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
        BoxCoverCommand = BoxCoverCommand + "'" +str(sourcedir) + "/" + str(image) + "' \) \(  -clone 0--1 -mosaic  \) -trim -reverse '" + str(outdir) + "/" + str(EdgeID) + str(config['boxcover']['suffix']) + ".psd'; " + CONVERT + " -flatten '" + outdir + "/" + EdgeID + config['boxcover']['suffix'] + ".psd' '" + outdir + "/" +EdgeID + config['boxcover']['suffix'] +".jpg'"
        
        if args.verbose:
            logger("makeBoxCommand:" + BoxCoverCommand )
        
        if args.noexec:
            result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:    
            result = subprocess.Popen( BoxCoverCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    
    else:
            #Ignore
            logger("     Do Nothing: Box Cover")
            result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)    
    
    # Run Command in background
    
    return(result) 

def makeVideoInfo(component,jobflag):
    EdgeID = edgeid
    video =  Source + "/" +jobcard['video']['source_video']
    destination = Finish + "/" + Project + "/" + edgeid + "/" + jobcard['videoinfo']['out_dir']
    for format in ['csv', 'json', 'xml']:
        if args.verbose:
            logger("Output Video Information in " + format )
        
        probeCommand = FFPROBE + " -v error -show_format -show_streams -print_format " + format + " '" +  video + "' > " + destination +"/" + EdgeID + "-info" +"."+ format
        if args.verbose:
            logger("MakeVideoInfo:" + probeCommand)
        if args.noexec:
            result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
        else:    
            result = subprocess.Popen(probeCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    
    return(result)

def makePromoImg(component,jobflag):
    sourcedir = Source + jobcard['promoimg']['promodir']
    destination = Finish + "/" + Project + "/" + edgeid + "/" + jobcard['promoimg']['out_dir']
    
    
    if jobflag == 'produce':
        
        if os.path.isdir(str(destination)):
            if args.verbose:
                logger("Destination Directory Exists:" + str(destination))
                logger("Directoy must not exists -- ERROR")
                result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:        
        
            if args.verbose:
                logger("Copy promo images" + sourcedir +" ==> " + destination)
            
            if args.noexec:
                result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:   
                shutil.copytree(sourcedir, destination, symlinks=False, ignore=None)
                result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)    
    else:
        logger("Make Promo Image ignored -- if any flag but produce is specificed")
        result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
         
    return(result)

def makePhotoSet(component,jobflag):
    sourcedir = Source + jobcard[component]['dir']
    destination = Finish + "/" + Project + "/" + edgeid + "/" + jobcard[component]['out_dir']
    
    
    if jobflag == 'produce':
        
        if os.path.isdir(str(destination)):
            if args.verbose:
                logger("Destination Directory Exists:" + str(destination))
                logger("Directoy must not exists -- ERROR")
                result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:        
        
            if args.verbose:
                logger("Copy promo images" + sourcedir +" ==> " + destination)
            
            if args.noexec:
                result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:   
                shutil.copytree(sourcedir, destination, symlinks=False, ignore=None)
                result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)    
    else:
        logger("Make Promo Image ignored -- if any flag but produce is specificed")
        result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
         
    return(result)
    
#===================================================================#
#                Global Variables                                   #
#===================================================================#
edgeid = jobcard['clipinfo']['edgeid']
Finish = config['default']['finish']
Source = config['default']['source']
Deliveries = config['default']['deliveries']
Project = jobcard['clipinfo']['projectno']
JobMatrix = {}

 
#===================================================================#
#                Main Code                                          #
#===================================================================#

# Make Finish Directory Based on Project and EdgeID
makeDirectories(Finish + "/" + Project + "/" + edgeid)

# Loop on Components
# All output is relative to "FINISH" Volume

#for component in jobcard['component']:
#   print component

# Tested 
logger("Start Processing Job Card for:" + edgeid)
products = ['capture','video1','video2','box_cover','videoinfo','promoimg','photoset1','photoset2' ]
for component in products:  

# Set Job Flag produce, exists, ignore

    JobFlag = jobcard['component'][component]
    logger("JobFlag:" + JobFlag)

#Use the function defined in the Job Card
    action = config['functions'][component]
    if args.verbose:
        logger("Processing Component:" + str(component))
    method = eval(action)
    JobMatrix[component] = method(component, JobFlag)

# Check all Component jobs for completion   
if args.verbose: 
    logger("All Components have started processing, wait for job completion")
    logger("Check Component Completion")
    
for component in JobMatrix:
    if args.verbose:
        logger("Checking Component:" + component + " Waiting for job to complete")
    stdoutdata, stderrdata = JobMatrix[component].communicate()
    JobStatus = JobMatrix[component].returncode
    if args.verbose:
        if JobStatus == 0:
            logger("      Job Completed Successfully:" + str(JobStatus))
            logger("#===========================================#")
            logger(stdoutdata)
            logger("#===========================================#")
        else:
            logger("      Job Failed Code:" + str(JobStatus))
            logger("#===========================================#")
            logger(stdoutdata)
            logger(stderrdata)
            logger("#===========================================#")

print "End of Program"        
        
        

