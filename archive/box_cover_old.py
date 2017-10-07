#!/opt/local/bin/python2.7
'''
Created on Sep 29, 2017

Module box_cover

@author: colin
'''

def produce(prefix ,component, jobcard, config):
    image=jobcard['box_cover']['cover']
    title=jobcard['clipinfo']['title']
    star=jobcard['clipinfo']['star']
    supporting = jobcard['clipinfo']['supporting']
    keywords = jobcard['clipinfo']['shorttitle']
    edgeid = jobcard['clipinfo']['edgeid]
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