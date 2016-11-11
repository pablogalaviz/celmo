import string
import os
import numpy as np 

def find_datafiles(directory):
    
    datafile_list=list()
        
    for filename in  os.listdir(directory):
        file_path=os.path.join(directory,filename)
        if os.path.isfile(file_path):   
            if is_enzo_parfile(file_path,filename):
                datafile_list.append(file_path)
        elif os.path.isdir(file_path):
            more_datafiles=find_datafiles(file_path)
            if len(more_datafiles) > 0:
                datafile_list.extend(more_datafiles)
    return datafile_list


def is_enzo_parfile(filepath,filename):
    if len(filename.split('.')) > 1:
        return False
    elif not istextfile(filepath):
        return False
    
    #filepath is a text file 
    #enzo_files have some associated_files enzo_files.*
    #lets try to find them 
    associated_files=list()
    dirname=os.path.dirname(filepath)
    for f in os.listdir(dirname):
        if filename in f and filename != f:
            ext=f.replace(filename+'.','')
            if np.sometrue([x in ext for x in ['cpu','boundary','hierarchy']]):
                associated_files.append(f)
            
    if len(associated_files) > 2:
        #it is very likely that we found an enzo data directory
        return True
    return False


# istextfile & istext from  http://code.activestate.com/recipes/173220/
def istextfile(filename, blocksize = 512):
    return istext(open(filename).read(blocksize))

def istext(s):
    if "\0" in s:
        return 0
    
    if not s:  # Empty files are considered text
        return 1
    
    text_characters = "".join(map(chr, range(32, 127)) + list("\n\r\t\b"))
    _null_trans = string.maketrans("", "")

    # Get the non-text characters (maps a character to itself then
    # use the 'remove' option to get rid of the text characters.)
    t = s.translate(_null_trans, text_characters)

    # If more than 30% non-text characters, then
    # this is considered a binary file
    if len(t)/len(s) > 0.30:
        return 0
    return 1

def load(file):
    pass
