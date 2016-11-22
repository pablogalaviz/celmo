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

def compute_brightness(cel_data):
    '''
    |
    | Function that computes the differential brightness (dB) of a fluid. 
    | dB is $\\sigma T^4$
    |
    |  Parameters
    |  ----------
    |  cel_data : celmo data with field temperature_normalized   
    |  
    |  Returns
    |  -------
    |
    |  None  : the new field is saved in celmo data  
    |
    '''

    if cel_data.exists('dBrightnessB') and cel_data.exists('dBrightnessV') and cel_data.exists('dBrightnessI'):
        logging.info("Found differential brightness field.")
        return

    logging.info("Computing differential brightness field.")

    if not cel_data.exists('temperature_normalized'):
        logging.error("Normalized temperature field does not exists. The temperature is necessary to compute the brightness.")
        exit(1)

    logging.info("Computing differential brightness")        
    dBrightness = (cel_data.get_field('temperature_normalized')**4)*cel_data.const.Stefan_Boltzmann
    cel_data.set_field('dBrightnessB', dBrightness)
    cel_data.set_field('dBrightnessI', dBrightness*cel_data.get_field('filter_factorI'))
    cel_data.set_field('dBrightnessV', dBrightness*cel_data.get_field('filter_factorV'))
    
    cel_data.save()
