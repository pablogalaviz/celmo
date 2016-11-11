import logging


def compute_brightness(cel_data):

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
