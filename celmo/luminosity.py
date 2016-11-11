import logging
import numpy as np 
import os 

'''
Created on 11 Nov 2016

@author: Pablo Galaviz
'''


def compute_luminosity(cel_data,output_path) :


    dx=cel_data.get_field('dx')
    dy=cel_data.get_field('dy')
    dz=cel_data.get_field('dz')

    dxu = np.unique(dx)
    dyu = np.unique(dy)
    dzu = np.unique(dz)
    dxy = dxu*dyu
    dyz = dyu*dzu
    dxz = dxu*dzu

    Lum_B_mX = np.sum(cel_data.get_field('EFD_B_mX'))*dyz
    Lum_B_pX = np.sum(cel_data.get_field('EFD_B_pX'))*dyz
    Lum_B_mY = np.sum(cel_data.get_field('EFD_B_mY'))*dxz
    Lum_B_pY = np.sum(cel_data.get_field('EFD_B_pY'))*dxz
    Lum_B_mZ = np.sum(cel_data.get_field('EFD_B_mZ'))*dxy
    Lum_B_pZ = np.sum(cel_data.get_field('EFD_B_pZ'))*dxy

    Lum_V_mX = np.sum(cel_data.get_field('EFD_V_mX'))*dyz
    Lum_V_pX = np.sum(cel_data.get_field('EFD_V_pX'))*dyz
    Lum_V_mY = np.sum(cel_data.get_field('EFD_V_mY'))*dxz
    Lum_V_pY = np.sum(cel_data.get_field('EFD_V_pY'))*dxz
    Lum_V_mZ = np.sum(cel_data.get_field('EFD_V_mZ'))*dxy
    Lum_V_pZ = np.sum(cel_data.get_field('EFD_V_pZ'))*dxy
                                                                                              
    Lum_I_mX = np.sum(cel_data.get_field('EFD_I_mX'))*dyz
    Lum_I_pX = np.sum(cel_data.get_field('EFD_I_pX'))*dyz
    Lum_I_mY = np.sum(cel_data.get_field('EFD_I_mY'))*dxz
    Lum_I_pY = np.sum(cel_data.get_field('EFD_I_pY'))*dxz
    Lum_I_mZ = np.sum(cel_data.get_field('EFD_I_mZ'))*dxy
    Lum_I_pZ = np.sum(cel_data.get_field('EFD_I_pZ'))*dxy


    Solar_L = 3.839e33
    logging.info("\tBolometric Luminosity -X: %e -- %f",Lum_B_mX, Lum_B_mX/Solar_L)
    logging.info("\tBolometric Luminosity +X: %e -- %f",Lum_B_pX, Lum_B_pX/Solar_L)
    logging.info("\tBolometric Luminosity -Y: %e -- %f",Lum_B_mY, Lum_B_mY/Solar_L)
    logging.info("\tBolometric Luminosity +Y: %e -- %f",Lum_B_pY, Lum_B_pY/Solar_L)
    logging.info("\tBolometric Luminosity -Z: %e -- %f",Lum_B_mZ, Lum_B_mZ/Solar_L)
    logging.info("\tBolometric Luminosity +Z: %e -- %f",Lum_B_pZ, Lum_B_pZ/Solar_L)

    logging.info("\tR Band Luminosity -X: %e -- %f",Lum_V_mX, Lum_V_mX/Solar_L)
    logging.info("\tR Band Luminosity +X: %e -- %f",Lum_V_pX, Lum_V_pX/Solar_L)
    logging.info("\tR Band Luminosity -Y: %e -- %f",Lum_V_mY, Lum_V_mY/Solar_L)
    logging.info("\tR Band Luminosity +Y: %e -- %f",Lum_V_pY, Lum_V_pY/Solar_L)
    logging.info("\tR Band Luminosity -Z: %e -- %f",Lum_V_mZ, Lum_V_mZ/Solar_L)
    logging.info("\tR Band Luminosity +Z: %e -- %f",Lum_V_pZ, Lum_V_pZ/Solar_L)

    logging.info("\tI Band Luminosity -X: %e -- %f",Lum_I_mX, Lum_I_mX/Solar_L)
    logging.info("\tI Band Luminosity +X: %e -- %f",Lum_I_pX, Lum_I_pX/Solar_L)
    logging.info("\tI Band Luminosity -Y: %e -- %f",Lum_I_mY, Lum_I_mY/Solar_L)
    logging.info("\tI Band Luminosity +Y: %e -- %f",Lum_I_pY, Lum_I_pY/Solar_L)
    logging.info("\tI Band Luminosity -Z: %e -- %f",Lum_I_mZ, Lum_I_mZ/Solar_L)
    logging.info("\tI Band Luminosity +Z: %e -- %f",Lum_I_pZ, Lum_I_pZ/Solar_L)


    cel_data.set_parameter("Luminosity/Bolometric/minusX",Lum_B_mX)
    cel_data.set_parameter("Luminosity/Bolometric/plusX",Lum_B_pX)

    cel_data.set_parameter("Luminosity/Bolometric/minusY",Lum_B_mY)
    cel_data.set_parameter("Luminosity/Bolometric/plusY",Lum_B_pY)

    cel_data.set_parameter("Luminosity/Bolometric/minusZ",Lum_B_mZ)
    cel_data.set_parameter("Luminosity/Bolometric/plusZ",Lum_B_pZ)

    cel_data.set_parameter("Luminosity/VBand/minusX",Lum_V_mX)
    cel_data.set_parameter("Luminosity/VBand/plusX",Lum_V_pX)

    cel_data.set_parameter("Luminosity/VBand/minusY",Lum_V_mY)
    cel_data.set_parameter("Luminosity/VBand/plusY",Lum_V_pY)

    cel_data.set_parameter("Luminosity/VBand/minusZ",Lum_V_mZ)
    cel_data.set_parameter("Luminosity/VBand/plusZ",Lum_V_pZ)

    cel_data.set_parameter("Luminosity/IBand/minusX",Lum_I_mX)
    cel_data.set_parameter("Luminosity/IBand/plusX",Lum_I_pX)

    cel_data.set_parameter("Luminosity/IBand/minusY",Lum_I_mY)
    cel_data.set_parameter("Luminosity/IBand/plusY",Lum_I_pY)

    cel_data.set_parameter("Luminosity/IBand/minusZ",Lum_I_mZ)
    cel_data.set_parameter("Luminosity/IBand/plusZ",Lum_I_pZ)

    cel_data.save()

    
    luminosity_file=output_path+"/Luminosity.gp"

    time=cel_data.get_parameter('time')
    
    new_entry = np.array([[time, Lum_B_mX, Lum_B_pX, Lum_B_mY, Lum_B_pY, Lum_B_mZ, Lum_B_pZ, Lum_V_mX, Lum_V_pX, Lum_V_mY, Lum_V_pY, Lum_V_mZ, Lum_V_pZ, Lum_I_mX, Lum_I_pX, Lum_I_mY, Lum_I_pY, Lum_I_mZ, Lum_I_pZ]])
    
    if os.path.exists(luminosity_file):
    
        lum_data = np.loadtxt(luminosity_file )

        if len(lum_data.shape) == 1:
            lum_data = lum_data.reshape([1, lum_data.shape[0] ])
        t = lum_data[:,0]

        indx = np.abs(t-new_entry[0,0]) < 1e-7
        lum_data=np.delete(lum_data, np.where(indx), axis=0)

        if len(lum_data) > 0:
            lum_data=np.append(lum_data, new_entry, axis=0)
            lum_data=np.sort(lum_data, axis=0)
        else:
            lum_data = new_entry
            
    else:
        lum_data = new_entry

        

    header_txt="Time\t\t L_bol[-X] (erg/s)\t\t L_bol[+X] (erg/s)\t\t L_bol[-Y] (erg/s)\t\t L_bol[+Y] (erg/s)\t\t L_bol[-Z] (erg/s)\t\t L_bol[+Z] (erg/s)\t\t L_V[-X] (erg/s)\t\t L_V[+X] (erg/s)\t\t L_V[-Y] (erg/s)\t\t L_V[+Y] (erg/s)\t\t L_V[-Z] (erg/s)\t\t L_V[+Z] (erg/s)\t\t L_I[-X] (erg/s)\t\t L_I[+X] (erg/s)\t\t L_I[-Y] (erg/s)\t\t L_I[+Y] (erg/s)\t\t L_I[-Z] (erg/s)\t\t L_I[+Z] (erg/s)"
    np.savetxt(luminosity_file, lum_data,fmt='%1.8e',delimiter='\t',header=header_txt)


