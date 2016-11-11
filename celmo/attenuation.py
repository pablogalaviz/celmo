import logging

'''
Created on 9 Nov 2016

@author: Pablo Galaviz
'''

def compute_attenuation(cel_data):
    if cel_data.exists('attenuation'):
        logging.info("Found attenuation field.")
        return
        
    logging.info("Computing attenuation field.")

    cel_data.set_field('attenuation', cel_data.get_field('opacity')*cel_data.get_field('density'))
    cel_data.save()