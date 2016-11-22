
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


def compute_temperature( Teff, mu, rho0,cel_data):


    '''
    |
    | Function that computes the temperature 
    | 
    |  Notation
    |  ----------
    |  temperature_vacuum   : temperature including the hot vacuum 
    |  temperature          : temperature without the hot vacuum (exterior is set to 0)
    |
    |  Parameters
    |  ----------
    |  Teff : effective temperature    
    |  mu   : mean molecular weight    
    |  Rho0 : density flor    
    |  cel_data : celmo data with optical depth in each direction      
    |  
    |  Returns
    |  -------
    |
    |  None  : the new fields are saved in celmo data  
    |
    '''


    if cel_data.exists('temperature_vacuum') and cel_data.exists('temperature'):
        logging.info("Found temperature.")
        return

    if not (cel_data.exists('energy') and cel_data.exists('density') ) :
        logging.error("Base fields do not exists. Energy density and density are necessary to compute the temperature.")
        exit(1)

    logging.info("Computing the temperature using T=M(gamma-1)U/R with:")
    logging.info("\tTeff=%0.2f, mu=%.2f and floor density rho0=%e",Teff,mu,rho0)
    cel_data.set_parameter('Teff', Teff)
    cel_data.set_parameter('mu', mu)
    cel_data.set_parameter('rho0', rho0)


    Ri=1.0/(cel_data.const.Avogadro*cel_data.const.Boltzmann)
    M=1.00797/mu
    Mgm1Ri = M*(cel_data.get_parameter("gamma")-1)*Ri  #number of H atoms

    temperature_vacuum = cel_data.get_field('energy')*Mgm1Ri
    
    cel_data.set_field('temperature_vacuum',temperature_vacuum )

    indxOut= (cel_data.get_field('density') <= rho0)*(temperature_vacuum > Teff)
    
    temperature = np.copy(temperature_vacuum)
    temperature[indxOut] = 1
    cel_data.set_field('temperature',temperature)
    
    cel_data.save()

