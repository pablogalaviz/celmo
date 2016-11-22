from scipy import integrate

import logging
import numpy as np 


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


def normalize_temperature(cel_data,t1):
    
    '''
    |
    | Function that "normalize the temperature"  
    | 
    |
    |  Parameters
    |  ----------
    |  cel_data : celmo data 
    |  t1 : temperature 
    |  
    |  Returns
    |  -------
    |
    |  min(t1,Teff)  : minimum between the effective temperature and the actual temperature 
    |
    '''
    return min(t1,cel_data.get_parameter('Teff'))
    

def compute_optical_depth(cel_data) :

    '''
    |
    | Function that computes the optical depth 
    | 
    |  Notation
    |  ----------
    |  m,p   : minus, plus
    |  X,Y,Z : each direction 
    |  optical_depth_pX refers to each optical depth ray in direction +X  
    |
    |  Parameters
    |  ----------
    |  cel_data : celmo data with optical depth in each direction      
    |  
    |  Returns
    |  -------
    |
    |  None  : the new fields are saved in celmo data  
    |
    '''


    if cel_data.exists('optical_depth_mX') and \
    cel_data.exists('optical_depth_pX') and \
    cel_data.exists('optical_depth_mY') and \
    cel_data.exists('optical_depth_pY') and \
    cel_data.exists('optical_depth_mZ') and \
    cel_data.exists('optical_depth_pZ') and \
    cel_data.exists('optical_depth_one'):
        logging.info("Found optical depth.")

        return
 
    logging.info("Computing optical depth.")

    Nx=int(cel_data.get_parameter('grid_size')[0])
    Ny=int(cel_data.get_parameter('grid_size')[1])
    Nz=int(cel_data.get_parameter('grid_size')[2])

    Nmax = np.max([Nx,Ny,Nz])

    optical_depth_mZ = np.zeros(cel_data.get_int_parameter('grid_size'))
    optical_depth_pZ = np.zeros(cel_data.get_int_parameter('grid_size'))

    optical_depth_mY = np.zeros(cel_data.get_int_parameter('grid_size'))
    optical_depth_pY = np.zeros(cel_data.get_int_parameter('grid_size'))

    optical_depth_mX = np.zeros(cel_data.get_int_parameter('grid_size'))
    optical_depth_pX = np.zeros(cel_data.get_int_parameter('grid_size'))

    optical_depth_one = np.zeros(cel_data.get_int_parameter('grid_size'))
    
    x = cel_data.get_field('x')
    y = cel_data.get_field('y')
    z = cel_data.get_field('z')
    attenuation = cel_data.get_field('attenuation')
    temperature = cel_data.get_field('temperature')

    for indx_1 in np.arange(Nmax) :
        for indx_2 in np.arange(Nmax) :
            if indx_1 < Nx and indx_2 < Ny :

                optical_depth_mZ[indx_1,indx_2] = integrate.cumtrapz(-attenuation[indx_1,indx_2],z[indx_1,indx_2],initial=0)*cel_data.get_parameter('length_units') 
                optical_depth_pZ[indx_1,indx_2] = -optical_depth_mZ[indx_1,indx_2]+optical_depth_mZ[indx_1,indx_2,-1]

                #Face -Z 
                indx_exterior = optical_depth_mZ[indx_1,indx_2] >= -1
                indx_od1 = np.sum(indx_exterior)

                if indx_od1 > Nz -3:
                    indx_od1 = Nz -1
                if indx_od1 < 2 : 
                    indx_od1 = 0


                temperature[indx_1,indx_2,indx_od1] = normalize_temperature(cel_data,temperature[indx_1,indx_2,indx_od1])
                optical_depth_mZ[indx_1,indx_2,indx_od1] = 0
                optical_depth_one[indx_1,indx_2,indx_od1-1] = -1


                #Face +Z 
                indx_exterior = optical_depth_pZ[indx_1,indx_2] >= -1
                indx_od1 = np.sum(indx_exterior)

                if indx_od1 > Nz -3:
                    indx_od1 = Nz -1
                if indx_od1 < 2 : 
                    indx_od1 = 0

                temperature[indx_1,indx_2,-indx_od1-1] = normalize_temperature(cel_data,temperature[indx_1,indx_2,-indx_od1-1])
                optical_depth_pZ[indx_1,indx_2,-indx_od1-1] = 0
                optical_depth_one[indx_1,indx_2,-indx_od1] = -1


            if indx_1 <= Nx and indx_2 <= Nz :
                optical_depth_mY[indx_1,:,indx_2] = integrate.cumtrapz(-attenuation[indx_1,:,indx_2],y[indx_1,:,indx_2],initial=0)*cel_data.get_parameter('length_units')
                optical_depth_pY[indx_1,:,indx_2] = -optical_depth_mY[indx_1,:,indx_2]+optical_depth_mY[indx_1,-1,indx_2]


                #Face -Y 
                indx_exterior = optical_depth_mY[indx_1,:,indx_2] >= 0
                indx_od1 = np.sum(indx_exterior)
                if indx_od1 > Ny -3:
                    indx_od1 = Ny -1
                if indx_od1 < 2 : 
                    indx_od1 = 0


                temperature[indx_1,indx_od1,indx_2] = normalize_temperature(cel_data,temperature[indx_1,indx_od1,indx_2])
                optical_depth_mY[indx_1,indx_od1,indx_2] = 0
                optical_depth_one[indx_1,indx_od1-1,indx_2] = -1


                #Face +Y 
                indx_exterior = optical_depth_pY[indx_1,:,indx_2] >= -1
                indx_od1 = np.sum(indx_exterior)
                if indx_od1 > Ny -3:
                    indx_od1 = Ny -1
                if indx_od1 < 2 : 
                    indx_od1 = 0

                temperature[indx_1,-indx_od1-1,indx_2] = normalize_temperature(cel_data,temperature[indx_1,-indx_od1-1,indx_2])
                optical_depth_pY[indx_1,-indx_od1-1,indx_2] = 0
                optical_depth_one[indx_1,-indx_od1,indx_2] = -1

            if indx_1 <= Ny and indx_2 <= Nz :
                optical_depth_mX[:,indx_1,indx_2] = integrate.cumtrapz(-attenuation[:,indx_1,indx_2],x[:,indx_1,indx_2],initial=0)*cel_data.get_parameter('length_units')
                optical_depth_pX[:,indx_1,indx_2] = -optical_depth_mX[:,indx_1,indx_2]+optical_depth_mX[-1,indx_1,indx_2]

                #Face -X 
                indx_exterior = optical_depth_mX[:,indx_1,indx_2] >= -1
                indx_od1 = np.sum(indx_exterior)

                if indx_od1 > Nx-3:
                    indx_od1 = Nx-1
                if indx_od1 < 2 : 
                    indx_od1 = 0

                temperature[indx_od1,indx_1,indx_2] = normalize_temperature(cel_data,temperature[indx_od1,indx_1,indx_2])
                optical_depth_mX[indx_od1,indx_1,indx_2] = 0
                optical_depth_one[indx_od1-1,indx_1,indx_2] = -1



                #Face +X 
                indx_exterior = optical_depth_pX[:,indx_1,indx_2] >= -1
                indx_od1 = np.sum(indx_exterior)

                if indx_od1 > Nx-3:
                    indx_od1 = Nx-1
                if indx_od1 < 2 : 
                    indx_od1 = 0

                temperature[-indx_od1-1,indx_1,indx_2] = normalize_temperature(cel_data,temperature[-indx_od1-1,indx_1,indx_2])
                optical_depth_pX[-indx_od1-1,indx_1,indx_2] = 0
                optical_depth_one[-indx_od1,indx_1,indx_2] = -1


    cel_data.set_field('optical_depth_mX',optical_depth_mX) 
    cel_data.set_field('optical_depth_pX',optical_depth_pX) 

    cel_data.set_field('optical_depth_mY',optical_depth_mY) 
    cel_data.set_field('optical_depth_pY',optical_depth_pY) 

    cel_data.set_field('optical_depth_mZ',optical_depth_mZ) 
    cel_data.set_field('optical_depth_pZ',optical_depth_pZ) 

    cel_data.set_field('optical_depth_one',optical_depth_one)

    cel_data.set_field('temperature_normalized',temperature)
    
    cel_data.save()
