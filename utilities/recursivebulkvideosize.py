#!/opt/local/bin/python
# encoding: utf-8
'''
bulkvideosize -- shortdesc

bulkvideosize is a description

It defines classes_and_methods

@author:     user_name

@copyright:  2017 organization_name. All rights reserved.

@license:    license

@contact:    user_email
@deffield    updated: Updated
'''

import sys
import os

import argparse

__all__ = []
__version__ = 0.1
__date__ = '2017-10-20'
__updated__ = '2017-10-20'

DEBUG = 1
TESTRUN = 0
PROFILE = 0



program_name = os.path.basename(sys.argv[0])



    # Setup argument parser
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()

group.add_argument("-v", "--verbose", action="store_true", help="Display detailed debugging information")
parser.add_argument("-l","--logfile", action="store", help="Write Logfile if ommitted write to STDOUT")
parser.add_argument("-s","--source", action="store", help="Source Directory")

    # Process arguments

args = parser.parse_args()


verbose = args.verbose
path = args.source
logfile = args.logfile



if verbose > 0:
    print("Verbose mode on")

if logfile != None:
    log_text = open(logfile, "w")
    log_text.write("PATH,FILENAME,WIDTH,HEIGHT,KBPS,DURATION\n")


## Use Get Video Size Function

def getvideosize(src):
    import shlex
    import os
    from string import Template
    import subprocess
    import datetime
    
    FFPROBE="/opt/local/bin/ffprobe"
    Error = False
 
    
  
    for root, dirs, files in os.walk(src):
          
        for video in files:
            
            if video.endswith(".mp4") and not video[0] == '.' :
                
                filename =  root + "/" + video
    
                CMD_TEMPLATE = "$FFPROBE  -v error -of flat=s=_ -select_streams v:0 -show_entries stream=height,width,bit_rate,duration '$VIDEO'"
                CMD = Template(CMD_TEMPLATE).safe_substitute(FFPROBE=FFPROBE, VIDEO=filename)
    
        
                videoName = os.path.basename(video)
                pathName = os.path.dirname(src + "/" + video)
        
                #print("Get the Video Size Information for Video: " + videoName )
                #print("Source Dir:" + pathName )
                #print("getVideoSizeCMD:\n  " )
        
                try:
                    pCMD = shlex.split(CMD)
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
                    myduration = str(datetime.timedelta(seconds=int(float(Duration))))
                    mybitrate = str(int(BitRate)/1000)
                    #print(path + "," + video + "," + lHeight + "," + lWidth + "," + mybitrate + "," + myduration)
                    if logfile != None:                                 
                        log_text.write(root + "," + video + "," + Height + "," + Width + "," + mybitrate + "," + myduration +"\n")
                    else:
                        print("[" +root + "," + video + "," + Height + "," + Width + "," + mybitrate + "," + myduration +"]")
                        
                except:
                    #print("Video Source: " + video + "ERROR")
                    if logfile != None:
                        log_text.write(root + "," + video + "," + "ERROR,ERROR,ERROR,ERROR")
            
    if logfile != None:
        log_text.close()
        
    return(Error)

myError = getvideosize(path)


