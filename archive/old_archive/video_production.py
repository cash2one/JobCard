'''
Created on Sep 30, 2017

@author: colin
'''

def logger(message):
        import datetime
        myTime = datetime.datetime.now()
            print str(myTime) + "-> " + str(message)

def preview(source, prefix, component, jobcard, config, noexec):
    destination = prefix + "/" + jobcard['clipinfo']['projectno']  + "/" + edgeid + "/" + jobcard[component]['out_dir']
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
        logger("  Offset X="  + str(x) + " Offset Y=" + str(y))
    if args.noexec:
        results = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:    
        results = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    return (results) ;
    
def makeComplianceTrailer(source, prefix, component, jobcard, config, noexec):
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

def makeTranscode(source, prefix, component, jobcard, config, noexec):
    
    transcodeCommand = FFMPEG + " -y -i '" + video + "' -threads 8 -hide_banner -vf scale=" + str(width) + "x" + str(height) + " -c:v h264_videotoolbox -b:v " + str(kbps) + "k -bufsize " + str(kbps*1000) +" -nal-hrd cbr -c:a aac -strict -2 '" + destination + "/" + EdgeID + "_" + str(width) + "x" + str(height) + "x" + str(kbps) + ".mp4'"
    if args.verbose: 
        logger("  TranscodeCommand:\n  " + transcodeCommand)
    
    if args.noexec:
        transcodeOutput = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:    
        transcodeOutput = subprocess.Popen(transcodeCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    
    
    return(transcodeOutput);

def makeConcatVideo(source, prefix, component, jobcard, config, noexec):
    
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

def writeMP4Metadata(source, prefix, component, jobcard, config, noexec):
    destination = Assembly + "/" + jobcard['clipinfo']['projectno'] + "/" + edgeid + "/" + jobcard[component]['out_dir']
    width = jobcard[component]['size_width']
    height = jobcard[component]['size_height']
    kbps = jobcard[component]['size_kbps'] 
    makeDirectories(destination)
    video = edgeid + "_" + str(width) + "x" + str(height) + "x" + str(kbps) + "_finished.mp4"
    outvideo = edgeid + "_" + str(width) + "x" + str(height) + "x" + str(kbps) + "_final.mp4"
    
    quote = "\""
    
    
    title = quote + jobcard['clipinfo']['title'] + " " + edgeid + quote
    author = quote + jobcard['clipinfo']['star'] + quote
    composer = quote + "Edge Interactive" + quote
    album = quote + jobcard['clipinfo']['supporting'] + quote
    proddate = quote + jobcard['clipinfo']['productiondate'] + quote
    release = quote + jobcard['clipinfo']['releasedate'] + quote
    comment = quote + jobcard['clipinfo']['keywords'] + quote
    genre = quote + "Adult"  + quote
    copyright_t = quote + "This production is produced 8/9/17 and copyright 2017 Edge Interactive Publishing Inc. All rights reserved. No right is granted for reproduction of these images other than for the personal use by the purchaser of this disk." + quote
    description = quote +  jobcard['clipinfo']['description'] + quote
    synopsis = quote + jobcard['clipinfo']['description'] + quote
    show = quote + jobcard['clipinfo']['shorttitle'] + quote
    episode_id = quote + edgeid + quote
    network = quote + jobcard['clipinfo']['licensor'] + quote
    track = quote + jobcard['clipinfo']['shorttitle'] + quote
    actors = quote + jobcard['clipinfo']['star'] + " and " + jobcard['clipinfo']['supporting'] + quote

    
    logger("Writing MP4 metadata")
    CMD = FFMPEG + " -i '" + destination + "/" + video + "' -metadata title=" + title + " -metadata author=" + author + " -metadata composer=" + composer + " -metadata album=" + album + " -metadata date=" + proddate + " -metadata purchase_date=" + release
    CMD = CMD + " -metadata track=" + track + " -metadata artist=" + actors +" -metadata comment=" + comment + " -metadata genre=" + genre + " -metadata copyright=" + copyright_t + " -metadata description=" + description + " -metadata synopsis=" + synopsis
    CMD = CMD + " -metadata show=" + show + " -metadata episode_id=" + episode_id + " -metadata network=" + network + " -metadata media_type=9 -y -c:v h264_videotoolbox -b:v " + str(kbps) +"k '" + destination + "/" + outvideo + "'"
    
    if args.verbose: 
        logger("  Writing Meta Data CMD:\n  " +  CMD )
    if args.noexec:
        result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:    
        result = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)     
    return(result)

def produce(source, prefix, component, jobcard, config, noexec):
    

    FFMPEG=config['locations']['ffmpeg']
    MOGRIFY=config['locations']['mogrify']

    CODEC = 'h264_videotoolbox'
    
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
    
    
        # component is component1 or component2
    video =  Source + "/" +jobcard['video']['src'] 
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
    
      # Start Concat
    PartMatrix['metadata'] = writeMP4Metadata(component,jobflag)


    #Verify Concat Completes before next process starts
    stdoutdata, stderrdata = PartMatrix['metadata'].communicate()
    PartStatus = PartMatrix['metadata'].returncode 
    if args.verbose:
        logger("  metadata Completed with return code " + str(PartStatus))      
    
    result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    return(result)

    
    return(result, MESSAGE, ERROR, WORK)