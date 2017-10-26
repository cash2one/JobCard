#/bin/python
'''
Created on Oct 18, 2017

@author: colin
'''

if __name__ == '__main__':
    pass

import sys
from sys import exit

try:
    from lxml import etree
    print("running with lxml.etree")
except ImportError:
    print "error loading library lxml"

    
    
root = etree.Element("Project")

email = etree.SubElement(root, "email")
email.text = ("myemail@domain.com")
password = etree.SubElement(root, "password")
password.text = ("SillyPassword")
locales = etree.SubElement(root, "locales")
language1 = etree.SubElement(locales,'Language',ID="1")

picture = etree.SubElement(language1, "picture")
picture.text = ("C:\Mixed\Upload\BF3.png")



et = etree.ElementTree(root)
et.write(sys.stdout, pretty_print=True)