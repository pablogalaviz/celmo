#!/usr/bin/env python2.7

'''
Main execution function

@author: Pablo Galaviz
'''

from celmo.interface.api import * 
from celmo.util.data import find_datafiles

try:
    from yt.mods import load
except ImportError:
    from celmo.util.data import load
    
    
def main():    
    
    start_time = time.time()
    
    logFormatter = logging.Formatter('CELMO %(levelname)s [%(asctime)s] | %(message)s')

    rootLogger = logging.getLogger()

    rootLogger.setLevel(logging.INFO)
    
    epilog_text=get_epilog()
    
    parser = argparse.ArgumentParser(description='CELMO, Common Envelope Light Module', epilog=epilog_text,formatter_class=argparse.RawDescriptionHelpFormatter)    
    parser.add_argument('input_file', help='Input parameter file.',metavar='intput.par')
    parser.add_argument('-s','--silent',action='store_true' ,help='Starts in silent mode, no message will be output.')
    parser.add_argument('-d','--debug' ,action='store_true' ,help='Shows debug info')
    parser.add_argument('--directory',type=str ,help='Project output directory')
    parser.add_argument('--datafiles',type=str ,help='Path to the root data files directory')

    args = parser.parse_args()
    config = configparser.ConfigParser()
    consoleHandler = logging.StreamHandler(sys.stdout)

    if  args.debug:
        rootLogger.setLevel(logging.DEBUG)
    
    if  args.silent:
        consoleHandler.setLevel(logging.ERROR)    
        
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    if file_exists(args.input_file, must_exist=True):
        config.read(args.input_file, encoding='utf-8')
        
    try:
        output_settings=parse_settings(config['output'],args)
    except:
        logging.exception("Error in parameters file")
        exit(errno.EINVAL)

    project_directory = expand_path(output_settings.get('directory'), 'results') 
    
    validate_and_make_directory(project_directory)
    shutil.copy(args.input_file, project_directory )

    fileHandler = logging.FileHandler(project_directory+"/Celmo.log",mode='w')
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    display_welcome()        

    logging.info('Project directory: %s', project_directory)

    if output_settings.get('datafiles') == None:
        logging.error("missing input data directory")
        return errno.EIO
        
    data_directory = expand_path(output_settings.get('datafiles'), '') 

    data=find_datafiles(data_directory)
    
    if len(data) == 0:
        logging.warn("No enzo data found in: %s",data_directory)
        return errno.EIO
        
    pf = load(data[0])
    
    
    
if __name__ == '__main__':
    exit(main())
    