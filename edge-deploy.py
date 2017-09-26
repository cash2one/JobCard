#!/usr/bin/python

#Import Libraries
import yaml
import subprocess
import sys
import os
import time



config = ("config.yml")
clip = ("clip.yml")

print "Edge Interactive Deployment Program (MCP)"




with open(config, 'r') as cfg:
    config = yaml.load(cfg)
    
with open(clip,'r') as clip:
    clip = yaml.load(clip)    


    
# Set Global Configuration Values

CURL=config['locations']['curl']
CONVERT=config['locations']['convert']
FFMPEG=config['locations']['ffmpeg']
FFPROBE=config['locations']['ffprobe']
FONT=config['boxcover']['font']


DEBUG=True

#subprocess.check_call([CURL, "--version"])
#subprocess.check_call([CONVERT, "--version"])
#subprocess.check_call([FFMPEG, "-version"])

#curlOUTPUT=subprocess.Popen([CURL, "--version"])

print '===='

if DEBUG:
    for section in clip:
        print(section)
        for clipkeys in clip[section]:
            print ('      ->', clipkeys, ':', clip[section][clipkeys])

#### Define Functions
#### Start with Easy ones -- Move to harder ones.

def uploadClips4Sale(account,file):
    if DEBUG:
        print "Account: " + account
        print "File to upload: " + file
        print "Account Password" + config['clips4sale'][account]
        print "FTP Site is:" + config['clips4sale']['ftpsite']
        subprocess.check_call(["ls", "-lh"])
        
    # Make Parameters for CURL
    curlCommand = CURL + " -u " + account +":" + config['clips4sale'][account] +" -T " + file + " ftp://" + config['clips4sale']['ftpsite']
    curlOUTPUT=subprocess.Popen(curlCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print curlOUTPUT
                                 
    return;

def makeBoxCover(image, title, star, supporting, keywords, EdgeID, title_size, star_size, support_size, keyword_size, EdgeID_size, alignment, color, outdir ):
    if DEBUG:
        print "Title:" + title + " : size %d" % title_size
        print "Star:" + star + " : size %d" %  star_size
        print "Supporting:" + supporting + " : size %d" % support_size
        print "Keywords:" + keywords + " : size %d" % keyword_size
        print "Part Num:" + EdgeID + " : size %d" % EdgeID_size
        print "Title Alignment:" + alignment
        print "Text Color:" + color
        print "Font:" + FONT
    ### Note We need Error Checking in here too
    
    if alignment == 'left':
        gravity='Northwest'
    if alignment == 'center':
        gravity = 'North'
    if alignment == 'right':
        gravity='NorthEast'        
    
    #Make keywords split by line
    
    keywords_f = keywords.replace(" ","\\n")
    title_f = title.replace("'","\\'")
    
    BoxCoverCommand = CONVERT + " -verbose -size " + str(config['boxcover']['box_width']) + "x" + str(config['boxcover']['box_height']) + " -font " + FONT + " -pointsize " + str(title_size)
    BoxCoverCommand = BoxCoverCommand + " -fill " + color + " \( \( -gravity " + gravity + " -background transparent -pointsize  " + str(title_size) + "  label:\"" + title_f +"\"" + " -pointsize " + str(star_size)
    BoxCoverCommand = BoxCoverCommand + " -annotate +0+250 '" + star + "'" + " -pointsize " + str(support_size) + " -annotate +0+450 '" +  supporting + "' -splice 0x18 \)"
    BoxCoverCommand = BoxCoverCommand + " \( +clone -background black -shadow 20x-9+0+0 \) -background transparent +swap -layers merge +repage \)  \( \( -gravity West -background transparent -pointsize " 
    BoxCoverCommand = BoxCoverCommand + str(keyword_size) + " label:'" + keywords_f + "'  -splice 50x0 \)  \( +clone -background black -shadow 20x-9+0+0 \) -background transparent +swap -layers merge +repage \) \( -gravity SouthWest "+ " -pointsize " +str(EdgeID_size) + " -background transparent label:"
    BoxCoverCommand = BoxCoverCommand + EdgeID +" -splice 100x0 \) " + "  \( \( -gravity SouthEast -background transparent label:'EDGE   \n' -splice 0x18  -pointsize 50  -annotate +50+192 '  _____________________   ' -splice 0x18 -pointsize 100 -annotate +50+120 'interactive  '   \) "
    BoxCoverCommand = BoxCoverCommand + " \( +clone -background black -shadow 60x18+0+0 \) -background transparent +swap -layers merge +repage \) \(  -label 'image' -background transparent -mosaic label:blank "
    BoxCoverCommand = BoxCoverCommand + image + " \) \(  -clone 0--1 -mosaic  \) -trim -reverse " + outdir + "/" + EdgeID + config['boxcover']['suffix'] + ".psd; " + CONVERT + " -flatten " + outdir + "/" + EdgeID + config['boxcover']['suffix'] + ".psd " + outdir + "/" +EdgeID + config['boxcover']['suffix'] +".jpg"
    
    
    
    print BoxCoverCommand
    
    boxCoverOutput = subprocess.Popen( BoxCoverCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Run Command in background
    
    return;    


def makeDirectories(base,project,part):
    print "Base: " + base
    print "Project: " + project
    print "Part: " +  part
    
    
    projectdir = base + "/" + project
    partdir = projectdir + "/" + part
    capturedir = partdir + "/capture"
    promodir = partdir + "/promo"
    videodir = partdir + "/video"
    photodir = partdir + "/photoset"
    dvddir = partdir + "/dvd"
    
    if not os.path.isdir(base):
        print "Missing Directory"
        exit()

    if not os.path.isdir(projectdir):
        os.makedirs(projectdir,0777)
        print "Created" + projectdir
    else:
        print "Directory" + projectdir + " -- exists"
    
    if not os.path.isdir(partdir):
        os.makedirs(partdir,0777)
        print "Created" + partdir
    else:
        print "Directory" + partdir + " -- exists" 
    
    if not os.path.isdir(capturedir):
        os.makedirs(capturedir,0777)
        print "Created" + capturedir
    else:
        print "Directory" + capturedir + " -- exists"     

    if not os.path.isdir(promodir):
        os.makedirs(promodir,0777)
        print "Created" + promodir
    else:
        print "Directory" + promodir + " -- exists"     

    if not os.path.isdir(videodir):
        os.makedirs(videodir,0777)
        print "Created" + videodir
    else:
        print "Directory" + videodir + " -- exists"     

    if not os.path.isdir(photodir):
        os.makedirs(photodir,0777)
        print "Created" + photodir
    else:
        print "Directory" + photodir + " -- exists"     

    if not os.path.isdir(dvddir):
        os.makedirs(dvddir,0777)
        print "Created" + dvddir
    else:
        print "Directory" + dvddir + " -- exists"     
               
    
    return;

def makeStills(video,destination,seconds, EdgeID):
    stillCommand = FFMPEG + " -i " + video + " -thread_type slice -hide_banner -vf fps=1/" + str(seconds) + " " + destination + "/capture/" + EdgeID + "_capture_%03d.jpg"    
    print stillCommand
    stillCommandOutput = subprocess.Popen(stillCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    return;
 
def makeTranscode(video, EdgeID,destination, width, height, kbps):
    
    transcodeCommand = FFMPEG + " -y -i " + video + " -threads 8 -hide_banner -vf scale=" + str(width) + "x" + str(height) + " -b:v " + str(kbps) + "k -bufsize " + str(kbps) +" -c:a aac -strict -2 " + destination + "/" + EdgeID + "_" + str(width) + "x" + str(height) + "x" + str(kbps) + ".mp4"
    print transcodeCommand 
    transcodeOutput = subprocess.Popen(transcodeCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    
    return(transcodeOutput);

def makeVideoInfo(EdgeID, video, destination):
    for format in ['csv', 'json', 'xml']:
        print "Output Video Information in " + format
        
        probeCommand = FFPROBE + " -v error -show_format -show_streams -print_format " + format + " " +  video + " > " + destination +"/" + EdgeID +"."+ format
        print probeCommand
        probeOutput = subprocess.Popen(probeCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    
    return;

def makeComplianceTrailer(EdgeID, video, destination, width, height, back_color, font_size, font_color, font, textfile):
    # Note the configuration file contains most of the variables
 
    # We need to create a new file from template for the compliance text.
    compliance_template = open(textfile,"r")
    compliance_file = open (destination + "/promo/" + EdgeID + "_" + "compliance.txt","w")
    
    compliance_file.write(clip['clipinfo']['title'] + " - " + clip['clipinfo']['EdgeID'] + "\n\n")
    compliance_file.write("Edge ID: " + clip['clipinfo']['EdgeID']+ "\n\n")
    compliance_file.write("Starring: " + clip['clipinfo']['star']+ "\n\n")
    compliance_file.write("Supporting cast: " + clip['clipinfo']['supporting']+ "\n\n")
    compliance_file.write("Keywords: " + clip['clipinfo']['keywords']+ "\n\n")
    compliance_file.write("Production Date: " + clip['clipinfo']['ProductionDate']+ "\n\n")
    compliance_file.write("Licensor: " + clip['clipinfo']['Licensor']+ "\n\n")
    compliance_file.write("\n\n\n")
    
    for line in compliance_template:
        compliance_file.write(line)

    compliance_file.close()
    compliance_template.close()
    
    complianceCommand = FFMPEG + " -y -f lavfi -r 30 -i color=" + back_color + ":" +str(width) + "x" + str(height) + " -f lavfi -i anullsrc -vf drawtext=\"fontfile=" + font + ":fontcolor=" + font_color + ": fontsize=" + str(font_size) + ":textfile=" + destination + "/promo/" + EdgeID  +  "_" + "compliance.txt" + ":x=50:y=50,fade=t=in:st=01:d=2,fade=t=out:st=28:d=2\" -c:v libx264 -b:v 1000k -pix_fmt yuv420p -video_track_timescale 15360 -c:a aac -ar 48000 -ac 2 -sample_fmt fltp -t 30 " + destination + "/video/" + EdgeID + "_" + str(width) + "x" + str(height) +  "_compliance.mp4"
    
    print complianceCommand
    complianceCommandOutput = subprocess.Popen(complianceCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    
    return;

def makePreview(EdgeID, destination, x, y, width, height, back_color, font_size, font_color, font):
    
    # Fix the title for any apostrophe
    
    title = clip['clipinfo']['title']
    title_f = title.replace("'","''\''")
    
    previewCommand = FFMPEG + " -y -f lavfi -r 30 -i color=" + back_color +":"+ str(width) + "x" + str(height) + " -f lavfi -i anullsrc -filter_complex  "
    # Make Title Line
    previewCommand = previewCommand + "\"drawtext=enable='between(t,00,10)':fontfile=" + font + ":text=\'" + title_f + " " + EdgeID + "\':x=" + str(x) + ":y=" + str(y) +":fontcolor=" + font_color  + ":fontsize=" + str(font_size)
    # Sub Title
    previewCommand = previewCommand + ",drawtext=enable='between(t,00,10)':fontfile=" + font + ":text=\'Starring " +  clip['clipinfo']['star'] + "\':x=" + str(x) + ":y=" + str(y+100) +":fontcolor=" + font_color + ":fontsize=" + str(font_size)
    # Keywords
    previewCommand = previewCommand + ",drawtext=enable='between(t,00,10)'    :fontfile=" + font + ":text=\'in " + clip['clipinfo']['keywords'] + "\':x=" + str(x) + ":y=" + str(y+200) +":fontcolor=" + font_color + ":fontsize=" + str(font_size)
    # Wrap end of command
    previewCommand = previewCommand + "\" -c:v libx264 -b:v 1000k -pix_fmt yuv420p -video_track_timescale 15360 -c:a aac -ar 48000 -ac 2 -sample_fmt fltp -t 12 " + destination + "/" + EdgeID + "_" + str(width) + "x" + str(height) + "_" + "preview" + ".mp4" 
    
   
    
    print previewCommand
    previewOutput = subprocess.Popen(previewCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    return (previewOutput) ;


##### MAIN CODE

#makeDirPID = makeDirectories(config['default']['temp'],clip['clipinfo']['projectno'],clip['clipinfo']['EdgeID'])
#makeBoxPID = makeBoxCover(clip['box_cover']['cover'], clip['clipinfo']['title'] + " " + clip['clipinfo']['EdgeID'] , clip['clipinfo']['star'], clip['clipinfo']['supporting'], clip['clipinfo']['keywords'], clip['clipinfo']['EdgeID'], config['boxcover']['title_size'],config['boxcover']['star_size'],config['boxcover']['support_size'],config['boxcover']['keyword_size'],config['boxcover']['EdgeID_size'],"right","white", config['default']['temp'] + "/" + clip['clipinfo']['projectno'] + "/" + clip['clipinfo']['EdgeID'] + "/promo" )
#makeCapPID = makeStills(clip['video']['source_video'],config['default']['temp'] + "/" + clip['clipinfo']['projectno'] + "/" + clip['clipinfo']['EdgeID'],clip['video']['capture'], clip['clipinfo']['EdgeID'])
#makeInfPID = makeVideoInfo(clip['clipinfo']['EdgeID'], clip['video']['source_video'], config['default']['temp'] + "/" + clip['clipinfo']['projectno'] + "/" + clip['clipinfo']['EdgeID'] + "/promo")
tranVid1PID = makeTranscode(clip['video']['source_video'], clip['clipinfo']['EdgeID'], config['default']['temp'] + "/" + clip['clipinfo']['projectno'] + "/" + clip['clipinfo']['EdgeID'] + "/video", clip['video']['size1_width'], clip['video']['size1_height'], clip['video']['size1_kbps'])
#tranVid2PID = makeTranscode(clip['video']['source_video'], clip['clipinfo']['EdgeID'], config['default']['temp'] + "/" + clip['clipinfo']['projectno'] + "/" + clip['clipinfo']['EdgeID'] + "/video", clip['video']['size2_width'], clip['video']['size2_height'], clip['video']['size2_kbps'])
makeCom1PID = makeComplianceTrailer(clip['clipinfo']['EdgeID'], clip['video']['source_video'], config['default']['temp'] + "/" + clip['clipinfo']['projectno'] + "/" + clip['clipinfo']['EdgeID'], clip['video']['size1_width'], clip['video']['size1_height'],config['compliance']['compliance_color'], config['compliance']['compliance_text_size'], config['compliance']['compliance_text_color'], config['compliance']['compliance_font'], config['compliance']['compliance'])
#makeCom2PID = makeComplianceTrailer(clip['clipinfo']['EdgeID'], clip['video']['source_video'], config['default']['temp'] + "/" + clip['clipinfo']['projectno'] + "/" + clip['clipinfo']['EdgeID'], clip['video']['size2_width'], clip['video']['size2_height'],config['compliance']['compliance_color'], config['compliance']['compliance_text_size'], config['compliance']['compliance_text_color'], config['compliance']['compliance_font'], config['compliance']['compliance'])
makePre1PID = previewPID1 = makePreview(clip['clipinfo']['EdgeID'], config['default']['temp'] + "/" + clip['clipinfo']['projectno'] + "/" + clip['clipinfo']['EdgeID'] + "/video", 100, 100, clip['video']['size1_width'], clip['video']['size1_height'], config['compliance']['header_color'], config['compliance']['header_font_size'], config['compliance']['header_font_color'], config['boxcover']['font'])
#makePre1PID = previewPID2 = makePreview(clip['clipinfo']['EdgeID'], config['default']['temp'] + "/" + clip['clipinfo']['projectno'] + "/" + clip['clipinfo']['EdgeID'] + "/video", 100, 100, clip['video']['size2_width'], clip['video']['size2_height'], config['compliance']['header_color'], config['compliance']['header_font_size'], config['compliance']['header_font_color'], config['boxcover']['font'])
