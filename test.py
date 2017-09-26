import subprocess

Command = "ls"

test = subprocess.Popen( Command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 

stdoutdata, stderrdata = test.communicate()
print test.returncode 




print "Watching the Processes"
stdoutdata, stderrdata = transcodePID.communicate()

while transcodePID.poll() == None:
    print "waiting for job to complete" 
    time.sleep(30)
print "job code: " + str(transcodePID.returncode)    
    
print "Done Watching the processes"