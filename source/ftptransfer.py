#!/opt/local/bin/python
'''
Created on Dec 7, 2017

@author: colin
'''

import os
import ftplib 

counter = 0

def myCallBack(filename):
    global counter
    print "block transferred:" + str(counter)
    counter = counter + 1
    return

username = "colin"   
password = "Space1999" 
filename = "/edge/Scratch/Test01/GMCZ_Scenes/GMCZ0022/clips4sale/edgeinter11/clips/GMCZ0022_1920x1080x6000_final.mp4"
host = "172.16.1.128"
destination = "clips2"
basename = os.path.basename(filename)
print basename

if os.path.isfile(filename): 
    print str(filename) + " file exists"
    filehandle = open(filename,'rb')
    
try:
    ftp = ftplib.FTP(host,username,password)
    print ftp.getwelcome()

    ftp.set_pasv(True)   
    ftp.cwd(destination)
    print ftp.pwd()
    try:
        ftp.size(basename)
        print "File Exists"
    except:
        print "Uploadling new file"
        
    print ftp.storbinary('STOR ' + str(basename), filehandle, 8192)


except Exception as e: 
        Error = True
        print("An error occured " + str(e))
              


    


    