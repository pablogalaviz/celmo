from celmo.io.files import *
from celmo.celmo_data import CelmoData, parse_par

import os 
import numpy as np 
import h5py

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



def import_enzo_data(par_file,cel_data):
    '''Imports ENZO data-set and save it in a celmo-data object'''
    
    with open(par_file) as f:
        for line in f:
            raw_info = line.strip().split('=') 
            if len(raw_info)>1:
                k,v = parse_par(raw_info[0], raw_info[1])
                if k != "":
                    cel_data.set_parameter(k,v)

    cel_data.set_enzo_directory( os.path.abspath( os.path.dirname(par_file )))

    cel_data.calculate_derivated_units()

                    
    hierarchy_file = par_file+'.hierarchy.hdf5'
    hf = h5py.File(hierarchy_file, "r")
    
    grid_list=list()
    id_list=list()
    for k,v in hf.items():
        if isinstance(v,h5py.Group):
            for kk in v.keys():
                grid_list.append(k+'/'+kk+'/GridData')
                id_list.append(kk)
                GridLeftEdge = v[kk+'/GridLeftEdge'][:]
                GridRightEdge = v[kk+'/GridRightEdge'][:]
                ii=v[kk+'/GridStartIndex'][:]
                ee=v[kk+'/GridEndIndex'][:]
                N=ee-ii
                
                dd    = (GridRightEdge-GridLeftEdge)/N
                start = GridLeftEdge+0.5*dd
                stop  = GridRightEdge-0.5*dd


                xx = np.linspace(start=start[0], stop=stop[0], num=N[0]+1,endpoint=True)*cel_data.get_parameter('length_units')
                yy = np.linspace(start=start[1], stop=stop[1], num=N[1]+1,endpoint=True)*cel_data.get_parameter('length_units')
                zz = np.linspace(start=start[2], stop=stop[2], num=N[2]+1,endpoint=True)*cel_data.get_parameter('length_units')
                                
                x,y,z = np.meshgrid(xx,yy,zz,indexing='ij')

    for grid_data in grid_list:
        link_data=hf.get(grid_data, default=None, getclass=False, getlink=True)
        data_filename = os.path.dirname(par_file)+'/'+os.path.basename(link_data.filename)
        data_f = h5py.File(data_filename, "r")
        for k,v in data_f.items():
            if k in id_list:        
                density=read_data_set(v,'Density')*cel_data.get_parameter('density_units')
                try:
                    energy=read_data_set(v,'Total_Energy')*cel_data.get_parameter('energy_units')
                except:
                    logging.warning("No field Total_Energy found, trying TotalEnergy.")
                    try:
                        energy=read_data_set(v,'TotalEnergy')*cel_data.get_parameter('energy_units')
                        logging.info("Found TotalEnergy field.")
                    except:
                        logging.error("Missing Total Energy field.")
                        logging.exception('')
                        exit(1)

                particle_position_x = read_data_set(v,'particle_position_x')*cel_data.get_parameter('length_units')
                particle_position_y = read_data_set(v,'particle_position_y')*cel_data.get_parameter('length_units')
                particle_position_z = read_data_set(v,'particle_position_z')*cel_data.get_parameter('length_units')
        
        
                cel_data.set_basic_fields(density, energy, particle_position_x, particle_position_y, particle_position_z,x,y,z)

                
                
    return cel_data



def read_data_set(grp, field):    
    ds = grp[field][:]
    return ds.transpose()


    

def read_enzo_data(project_path, data_path, yt_reader=False):
    
    cdata = CelmoData(project_path+'/'+os.path.basename(data_path))
    
    load_yt = False

    if yt_reader:    
        try:
            from yt.mods import load
            load_yt = True
        except ImportError:
            logging.warn("Import error: yt, using native reader")
            load_yt = False
        
        
    if load_yt:
        pf = load(data_path)
        #read the raw data 
        cdata.set_from_yt(pf)
        return cdata
    else:
        return import_enzo_data(data_path,cdata)
        