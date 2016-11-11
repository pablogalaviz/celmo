'''
Created on 8 Nov 2016

@author: Pablo Galaviz
'''
import logging
import numpy as np

def compute_temperature( Teff, mu, rho0,cel_data):

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

