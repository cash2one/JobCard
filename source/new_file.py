import yaml
import importlib
import os

component = 'photoset1'
prefix = '/Users/colin/Documents/Appcelerator_Studio_Workspace/JobCard/Assembly/'
source = '/Users/colin/Documents/Appcelerator_Studio_Workspace/JobCard/EdgeSource01'
finish = '/Users/colin/Documents/Appcelerator_Studio_Workspace/JobCard/Finished'
card = '/Users/colin/Documents/Appcelerator_Studio_Workspace/JobCard/example/edge0022.yaml'
job = open('/Users/colin/Documents/Appcelerator_Studio_Workspace/JobCard/example/edge0022.yaml','r')
cfile = open('/Users/colin/Documents/Appcelerator_Studio_Workspace/JobCard/example/config.yaml','r')
noexec = False
jobcard = yaml.load(job)
config = yaml.load(cfile)
jobflag = 'exists'

#destination = prefix + jobcard['clipinfo']['projectno'] + "/" + jobcard['clipinfo']['prime_dubya'] + "/" + jobcard['clipinfo']['edgeid']
#if not os.path.isdir(destination):
#        os.makedirs(destination,0777)


#print createComplianceText.createDescription(destination,component, jobcard)

myModule = importlib.import_module('photoset')

if jobflag == 'produce':
    result, message, error, work = myModule.produce(source, prefix, component, jobcard, config, noexec)
elif jobflag == 'exists':
    result, message, error, work = myModule.exists(finish, prefix, component, jobcard, config, noexec)


#message, error, sizeofVideo,Duration,BitRate = myModule.produce(source, prefix, component, jobcard, config, noexec)


print "Result:" + str(result)
print "Message:\n" + message
print "Error:\n" + error
print "Work:\n"+ work
