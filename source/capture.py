'''
Created on Sep 29, 2017

@author: colin

Module Capture

'''

import os
import getvideosize
import subprocess


def produce(source, prefix, component, jobcard, config, noexec):
    

    FFMPEG=config['locations']['ffmpeg']
    MOGRIFY=config['locations']['mogrify']

    
    MESSAGE = ''
    ERROR = ''
    NEWLINE = '\n'
    WORK = ''
    
    # Define Parameters
    video =  source + "/" +jobcard['video']['src']
    seconds = jobcard['capture']['frame_every']
    projectno = jobcard['clipinfo']['projectno']
    edgeid = jobcard['clipinfo']['edgeid']
    prime_dubya = jobcard['clipinfo']['prima_dubya']
    videoName = os.path.basename(video)
    pathName = os.path.dirname( source + "/" + video)
    t_size = jobcard['thumbnails']['size']
    thumb_dir = jobcard['thumbnails']['out_dir']
    destination = prefix + "/" + projectno + "/" +  prime_dubya +"/" + edgeid + "/" + jobcard[component]['out_dir']
    
        
    MESSAGE = MESSAGE + "Make Stills for Video: " + videoName + NEWLINE
    MESSAGE = MESSAGE + "Source Dir:"  + pathName + NEWLINE
    MESSAGE = MESSAGE + "Put Stills in Destination:\n  " + destination + NEWLINE
    
    if not os.path.isdir(destination + "/" + thumb_dir):
        os.makedirs(destination + "/" + thumb_dir,0777)

    
    # Get video Size 
    message, error, SizeOfVideo, Duration, Bitrate  = getvideosize.produce(source, prefix, component, jobcard, config, noexec)
    
    MESSAGE = MESSAGE + message + NEWLINE
    ERROR = ERROR + error + NEWLINE         
   
    CMD = FFMPEG + " -c:v h264_vda -i '"  + video + "' -thread_type slice -hide_banner -vf fps=1/" + str(seconds) + "  -c:v mjpeg '" + destination + "/" + edgeid + "_" + SizeOfVideo + "_capture_%03d.jpg'" 
    
    MESSAGE = MESSAGE + "Making stills from video:" + video + " Size:" + str(SizeOfVideo) + " Duration:" + str(Duration) + " seconds @ bitrate:" + str(Bitrate) + NEWLINE
    MESSAGE = MESSAGE + "StillCommand:\n  " + CMD + NEWLINE
    
    if noexec:
        MESSAGE = MESSAGE + "No Execute" + NEWLINE
        result=subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        MESSAGE = MESSAGE + "Running Command" + NEWLINE   
        result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    
     
    MESSAGE = MESSAGE + "Capture on " + videoName + " Completed" + NEWLINE
        
    # Create Thumbnails at the end
    # Check for capture to complete
    # Wait for the last convert to complete. 
    stdoutdata, stderrdata = result.communicate()
    myreturncode = result.returncode 
  
    MESSAGE = MESSAGE + "Capture Return Code: " + str(myreturncode)
    MESSAGE = MESSAGE + stdoutdata
        
    # Might have to verify all completed 
    #
    #

    CMD = MOGRIFY + " -path '" + destination + "/" + str(thumb_dir) +"' -thumbnail '" + str(t_size) + "' '" + destination + "/*.jpg'"
        
    MESSAGE = MESSAGE + "Creating Thumbnails in " + destination + NEWLINE
    MESSAGE = MESSAGE + " ThumbCMD\n  " + CMD + NEWLINE
    if not noexec:     
        result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        # No Exec
        result = subprocess.Popen("ls", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        
    return(result, MESSAGE, ERROR, WORK)


def exists(prefix, component, jobcard):
    
    
    result = subprocess.Popen("ls", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return(result)