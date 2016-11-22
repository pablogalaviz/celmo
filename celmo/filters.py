import logging
import numpy as np
import os 

from scipy import integrate


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


def compute_filters(cel_data):

    '''
    |
    | Function that computes the filter factors 
    | 
    |  Notation
    |  ----------
    |  I,V :  I band, V band
    | 
    |
    |  Parameters
    |  ----------
    |  cel_data : celmo data      
    |  
    |  Returns
    |  -------
    |
    |  None  : the new fields are saved in celmo data  
    |
    '''

    if cel_data.exists('filter_factorI') and  cel_data.exists('filter_factorV'):
        logging.info("Found filters")
        
        return

    if not cel_data.exists('temperature') :
        logging.error("Temperature fields does not exists. Temperature is necessary to compute the filters.")
        exit(1)

    filters_directory=os.path.dirname(__file__)+"/data/filters/"
    
    if not os.path.exists(filters_directory):
        logging.error("Filters directory %s not found")
        exit(1)
    
    files = os.listdir(filters_directory)
    temperature=cel_data.get_field('temperature').flatten()
    for f in files:
        if f.find('.celf') >0:
            _data_file = filters_directory+f
            cel_filter = CelmoFilter(_data_file, cel_data)                
            filter_factor =np.reshape( cel_filter.Factors(temperature),cel_data.get_int_parameter('grid_size'))
            if f.find('I.celf') > 0 :
                cel_data.set_field('filter_factorI', filter_factor)
            elif f.find('V.celf') > 0 :
                cel_data.set_field('filter_factorV', filter_factor)

    cel_data.save()



class CelmoFilter(object) : 

    '''
    |
    | Common Envelope Luminosity Module Filters.
    |
    '''


    def __init__(self, _data_file,cel_data):

        '''
        |
        |  This c
        |
        |  Parameters
        |  ----------
        |  _data_file : a path to the filter table    
        |  cel_data   : celmo data container
        |
        |  Returns
        |  -------
        |
        |  None  : the new fields are saved in celmo data  
        |
        '''

        self.cel_data = cel_data

        logging.info("Reading filter table from file: %s",_data_file) 
        dd = np.loadtxt(_data_file)
        x = dd[:,0]
        self.y = dd[:,1]
        self.xiT = self.Lambda2xiT(x)


    def f  (self,x) :
        return x**3/(np.exp(x)-1)

        
    def Lambda2xiT(self,lmbd) :
        #nu, transform lmbd form angstrom to m
        nu = self.cel_data.const.speed_of_light/(lmbd*1e-8)

        hik = self.cel_data.const.Planck/self.cel_data.const.Boltzmann
        return nu*hik


    def filterAt(self, TT):
        iT= 1.0/TT
        return self.xiT*iT

    def getFilterFactor(self,T):
        if T ==1 :
            return 0
        xi = self.filterAt(T)

        return 15*np.abs(integrate.simps(self.f(xi)*self.y, xi, even='avg'))/np.pi**4


    def Factors(self, TT) : 
        dims = TT.shape
        data = np.ones_like(TT)
        for indx_x in np.arange(dims[0]) :
            data[indx_x] = self.getFilterFactor(TT[indx_x])

        return data
