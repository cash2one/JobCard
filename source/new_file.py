import createComplianceText
import yaml

component = 'ebay_text'
destination = '/Users/colin/Documents/Appcelerator_Studio_Workspace/JobCard/Assembly/Test01/GMCZ0022'
card = '/Users/colin/Documents/Appcelerator_Studio_Workspace/JobCard/example/edge0022.yaml'
job = open('/Users/colin/Documents/Appcelerator_Studio_Workspace/JobCard/example/edge0022.yaml','r')
jobcard = yaml.load(job)


print createComplianceText.createDescription(destination,component, jobcard)


