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


def compute_extinction_factor(cel_data):

    '''
    |
    | Function that computes the extinction factor $ef := \\exp(-\\tau)$
    | 
    |  Notation
    |  ----------
    |  m,p   : minus, plus
    |  X,Y,Z : each direction 
    |  extinction_factor_mX refers to each extinction factor ray in direction -X  
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

    
    if cel_data.exists('extinction_factor_mX') and \
    cel_data.exists('extinction_factor_pX') and \
    cel_data.exists('extinction_factor_mY') and \
    cel_data.exists('extinction_factor_pY') and \
    cel_data.exists('extinction_factor_mZ') and \
    cel_data.exists('extinction_factor_pZ') :
        logging.info("Found extinction factor")
        return 
        
    logging.info("Computing extinction factor")
 
    #optical_depth_??: it is in fact -\\tau, m refers to minus, p to plus  and X,Y,Z to the direction 
    cel_data.set_field('extinction_factor_mX', np.exp(cel_data.get_field('optical_depth_mX')))
    cel_data.set_field('extinction_factor_pX', np.exp(cel_data.get_field('optical_depth_pX')))

    cel_data.set_field('extinction_factor_mY', np.exp(cel_data.get_field('optical_depth_mY')))
    cel_data.set_field('extinction_factor_pY', np.exp(cel_data.get_field('optical_depth_pY')))

    cel_data.set_field('extinction_factor_mZ', np.exp(cel_data.get_field('optical_depth_mZ')))
    cel_data.set_field('extinction_factor_pZ', np.exp(cel_data.get_field('optical_depth_pZ')))

    cel_data.save()
