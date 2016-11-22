import logging

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

def compute_attenuation(cel_data):
    '''
    |
    | Function that computes the attenuation of a radiation field. 
    | Attenuation is the product of opacity and density
    |
    |  Parameters
    |  ----------
    |  cel_data : celmo data with fields opacity and density   
    |  
    |  Returns
    |  -------
    |
    |  None  : the new field is saved in celmo data  
    |
    '''
    
    if cel_data.exists('attenuation'):
        logging.info("Found attenuation field.")
        return
        
    logging.info("Computing attenuation field.")

    cel_data.set_field('attenuation', cel_data.get_field('opacity')*cel_data.get_field('density'))
    cel_data.save()