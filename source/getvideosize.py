'''
Created on Sep 29, 2017

@author: colin
'''
# Useful functions too small for their own module






def produce(source, prefix, component, jobcard, config, noexec):
    import shlex
    import os
    from string import Template
    import subprocess
    import datetime
    
    CURL=config['locations']['curl']
    CONVERT=config['locations']['convert']
    FFMPEG=config['locations']['ffmpeg']
    FFPROBE=config['locations']['ffprobe']
    MOGRIFY=config['locations']['mogrify']
    FONT=config['boxcover']['font']
    
    MESSAGE = ''
    ERROR = ''
    NEWLINE = '\n'
    
    
    
    #Validate global short cuts exists
    if not os.path.isfile(CURL):
        print "Curl is missing:" + str(CURL)
        exit(3)
    if not os.path.isfile(CURL):
        print "Convert is missing:" + str(CONVERT)
        exit(3)
    if not os.path.isfile(FFMPEG):
        print "ffmpeg is missing:" + str(FFMPEG)
        exit(3) 
    if not os.path.isfile(FFPROBE):
        print "ffprobe is missing:" + str(FFPROBE)
        exit(3)
    if not os.path.isfile(MOGRIFY):
        print "Font is missing:" + str(FONT)
        exit(3)  
    if not os.path.isfile(FONT):
        print "Font is missing:" + str(FONT)
        exit(3)       
    
    video =  source + "/" + jobcard['video']['src']

    
    CMD_TEMPLATE = "$FFPROBE  -v error -of flat=s=_ -select_streams v:0 -show_entries stream=height,width,bit_rate,duration '$VIDEO'"
    CMD = Template(CMD_TEMPLATE).safe_substitute(FFPROBE=FFPROBE, VIDEO=video)
    
    
    videoName = os.path.basename(video)
    pathName = os.path.dirname( source + "/" + video)
    
    MESSAGE = MESSAGE + "Get the Video Size Information for Video: " + videoName + NEWLINE
    MESSAGE = MESSAGE + "Source Dir:" + pathName + NEWLINE
    MESSAGE = MESSAGE + "getVideoSizeCMD:\n  " + CMD  + NEWLINE
    

    pCMD = shlex.split(CMD)
    
    if noexec: 
        result=subprocess.check_output("echo")
        sizeofVideo="1920x1080"
        Duration="60"
        BitRate="1500000"
        myduration = '00:00:00'
        mybitrate = '1500'
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
        myduration = str(datetime.timedelta(seconds=int(float(Duration))))
        mybitrate = str(int(BitRate)/1000)
          
        
    MESSAGE = MESSAGE + "Video Source: Size: " + sizeofVideo + " Duration:" + myduration + " BitRate:" + mybitrate + " kbps" 
 
    return(MESSAGE, ERROR, sizeofVideo,Duration,BitRate)


