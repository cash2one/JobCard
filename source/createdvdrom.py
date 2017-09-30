'''
Created on Sep 29, 2017

@author: colin
'''

def createdatadvd(in_dir,out_dir, volid, mkisofs, runflag, verbose, components):
#===============================================================================
#  Create a DVD using mkisofs from an assembly directory
#  This module can be called stand alone as well
#    Arg1 = Source Directory
#    Arg2 = Where the ISO will be Written
#    Arg3 = Volume ID
#    Arg4 = full path to mkisofs binary
#    Arg5 = Run Flag = true: do the command; false: show the command
#    Arg6 = Verbose output (true or false)
#    Arg7 = Array of Components to use
#
#    Return true or false (success or failure), + error messages
#===============================================================================

#===============================================================================
# Logic
# This code will take the output from "Assembly" 
#    then create a scratch folder with all of the components
#    then create a ISO from the components
#        placing the ISO image and a description.txt file into the deliveries folder
#
#===============================================================================
 
#------------------------------------------------------------------------------ 
#    Global Variable
#------------------------------------------------------------------------------ 
    status = False
    CMDtemplate = "$MKISOFS "
    log_message = ''

    print "Make Data DVD"
    print in_dir + out_dir

    #===========================================================================
    # Results
    # Arg 1 ; true or false [success or failure]
    # Arg 2 ; text string of Command
    # Arg 3 ; text string of Messages (Verbose or not)
    #===========================================================================
    
    return

