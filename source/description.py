#!/opt/local/bin/python2.7

# Create a compliance file


def word_wrap(string, width=80, ind1=0, ind2=0, prefix=''):
    """ word wrapping function.
        string: the string to wrap
        width: the column number to wrap at
        prefix: prefix each line with this string (goes before any indentation)
        ind1: number of characters to indent the first line
        ind2: number of characters to indent the rest of the lines
    """
    string = prefix + ind1 * " " + string
    newstring = ""
    while len(string) > width:
        # find position of nearest whitespace char to the left of "width"
        marker = width - 1
        while not string[marker].isspace():
            marker = marker - 1

        # remove line from original string and add it to the new string
        newline = string[0:marker] + "\n"
        newstring = newstring + newline
        string = prefix + ind2 * " " + string[marker + 1:]

    return newstring + string


def produce(source, prefix, component, jobcard, config, noexec):
    from string import Template
    import os
    import subprocess

    
    COMPLIANCE = ''
    MESSAGE = ''
    ERROR = ''
    NEWLINE = "\n"
    
    MESSAGE = MESSAGE + "Create " + component + " from Template" + NEWLINE
    
    template = jobcard[component]['src']

    if os.path.isfile(template):
        MESSAGE = MESSAGE + "Template Exists: " + template + NEWLINE
    else:
        ERROR = ERROR + "Template Does not Exist: " + template + NEWLINE
        return(ERROR)
     
    
    
    
    name = jobcard['clipinfo']['edgeid'] + jobcard[component]['suffix']
    projectno = jobcard['clipinfo']['projectno']
    edgeid = jobcard['clipinfo']['edgeid']
    prime_dubya = jobcard['clipinfo']['prime_dubya']
    star = jobcard['clipinfo']['star']
    supporting = jobcard['clipinfo']['supporting']
    shorttitle = jobcard['clipinfo']['shorttitle']
    title = jobcard['clipinfo']['title']
    description = jobcard['clipinfo']['description']
    keywords = jobcard['clipinfo']['keywords']
    productiondate = jobcard['clipinfo']['productiondate']
    releasedate = jobcard['clipinfo']['releasedate']
    licensor = jobcard['clipinfo']['licensor']

    destination = prefix + "/" + projectno + "/" +  prime_dubya +"/" + edgeid + "/" + jobcard[component]['out_dir']

    


    if not os.path.isdir(destination):
        os.makedirs(destination,0777)
           
    desc_template = open(template,"r")
    desc_text = open(destination + "/" + name, "w")


    for line in desc_template:
        
        formatted_line = word_wrap(line, width=80, ind1=0, ind2=11, prefix='')
        COMPLIANCE = COMPLIANCE + formatted_line
    

    Modified = Template(COMPLIANCE).safe_substitute(STAR=star, EDGEID=edgeid, SUPPORTING=supporting,SHORTTITLE=shorttitle, KEYWORDS=keywords, PRODUCTIONDATE=productiondate, RELEASEDATE=releasedate, LICENSOR=licensor, PROJECTNO=projectno, DESCRIPTION=description, TITLE=title)
    desc_text.write(Modified)
    
    
    
    result = subprocess.Popen("echo", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #==========================================================================
    # Return a result code for parallel processing (use echo for something that will resolve as true if not needed
    # Next return logging MESSAGE
    # Next return Error Messages
    # Next return any work (or blank string if none)
    #==========================================================================
    
    return(result, MESSAGE, ERROR, Modified)  


if __name__ == "__main__":
    import sys
    import yaml
    import os
    prefix = sys.argv[1]
    component = sys.argv[2]
    
    jobfile = sys.argv[3]
    job = open(jobfile,'r')
    jobcard = yaml.load(job)
    
    destination = prefix + "/" + jobcard[component]['out_dir']
    
    #print jobcard
    print "Destination:" + str(destination) 
    print "Component:" + component 
    print "Job card file: " + jobfile

    if not os.path.isdir(destination):
        os.makedirs(destination,0777)
        
    produce(destination, component , jobcard )
    
    