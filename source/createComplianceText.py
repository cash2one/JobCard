#!/opt/local/bin/python2.7


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

star = 'Donna Bell'
edgeid = 'GMCZ0022'
shorttitle = 'Suck Fuck Anal A2M Facial'
supporting = 'Choky Ice'
keywords = 'Porn Stars, Hetrosexual, Blowjobs, Finger Fucking, Vaginal Sex, Anal, A2M, Facials, Hose, Uniforms'
stats = 'Model Stats with crazy formatting I am sure'
productiondate = 'June 1, 2010'
releasedate = 'September 26, 2017'
licensor = 'Global Media International License.'
primedubya = 'GMCZ_Scenes'


# Create a compliance file
from string import Template

template = '/Users/colin/Documents/Appcelerator_Studio_Workspace/JobCard/example/compliance_template.txt'

compliance_template = open(template,"r")


COMPLIANCE = ''

for line in compliance_template:
    
    formatted_line = word_wrap(line, width=80, ind1=0, ind2=11, prefix='')
    COMPLIANCE = COMPLIANCE + formatted_line
    

Modified = Template(COMPLIANCE).safe_substitute(STAR=star, EDGEID=edgeid, SUPPORTING=supporting,SHORTTITLE=shorttitle, KEYWORDS=keywords, STATS=stats, PRODUCTIONDATE=productiondate, RELEASEDATE=releasedate, LICENSOR=licensor, PRIMEDUBYA=primedubya)

print Modified    