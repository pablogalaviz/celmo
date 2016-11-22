from celmo.io.files import *

import gc 
import h5py
import logging
import numpy as np
import os


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


def parse_par(k,v):
    '''
    |
    | Function that parses Enzo parameters  
    | 
    |
    |  Parameters
    |  ----------
    |  k : key   
    |  v : value   
    |  
    |  Returns
    |  -------
    |
    |  k_new  : new key (lowercase with separator _)  
    |  v_new  : array, number or string   
    |
    '''
    
    if 'initialtime' in k.lower():
        return "time",float(v)
    elif 'topgriddimensions' in k.lower():
        if type(v) == str:
            return 'grid_size',  np.array([float(x) for x in v.split()])
        elif type(v)==np.ndarray:
            return 'grid_size',  v
    elif 'gamma' in k.lower():
        return 'gamma',float(v)
    elif 'massunits' in k.lower():
        return 'mass_units',float(v)
    elif 'densityunits' in k.lower():
        return 'density_units',float(v)
    elif 'timeunits' in k.lower():
        return 'time_units',float(v)
    elif 'lengthunits' in k.lower():
        return 'length_units',float(v)
    elif 'domainleftedge' in k.lower():
        if type(v) == str:
            return 'domain_left_edge',  np.array([float(x) for x in v.split()])
        elif type(v)==np.ndarray:
            return 'domain_left_edge',  v            
    elif 'domainrightedge' in k.lower():
        if type(v) == str:
            return 'domain_right_edge',  np.array([float(x) for x in v.split()])
        elif type(v)==np.ndarray:
            return 'domain_right_edge',  v

    
    return "", 0 
    

