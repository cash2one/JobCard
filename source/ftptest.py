#!/opt/local/bin/python
#-*- coding: utf-8 -*-
'''
Created on Dec 7, 2017

@author: colin
'''

import job
import os
import yaml

import logging
import logging.config



logger = logging.getLogger(__name__)

logging.basicConfig( disable_existing_loggers=False,format='%(asctime)s %(name)s:%(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

logger.info("Start Run")

filename = "/edge/Scratch/Test01/GMCZ_Scenes/GMCZ0022/clips4sale/edgeinter11/clips/GMCZ0022_1920x1080x6000_final.mp4"

cfg = open("/Users/colin/Documents/Appcelerator_Studio_Workspace/JobCard/example/config.yaml",'r')
config = yaml.load(cfg)
    
location = "clips4sale"
account = "edge001"
path = "clips"


job.filetransfer(config, location, account, filename, path)

logger.info("End Run")