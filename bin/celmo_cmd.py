#!/usr/bin/env python2.7

'''
Main execution function

@author: Pablo Galaviz
'''
from celmo import *

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
    parser.add_argument('-ow','--overwrite',type=str ,help='Overwrite data')
    parser.add_argument('-yt','--yt_reader' ,action='store_true' ,help='Use yt to read the data')
    parser.add_argument('--directory',type=str ,help='Project output directory')
    parser.add_argument('--datafiles',type=str ,help='Path to the root data files directory')
    parser.add_argument('-Teff','--effective_temperature',type=float,help='Effective temperature of the star at t=0')
    parser.add_argument('-mu','--mol_weight',type=float ,help='Mean molecular weight', default = 1.2 )
    parser.add_argument('-rho0','--floor_density',type=float ,help='Vacuum density', default = 1e-9 )

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
        model_settings=parse_settings(config['model'],args)
    except:
        logging.exception("Error in parameters file")
        exit(errno.EINVAL)

    project_directory = expand_path(output_settings.get('directory'), 'results') 
        
    validate_and_make_directory(project_directory, backup=output_settings.getboolean('overwrite'))
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
    
    if model_settings.get("effective_temperature") == None:
        logging.error("Missing parameter effective_temperature")
        return -1
    
    effective_temperature=model_settings.getfloat("effective_temperature")     
    mol_weight=model_settings.getfloat("mol_weight")     
    floor_density=model_settings.getfloat("floor_density")     
    
    for d in data:
        celmo_data = read_enzo_data(project_directory,d,args.yt_reader)
        compute_temperature(effective_temperature, mol_weight,floor_density, celmo_data)
        compute_opacity(celmo_data)
        compute_filters(celmo_data)
        compute_attenuation(celmo_data)
        compute_optical_depth(celmo_data)
        compute_brightness(celmo_data)
        compute_extinction_factor(celmo_data)
        compute_energy_flux_density(celmo_data)
        compute_luminosity(celmo_data,project_directory)

    
    
if __name__ == '__main__':
    exit(main())
    