class CelmoData(object):

    '''
    |
    | Common Envelope Luminosity Module Data container.
    |
    '''


    class constants:
        def __init__(self):
            '''
            Defines physical constants in CGS units 
            '''
            self.Avogadro = 6.0221366516751604e+23
            self.Boltzmann = 1.3806504e-16
            self.Stefan_Boltzmann =  5.67051e-05
            self.speed_of_light = 29979245800.0
            self.Planck=6.62606896e-27



    def __init__ (self, directory_name,mode = 'a'):

        '''
        |
        | Common Envelope Luminosity Module Data container.
        | A class that stores the necessary data required to compute the 
        | luminosity emitted  from   common  envelope,
        | hydrodynamic  simulations carried  out with  the 3D  hydrodynamic code,
        | Enzo used in unigrid mode
        |
        |  Parameters
        |  ----------
        |  directory_name : a path to store the data in a hdf5 file   
        |
        |  Returns
        |  -------
        |
        |  CelmoData  : celmo data container   
        |
        '''

        
        gc.enable()
        self. directory_name = os.path.dirname(directory_name)
        
        validate_and_make_directory(directory_name,backup=False)
        
        self.const = self.constants()
        self.data_file = directory_name+"/cel_data.h5"
        

        if os.path.exists(self.data_file):
            self.data_hdf5 = h5py.File(self.data_file, mode)
        else:
            self.data_hdf5 = h5py.File(self.data_file, "w")

        self.grid = list()
        self.grid2append = dict()


    def set_from_yt(self,pf):

        '''
        |
        | CelmoData can read the fields from a yt file 
        |
        |  Parameters
        |  ----------
        |  pf : yt file   
        |
        |  Returns
        |  -------
        |
        |  None  : data is saved in a file   
        |
        '''
        
        for k,v in pf.parameters.items():
            kk,vv = parse_par(k, v)   
            if kk != "":         
                self.set_parameter(kk, vv)
        self.calculate_derivated_units()
        
        data=pf.h.all_data()
        
        density=data['Density']*self.get_parameter('density_units')
        try:
            energy=data['Total_Energy']*self.get_parameter('energy_units')
        except:
            logging.warning("No field Total_Energy found, trying TotalEnergy.")
            try:
                energy=data['TotalEnergy']*self.get_parameter('energy_units')
                logging.info("Found TotalEnergy field.")
            except:
                logging.error("Missing Total Energy field.")
                logging.exception('')
                exit(1)
    
    
        particle_position_x = data['particle_position_x']*self.get_parameter('length_units')
        particle_position_y = data['particle_position_y']*self.get_parameter('length_units')
        particle_position_z = data['particle_position_z']*self.get_parameter('length_units')

        x = data['x'] *self.get_parameter('length_units')
        y = data['y'] *self.get_parameter('length_units')
        z = data['z'] *self.get_parameter('length_units')

        self.set_basic_fields(density, energy, particle_position_x, particle_position_y, particle_position_z,x,y,z)

         
    def set_basic_fields(self,density,energy,particle_position_x,particle_position_y,particle_position_z,x,y,z):

        '''
        |
        | Reads the main fields and generate derived date  
        |
        |  Parameters
        |  ----------
        |  density : a flat numpy array 
        |  energy :  a flat numpy array 
        |  particle_position_x : array with the x position of the particles 
        |  particle_position_y : array with the y position of the particles 
        |  particle_position_z : array with the z position of the particles 
        |  x : coordinates in axis x
        |  y : coordinates in axis y
        |  z : coordinates in axis z
        |
        |  Returns
        |  -------
        |
        |  None  : data is saved in a file   
        |
        '''

        pressure = energy*density*(self.get_parameter('gamma')-1)

        grid_size=self.get_int_parameter('grid_size') 

        self.set_field('density', np.reshape(density,  grid_size ))
        self.set_field('energy',  np.reshape(energy,   grid_size ))
        self.set_field('pressure',np.reshape(pressure, grid_size ))
    
        self.set_field('particle_position_x',particle_position_x)
        self.set_field('particle_position_y',particle_position_y)
        self.set_field('particle_position_z',particle_position_z)


        if len(x.shape) == 1:
            x = np.reshape(x, grid_size )
        if len(y.shape) == 1:
            y = np.reshape(y, grid_size )
        if len(z.shape) == 1:
            z = np.reshape(z, grid_size )


        self.set_field('x', x)
        self.set_field('y', y)
        self.set_field('z', z)


        dx=np.unique(np.diff(x, axis=0))
        dy=np.unique(np.diff(y, axis=1))
        dz=np.unique(np.diff(z, axis=2))

        
        dxx=np.ones_like(x)*dx[0]
        dyy=np.ones_like(y)*dy[0]
        dzz=np.ones_like(z)*dz[0]

        self.set_field('dx', dxx)
        self.set_field('dy', dyy)
        self.set_field('dz', dzz)


        self.save()


        
    def set_enzo_directory(self,enzo_directory_name):
        self.enzo_directory_name = enzo_directory_name
        

    def set_parameter(self,name,val):

        '''
        |
        | Stores a scalar parameter in the projects file  
        |
        |  Parameters
        |  ----------
        |  name : scalar name 
        |  val :  value 
        |
        |  Returns
        |  -------
        |
        |  None  : data is saved in a file   
        |
        '''
        
        arr=np.array([val])

        logging.debug("setting parameter: "+name+" = "+str(val))
    
        if self.parameter_exists(name):
            self.data_hdf5['parameters/'+name][0] = arr
        else:
            self.data_hdf5.create_dataset('parameters/'+name,data=arr)
        
    def get_parameter(self,name):
        '''
        |
        | Returns a scalar parameter stored in the projects file  
        |
        |  Parameters
        |  ----------
        |  name : scalar name 
        |
        |  Returns
        |  -------
        |
        |  val or None  : The value of the scalar or None if the scalar does not exists 
        |
        '''
        try:
            return self.data_hdf5['parameters/'+name][0]
        except:
            logging.warning("There is not parameter: %s"%name)
            return None

    def get_int_parameter(self,name):
        '''
        |
        | Returns a integer scalar parameter stored in the projects file  
        |
        |  Parameters
        |  ----------
        |  name : scalar name 
        |
        |  Returns
        |  -------
        |
        |  val or None  : The value of the scalar or None if the scalar does not exists 
        |
        '''
        param=self.get_parameter(name)
        if isinstance(param,np.ndarray):
            return [int(x) for x in param]
        elif isinstance(param,float):
            return int(x)
        else:
            return param
            

    def calculate_derivated_units(self):
        '''
        |
        | Computes speed, energy and pressure units 
        |
        |  Parameters
        |  ----------
        |  None :  internal use 
        |
        |  Returns
        |  -------
        |
        |  None  :  internal use
        |
        '''
        logging.debug("length units: %f", self.get_parameter('length_units'))
        logging.debug("time units: %f", self.get_parameter('time_units'))

        self.set_parameter('speed_units',self.get_parameter('length_units')/self.get_parameter('time_units'))
        self.set_parameter('energy_units',self.get_parameter('speed_units')**2)  #Energy Density 
        self.set_parameter('pressure_units',self.get_parameter('energy_units')*self.get_parameter('density_units'))


    def set_field(self,name,val):
        '''
        |
        | Stores a field in the projects file  
        |
        |  Parameters
        |  ----------
        |  name : field name 
        |  val :  value 
        |
        |  Returns
        |  -------
        |
        |  None  : data is saved in a file   
        |
        '''
        if self.exists(name):
            self.data_hdf5['fields/'+name][...] = val
        else:
            self.data_hdf5.create_dataset('fields/'+name,data=val)

    def get_field(self,name):
        '''
        |
        | Returns a field stored in the projects file  
        |
        |  Parameters
        |  ----------
        |  name : field name 
        |
        |  Returns
        |  -------
        |
        |  val or None  : numpy array or None if the field does not exists 
        |
        '''
        try:
            return np.array(self.data_hdf5['fields/'+name])
        except:
            logging.warning("Field %s is not defined."%name)


    def save(self):
        '''
        |
        | Save the data to the projects file  
        |
        '''
        self.data_hdf5.flush()

    def list_fields(self):
        '''
        |
        | Returns a list with the name of the fields stored in the projects file  
        |
        |  Parameters
        |  ----------
        |  None :  
        |
        |  Returns
        |  -------
        |
        |  list  : a list with the name of the fields 
        |
        '''
        return list(self.data_hdf5['fields'].keys())

    def list_parameters(self):
        '''
        |
        | Returns a list with the name of the scalars stored in the projects file  
        |
        |  Parameters
        |  ----------
        |  None :  
        |
        |  Returns
        |  -------
        |
        |  list  : a list with the name of the scalars 
        |
        '''
        return list(self.data_hdf5['parameters'].keys())


    def exists(self,name):
        '''
        |
        | Test if a field exists in the projects file  
        |
        |  Parameters
        |  ----------
        |  name : name of the field  
        |
        |  Returns
        |  -------
        |
        |  bool  : True if the field exists, else False
        |
        '''
        return 'fields/'+name in self.data_hdf5

    def parameter_exists(self,name):
        '''
        |
        | Test if a scalar exists in the projects file  
        |
        |  Parameters
        |  ----------
        |  name : name of the scalar  
        |
        |  Returns
        |  -------
        |
        |  bool  : True if the scalar exists, else False
        |
        '''
        return 'parameters/'+name in self.data_hdf5

    def get_field_1d(self, name, axis=0 ):
        
        '''
        |
        | Returns a 1d array of a field containing the origin in a given direction  
        |
        |  Parameters
        |  ----------
        |  name : name of the field
        |  axis : 0,1,2 for x,y,z respectively   
        |
        |  Returns
        |  -------
        |
        |  numpy_array  : 1d array with the data 
        |
        '''

        gz = self.get_int_parameter('grid_size')
        
        try:
            field=self.get_field(name)
            if axis==0:
                return field[:,int(gz[1]/2),int(gz[2]/2)]
            elif axis==1:
                return field[int(gz[0]/2),:,int(gz[2]/2)]
            elif axis==2:
                return field[int(gz[0]/2),int(gz[1]/2),:]
            else:
                logging.warning("Axis %s out of range."%str(axis))
        except:
            
            logging.warning("Field %s is not defined."%name)


