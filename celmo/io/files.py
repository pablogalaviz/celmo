import errno
import logging
import numpy as np 
import os
import shutil
import string

'''
//
// Made by Pablo Galaviz
// e-mail  <pablogalavizv@gmail.com>
// 
//  This file is part of CELMO
//
//  CELMO is free software: you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or
//  any later version.
//
//  CELMO is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//
//  You should have received a copy of the GNU General Public License
//  along with CELMO.  If not, see <http://www.gnu.org/licenses/>.
//
'''

def file_exists(data_file, must_exist=False):

    is_dir=False
    if os.path.exists(data_file):
        if not os.path.isdir(data_file):
            return True
        is_dir=True
        
    if must_exist:
        if is_dir:
            logging.error('%s is a directory!', data_file)
        else:
            logging.error('File %s does not exist!', data_file)

        exit(errno.ENOENT)
    else :
        return False

def validate_and_make_directory(_directory, backup=True):

    _directory = _directory.replace('//', '/')
    
    if os.path.exists(_directory):
        if not os.path.isdir(_directory):
            logging.error("The output %s is a regular file",_directory)
            exit(errno.EIO)
        else:
            if os.path.exists(_directory+'_prev'):
                shutil.rmtree(_directory+'_prev')
            if backup:
                shutil.move(_directory, _directory+'_prev')
            else:
                return 
            
    try:
        logging.info("Making directory %s",_directory)
        os.makedirs(_directory)
        return _directory
    except:
        logging.exception('').replace('//', '/')
        exit(errno.EIO)

def expand_path(path, default):
    if path == None:
        path = os.path.abspath(os.path.curdir+'/'+default+'/').replace('//','/')

    if '~' in path:
        path = os.path.expanduser(path)

    if '$' in path:
        path = os.path.expandvars(path)
        
    return os.path.abspath(path)


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


