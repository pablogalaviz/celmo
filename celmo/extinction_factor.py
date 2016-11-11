'''
Created on 10 Nov 2016

@author: Pablo Galaviz
'''
import logging
import numpy as np 

def compute_extinction_factor(cel_data):
    
    if cel_data.exists('extinction_factor_mX') and \
    cel_data.exists('extinction_factor_pX') and \
    cel_data.exists('extinction_factor_mY') and \
    cel_data.exists('extinction_factor_pY') and \
    cel_data.exists('extinction_factor_mZ') and \
    cel_data.exists('extinction_factor_pZ') :
        logging.info("Found extinction factor")
        return 
        
    logging.info("Computing extinction factor")
 
    cel_data.set_field('extinction_factor_mX', np.exp(cel_data.get_field('optical_depth_mX')))
    cel_data.set_field('extinction_factor_pX', np.exp(cel_data.get_field('optical_depth_pX')))

    cel_data.set_field('extinction_factor_mY', np.exp(cel_data.get_field('optical_depth_mY')))
    cel_data.set_field('extinction_factor_pY', np.exp(cel_data.get_field('optical_depth_pY')))

    cel_data.set_field('extinction_factor_mZ', np.exp(cel_data.get_field('optical_depth_mZ')))
    cel_data.set_field('extinction_factor_pZ', np.exp(cel_data.get_field('optical_depth_pZ')))
