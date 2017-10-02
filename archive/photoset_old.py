'''
Created on Sep 29, 2017

@author: colin
'''
def produce(source, prefix, component, jobcard, config, noexec):
    import os
    import subprocess
    
    MESSAGE = ''
    ERROR = ''
    WORK = ''
    NEWLINE = '\n'
    
    projectno = jobcard['clipinfo']['projectno']
    edgeid = jobcard['clipinfo']['edgeid']
    prime_dubya = jobcard['clipinfo']['prime_dubya']
    sourcedir = source + "/" + jobcard[component]['src']
    t_size = jobcard['thumbnails']['size']
    thumb_dir = jobcard['thumbnails']['out_dir']
    
    CONVERT=config['locations']['convert']
    MOGRIFY=config['locations']['mogrify']
    
    destination = prefix + "/" + projectno + "/" +  prime_dubya +"/" + edgeid + "/" + jobcard[component]['out_dir'] + "_" + str(jobcard[component]['set_width']) + "x" + str(jobcard[component]['set_height'])
    if not os.path.isdir(destination + "/" + thumb_dir):
        os.makedirs(destination + "/" + thumb_dir,0777)
        
        
    PhotoMatrix = {}
    ErrorMatrix = {}
    #=======================================================================
    # Produce Images
    #=======================================================================
    print "Produce Images"
    print "Source Dir:" + sourcedir
    MESSAGE = MESSAGE + "makePhotoSet: Produce" + NEWLINE
    if not os.path.isdir(sourcedir): 
        print "Source Dir does not exists"        
        MESSAGE = MESSAGE +  "Make Photo set: Directory does not exist: " + sourcedir + NEWLINE
        ErrorMatrix['makePhotoSet'] = "directory " + sourcedir + " does not exist"
        result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  
        return(result) 
    count = 0
        
    for filename in os.listdir(sourcedir):
        if filename.endswith(".tif") or filename.endswith(".jpg"): 
            MESSAGE = MESSAGE +  "copying file " + filename + " to " + destination + NEWLINE
            CMD = CONVERT +" '" + sourcedir + "/" + filename + "' -resize " + str(jobcard[component]['set_width']) + "x" + str(jobcard[component]['set_height']) + " -set filename:mysize '%wx%h' '" + destination + "/" + edgeid + "_" + str(count).zfill(3) + ".jpg'; "           
            MESSAGE = MESSAGE +  "makePhotoSetCMD\n  " + CMD  + NEWLINE
            if not noexec:    
                PhotoMatrix[count] = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                count = count + 1    
            else:
                MESSAGE = MESSAGE +  "ignoring file " + filename + NEWLINE
        
    if not noexec:
        # Wait for the last convert to complete. 
        for photo in range(0,count):
            MESSAGE = MESSAGE +  "  Checking on Photo # " + str(photo) + " to complete" + NEWLINE
            stdoutdata, stderrdata = PhotoMatrix[photo].communicate()
            PartStatus = PhotoMatrix[photo].returncode 
            MESSAGE = MESSAGE +  "   Photo conversion returned Status: " + str(PartStatus) + NEWLINE
    
    
    #===========================================================================
    # Create Thumbnails
    #===========================================================================
    # Create Thumbnails for all of the images
    CMD = MOGRIFY + " -path '" + destination + "/" + str(thumb_dir) +"' -thumbnail '" + str(t_size) + "' '" + destination + "/*.jpg'"
        
    MESSAGE = MESSAGE + "Creating Thumbnails in " + destination + NEWLINE
    MESSAGE = MESSAGE + " ThumbCMD\n  " + CMD + NEWLINE
    if not noexec:     
        result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        # No Exec
        result = subprocess.Popen("ls", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        

           
    return(result, MESSAGE, ERROR, WORK)  

def exists(source, prefix, component, jobcard, config, noexec):
    import os
    import subprocess
    
    MESSAGE = ''
    ERROR = ''
    WORK = ''
    NEWLINE = '\n'
    
    projectno = jobcard['clipinfo']['projectno']
    edgeid = jobcard['clipinfo']['edgeid']
    prime_dubya = jobcard['clipinfo']['prime_dubya']
    sourcedir = source + "/" + jobcard[component]['src']
    t_size = jobcard['thumbnails']['size']
    thumb_dir = jobcard['thumbnails']['out_dir']
    
    CONVERT=config['locations']['convert']
    MOGRIFY=config['locations']['mogrify']
    
    destination = prefix + "/" + projectno + "/" +  prime_dubya +"/" + edgeid + "/" + jobcard[component]['out_dir'] + "_" + str(jobcard[component]['set_width']) + "x" + str(jobcard[component]['set_height'])
    if not os.path.isdir(destination + "/" + thumb_dir):
        os.makedirs(destination + "/" + thumb_dir,0777)
        
        
    PhotoMatrix = {}
    ErrorMatrix = {}
    #=======================================================================
    # Existing Images
    #=======================================================================
    print "Existing Images"
    print "Source Dir:" + sourcedir
    MESSAGE = MESSAGE + "makePhotoSet: Existing" + NEWLINE
    if not os.path.isdir(sourcedir): 
        print "Source Dir does not exists"        
        MESSAGE = MESSAGE +  "Make Photo set: Directory does not exist: " + sourcedir + NEWLINE
        ErrorMatrix['makePhotoSet'] = "directory " + sourcedir + " does not exist"
        result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  
        return(result) 
    count = 0
        
    for filename in os.listdir(sourcedir):
        if filename.endswith(".tif") or filename.endswith(".jpg"): 
            MESSAGE = MESSAGE +  "copying file " + filename + " to " + destination + NEWLINE
            CMD = CONVERT +" '" + sourcedir + "/" + filename + "' -resize " + str(jobcard[component]['set_width']) + "x" + str(jobcard[component]['set_height']) + " -set filename:mysize '%wx%h' '" + destination + "/" + edgeid + "_" + str(count).zfill(3) + ".jpg'; "           
            MESSAGE = MESSAGE +  "makePhotoSetCMD\n  " + CMD  + NEWLINE
            if not noexec:    
                PhotoMatrix[count] = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                count = count + 1    
            else:
                MESSAGE = MESSAGE +  "ignoring file " + filename + NEWLINE
        
    if not noexec:
        # Wait for the last convert to complete. 
        for photo in range(0,count):
            MESSAGE = MESSAGE +  "  Checking on Photo # " + str(photo) + " to complete" + NEWLINE
            stdoutdata, stderrdata = PhotoMatrix[photo].communicate()
            PartStatus = PhotoMatrix[photo].returncode 
            MESSAGE = MESSAGE +  "   Photo conversion returned Status: " + str(PartStatus) + NEWLINE
    
    
    #===========================================================================
    # Create Thumbnails
    #===========================================================================
    # Create Thumbnails for all of the images
    CMD = MOGRIFY + " -path '" + destination + "/" + str(thumb_dir) +"' -thumbnail '" + str(t_size) + "' '" + destination + "/*.jpg'"
        
    MESSAGE = MESSAGE + "Creating Thumbnails in " + destination + NEWLINE
    MESSAGE = MESSAGE + " ThumbCMD\n  " + CMD + NEWLINE
    if not noexec:     
        result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        # No Exec
        result = subprocess.Popen("ls", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        

    return(result, MESSAGE, ERROR, WORK) 