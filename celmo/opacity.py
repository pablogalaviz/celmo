from scipy.interpolate import RectBivariateSpline
from celmo.io.files import *

import logging
import numpy as np
import os
import gc

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


def compute_opacity(cel_data):

    '''
    |
    | Function that computes the opacity 
    | 
    |
    |  Parameters
    |  ----------
    |  cel_data : celmo data with temperature and density       
    |  
    |  Returns
    |  -------
    |
    |  None  : the new fields are saved in celmo data  
    |
    '''


    if cel_data.exists('opacity') :
        logging.info("Found opacity field.")
        return 

    logging.info("Computing opacity field.")

    opacity_directory=os.path.dirname(__file__)+"/data/opacity_tables/"
    
    if not os.path.exists(opacity_directory):
        logging.error('Opacity files in not found!, directory %s does not exists ', opacity_directory)
        exit(errno.ENOENT)

    if not cel_data.exists('temperature'):
        logging.error("Temperature field does not exists. The temperature is necessary to compute the opacity.")
        exit(1)

    
    OpacityData = Opacity(opacity_directory+"lowT_af94_gn93_z2m2_x70.data",opacity_directory+"OP_z2m2_x70.data")

    grid_size=[int(i) for i in cel_data.get_parameter('grid_size')]
    logT = np.zeros(grid_size, dtype='float64')

    temperature = cel_data.get_field('temperature')

    indx= temperature > 1 
    logT[indx]=np.log10(temperature[indx]) 

    #test limits 
    indxLT= logT<3
    indxUT= logT>8.7

    density=cel_data.get_field('density')
    logR=np.log10(density)-3*logT+18            
    indxLR= logR<-7
    indxUR= logR>1

    logT[indxLT] = 3
    logT[indxUT] = 8.7

    logR[indxLR] = -7
    logR[indxUR] = 1

    opacity=np.reshape( np.power(10,OpacityData.ev(logT.flatten(),logR.flatten())), grid_size)
    
    del OpacityData
    gc.collect()
    
    indxOut= density <= cel_data.get_parameter('rho0')
    
    opacity[indxOut] = 0

    cel_data.set_field('opacity',opacity)
    cel_data.save()


class Opacity(object):

    '''
    |
    | Common Envelope Luminosity Module Opacity interpolation.
    |
    '''


    def __init__(self, _file_nameL, _file_nameH):
        
        '''
        |
        |  Reads the opacity from tables and create a numpy rectangular bivariate spline interpolation.
        |
        '''


        self.opintL = self.interpolateOpacityTable(_file_nameL)    
        self.opintH = self.interpolateOpacityTable(_file_nameH)
        logging.info("Opacity interpolation ready")


    def interpolateOpacityTable(self,file_name):

        '''
        |  Parameters
        |  ----------
        |  file_name : opacity table file     
        |  
        |  Returns
        |  -------
        |
        |  RectBivariateSpline  : rectangular bivariate spline  
        |
        '''

        flines = open(file_name, 'r').readlines()

        logging.info("Reading opacity from file: %s",file_name)

        num_of_lines = len(flines)
        Np1 = len( flines[int(num_of_lines/2)].split())
        N=Np1-1

        logT=np.empty(0)
        logR=np.empty(0)
        Values=np.empty(0)

        for line in flines:
            arr_line = line.split()
            if len(arr_line) == Np1: 
                raw_data = [float(x) for x in arr_line]
                logT = np.append(logT,raw_data[0])
                if len(Values)==0:
                    Values = [np.array(raw_data[1:])]
                else:
                    new_val = [np.array(raw_data[1:])]
                    Values = np.append(Values,new_val,axis=0)   
            elif len(arr_line) == N:
                logR = np.array([float(x) for x in arr_line])


        return RectBivariateSpline(logT, logR,Values)

    

    def ev(self, logT, logR):
 
        '''
        |
        |  Evaluates the opacity in a grid 
        |
        |  Notation
        |  ----------
        |  T   : temperature 
        |  Rho : density 
        |  R   : exp(log(Rho) - 3*log(T) + 18) 
        |
        |
        |  Parameters
        |  ----------
        |  logT : log(T)      
        |  logR : log(R)      
        |  
        |  Returns
        |  -------
        |
        |  RectBivariateSpline  : rectangular bivariate spline  
        |
        '''

        
        if len(logT) != len(logR):
            logging.error("Incompatible opacity arrays...")
            exit()

        opacity_data = np.zeros_like(logT)

        #L: -7 <= logR <= 1.0; 3.00 <= logT <= 4.1
        #H: -8 <= logR <= 1.0; 3.75 <= logT <= 8.7

        logging.debug("Split temperature-density domain ")


        indxOpL = (-7 <= logR)*(logR <= 1.0)*(3 <= logT)*(logT <= 4.1)
        indxOpH = (-8 <= logR)*(logR <= 1.0)*(3.75 <= logT)*(logT <= 8.7)
        indxOpHmL = indxOpH - indxOpH*indxOpL 

        logging.debug("Computing high temperature opacity")

        if indxOpHmL.sum() > 0 :
            opacity_data[indxOpHmL] = self.opintH.ev(logT[indxOpHmL],logR[indxOpHmL] )

        logging.debug("Computing low temperature opacity")

        if indxOpL.sum() > 0 :
            opacity_data[indxOpL] = self.opintL.ev(logT[indxOpL],logR[indxOpL] )

        logging.debug("done")

        return opacity_data

