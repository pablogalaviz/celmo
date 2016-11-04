'''
Console interface

@author: Pablo Galaviz
'''

import errno
import logging
import os 
import shutil

def get_epilog():
    return ''' 
=============================
    Author: Pablo Galaviz
    pablo.galaviz@me.com 
=============================

License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html> 
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
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

def parse_settings(config_data,arg_data):
            
    for k,v in arg_data.__dict__.items():
        kk = k.replace('_',' ')
        if v != None and kk in config_data: 
            config_data.update({kk:str(v)})
            
    return config_data

def validate_and_make_directory(_directory):

    _directory = _directory.replace('//', '/')
    
    if os.path.exists(_directory):
        if not os.path.isdir(_directory):
            logging.error("The output %s is a regular file",_directory)
            exit(errno.EIO)
        else:
            if os.path.exists(_directory+'_prev'):
                shutil.rmtree(_directory+'_prev')
            shutil.move(_directory, _directory+'_prev')

    try:
        logging.info("Making directory %s.",_directory)
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


def display_welcome():
    
    logging.info("=========================================================")
    logging.info(" ______     ______     __         __    __     ______    ")
    logging.info("/\  ___\   /\  ___\   /\ \       /\ \"-./  \   /\  __ \  ")
    logging.info("\ \ \____  \ \  __\   \ \ \____  \ \ \-./\ \  \ \ \/\ \  ")
    logging.info(" \ \_____\  \ \_____\  \ \_____\  \ \_\ \ \_\  \ \_____\ ")
    logging.info("  \/_____/   \/_____/   \/_____/   \/_/  \/_/   \/_____/ ")
    logging.info("====================== Celmo  16.11 =====================")
    logging.info("")
    logging.info("")
    logging.info("                    Author: Pablo Galaviz     ")
    logging.info("                    Pablo.Galaviz@me.com      ")
    logging.info("")
    logging.info("")
    logging.info("====================== Celmo  16.11 =====================")
    logging.info("")
    logging.info("")

