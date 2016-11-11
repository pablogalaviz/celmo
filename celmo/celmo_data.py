'''
Created on 7 Nov 2016

@author: pablo
'''
from celmo.io.files import *

import gc 
import h5py
import logging
import numpy as np
import os

def parse_par(k,v):
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

    class constants:
        def __init__(self):
            '''Defines physical constants in CGS units '''
            self.Avogadro = 6.0221366516751604e+23
            self.Boltzmann = 1.3806504e-16
            self.Stefan_Boltzmann =  5.67051e-05
            self.speed_of_light = 29979245800.0
            self.Planck=6.62606896e-27



    """Common Envelope Luminosity Module Data container """
    def __init__ (self, directory_name,mode = 'a'):
        
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
            except:
                logging.error("No field Total Energy found.")
                logging.exception('')
                exit(1)
    
    
        particle_position_x = data['particle_position_x']*self.get_parameter('length_units')
        particle_position_y = data['particle_position_y']*self.get_parameter('length_units')
        particle_position_z = data['particle_position_z']*self.get_parameter('length_units')

        x = data['x']*self.get_parameter('length_units')
        y = data['y']*self.get_parameter('length_units')
        z = data['z']*self.get_parameter('length_units')

        self.set_basic_fields(density, energy, particle_position_x, particle_position_y, particle_position_z,x,y,z)

         
    def set_basic_fields(self,density,energy,particle_position_x,particle_position_y,particle_position_z,x,y,z):

        pressure = energy*density*(self.get_parameter('gamma')-1)

        self.set_field('density', np.reshape(density,  self.get_parameter('grid_size') ))
        self.set_field('energy',  np.reshape(energy,   self.get_parameter('grid_size') ))
        self.set_field('pressure',np.reshape(pressure, self.get_parameter('grid_size') ))
    
        self.set_field('particle_position_x',particle_position_x)
        self.set_field('particle_position_y',particle_position_y)
        self.set_field('particle_position_z',particle_position_z)

        xx = np.reshape(x, self.get_parameter('grid_size') )
        yy = np.reshape(y, self.get_parameter('grid_size') )
        zz = np.reshape(z, self.get_parameter('grid_size') )

        self.set_field('x', xx)
        self.set_field('y', yy)
        self.set_field('z', zz)

        dx=np.diff(xx, axis=0)
        dy=np.diff(yy, axis=1)
        dz=np.diff(zz, axis=2)
        
        dxx=np.concatenate((dx,np.array([dx[-1,:,:]])),axis=0)
        dyy=np.concatenate((dy,np.transpose(np.array([dy[:,-1,:]]),(1,0,2))),axis=1)
        dzz=np.concatenate((dz,np.transpose(np.array([dz[:,:,-1]]),(1,2,0))),axis=2)

        self.set_field('dx', dxx)
        self.set_field('dy', dyy)
        self.set_field('dz', dzz)


        self.save()


        
    def set_enzo_directory(self,enzo_directory_name):
        self.enzo_directory_name = enzo_directory_name
        

    def set_parameter(self,name,val):
        
        arr=np.array([val])

        logging.debug("setting parameter: "+name+" = "+str(val))
    
        if self.parameter_exists(name):
            self.data_hdf5['parameters/'+name][0] = arr
        else:
            self.data_hdf5.create_dataset('parameters/'+name,data=arr)
        
    def get_parameter(self,name):
        try:
            return self.data_hdf5['parameters/'+name][0]
        except:
            logging.warning("There is not parameter: %s"%name)
            return None

        

    def calculate_derivated_units(self):
        logging.debug("length units: %f", self.get_parameter('length_units'))
        logging.debug("time units: %f", self.get_parameter('time_units'))

        self.set_parameter('speed_units',self.get_parameter('length_units')/self.get_parameter('time_units'))
        self.set_parameter('energy_units',self.get_parameter('speed_units')**2)  #Energy Density 
        self.set_parameter('pressure_units',self.get_parameter('energy_units')*self.get_parameter('density_units'))


    def set_field(self,name,val):
        if self.exists(name):
            self.data_hdf5['fields/'+name][...] = val
        else:
            self.data_hdf5.create_dataset('fields/'+name,data=val)

    def get_field(self,name):
        try:
            return np.array(self.data_hdf5['fields/'+name])
        except:
            logging.warning("Field %s is not defined."%name)


    def save(self):
        self.data_hdf5.flush()


    def exists(self,name):
        return 'fields/'+name in self.data_hdf5

    def parameter_exists(self,name):
        return 'parameters/'+name in self.data_hdf5

    def get_field_1d(self, name, axis=0 ):
        try:
            field=self.get_field(self, name)
            if axis==0:
                return field[:,self.par.grid_size[1]/2,self.par.grid_size[2]/2]
            elif axis==1:
                return field[self.par.grid_size[0]/2,:,self.par.grid_size[2]/2]
            elif axis==2:
                return field[self.par.grid_size[0]/2,self.par.grid_size[1]/2,:]
            else:
                logging.warning("Axis %s out of range."%str(axis))
        except:
            logging.warning("Field %s is not defined."%name)


    def append_grid(self):
        if len(self.grid2append)>0:
            self.grid.append(self.grid2append)
    
    
    
    def new_grid(self,_id):        
        self.append_grid()
        self.grid2append = dict()
        self.grid2append['id'] = _id

    def push(self,k,v):
        self.grid2append[k]=v
    
    
    def __getitem__(self, args):

        if isinstance(args, str):
            narg=1
        else:
            narg=len(args)
            
        if narg > 5:
            raise Exception('Error trying to access grid. Wrong number of arguments: %d. Number of arguments should be less than 5 '%narg)

        if narg == 1:
            return self.getitem_1(args)


    def getitem_1(self,field):
        
        for grid in self.grid:
            data_file=self.enzo_directory_name+'/'+os.path.basename(grid['BaryonFileName'])
            file_exists(data_file,must_exist=True) 
            f = h5py.File(data_file, "r")
            for v in f.values():
                if field in v: 
                    yield (grid, np.array(v[field]))
