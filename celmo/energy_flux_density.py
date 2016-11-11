import logging
import numpy as np 

from scipy import integrate

'''
Created on 10 Nov 2016

@author: Pablo Galaviz
'''

def integrate_dI(_dI, _r, _dr):

    indx_dL = _dI>1
    DeltaL= _dr[indx_dL].sum()
    
    if DeltaL > 0 :
        return 4*integrate.trapz(_dI,_r)/DeltaL
    else :
        return 0


def compute_energy_flux_density(cel_data):

    EFD_bool = cel_data.exists('EFD_B_mX') and cel_data.exists('EFD_B_pX')
    EFD_bool = cel_data.exists('EFD_B_mY') and cel_data.exists('EFD_B_pY') and EFD_bool 
    EFD_bool = cel_data.exists('EFD_B_mZ') and cel_data.exists('EFD_B_pZ') and EFD_bool 

    EFD_bool = cel_data.exists('EFD_V_mX') and cel_data.exists('EFD_V_pX') and EFD_bool
    EFD_bool = cel_data.exists('EFD_V_mY') and cel_data.exists('EFD_V_pY') and EFD_bool 
    EFD_bool = cel_data.exists('EFD_V_mZ') and cel_data.exists('EFD_V_pZ') and EFD_bool 

    EFD_bool = cel_data.exists('EFD_I_mX') and cel_data.exists('EFD_I_pX') and EFD_bool
    EFD_bool = cel_data.exists('EFD_I_mY') and cel_data.exists('EFD_I_pY') and EFD_bool 
    EFD_bool = cel_data.exists('EFD_I_mZ') and cel_data.exists('EFD_I_pZ') and EFD_bool 


    if EFD_bool :
        logging.info("Found energy flux density field.")
        return 

    logging.info("Computing energy flux density field.")


    domain_dimensions = cel_data.get_parameter('grid_size')
    Nmax = int(np.max(domain_dimensions))
            

    EFD_B_mX = np.zeros(domain_dimensions[1:3])
    EFD_B_pX = np.zeros(domain_dimensions[1:3])

    EFD_B_mY = np.zeros(domain_dimensions[0:3:2])
    EFD_B_pY = np.zeros(domain_dimensions[0:3:2])

    EFD_B_mZ = np.zeros(domain_dimensions[0:2])
    EFD_B_pZ = np.zeros(domain_dimensions[0:2])

    EFD_V_mX = np.zeros(domain_dimensions[1:3])
    EFD_V_pX = np.zeros(domain_dimensions[1:3])

    EFD_V_mY = np.zeros(domain_dimensions[0:3:2])
    EFD_V_pY = np.zeros(domain_dimensions[0:3:2])

    EFD_V_mZ = np.zeros(domain_dimensions[0:2])
    EFD_V_pZ = np.zeros(domain_dimensions[0:2])

    EFD_I_mX = np.zeros(domain_dimensions[1:3])
    EFD_I_pX = np.zeros(domain_dimensions[1:3])

    EFD_I_mY = np.zeros(domain_dimensions[0:3:2])
    EFD_I_pY = np.zeros(domain_dimensions[0:3:2])

    EFD_I_mZ = np.zeros(domain_dimensions[0:2])
    EFD_I_pZ = np.zeros(domain_dimensions[0:2])

    dBrightnessB=cel_data.get_field('dBrightnessB')
    dBrightnessI=cel_data.get_field('dBrightnessI')
    dBrightnessV=cel_data.get_field('dBrightnessV')

    extinction_factor_mX=cel_data.get_field('extinction_factor_mX')
    extinction_factor_pX=cel_data.get_field('extinction_factor_pX')

    extinction_factor_mY=cel_data.get_field('extinction_factor_mY')
    extinction_factor_pY=cel_data.get_field('extinction_factor_pY')

    extinction_factor_mZ=cel_data.get_field('extinction_factor_mZ')
    extinction_factor_pZ=cel_data.get_field('extinction_factor_pZ')

    x=cel_data.get_field('x')
    y=cel_data.get_field('y')
    z=cel_data.get_field('z')

    dx=cel_data.get_field('dx')
    dy=cel_data.get_field('dy')
    dz=cel_data.get_field('dz')

    intensityB_mZ = dBrightnessB*extinction_factor_mZ
    intensityV_mZ = dBrightnessV*extinction_factor_mZ
    intensityI_mZ = dBrightnessI*extinction_factor_mZ

    intensityB_pZ = dBrightnessB*extinction_factor_pZ
    intensityV_pZ = dBrightnessV*extinction_factor_pZ
    intensityI_pZ = dBrightnessI*extinction_factor_pZ

    intensityB_mY = dBrightnessB*extinction_factor_mY
    intensityV_mY = dBrightnessV*extinction_factor_mY
    intensityI_mY = dBrightnessI*extinction_factor_mY

    intensityB_pY = dBrightnessB*extinction_factor_pY
    intensityV_pY = dBrightnessV*extinction_factor_pY
    intensityI_pY = dBrightnessI*extinction_factor_pY

    intensityB_mX = dBrightnessB*extinction_factor_mX
    intensityV_mX = dBrightnessV*extinction_factor_mX
    intensityI_mX = dBrightnessI*extinction_factor_mX

    intensityB_pX = dBrightnessB*extinction_factor_pX
    intensityV_pX = dBrightnessV*extinction_factor_pX
    intensityI_pX = dBrightnessI*extinction_factor_pX



    for indx_1 in xrange(Nmax) :
        for indx_2 in xrange(Nmax) :
            if indx_1 <= domain_dimensions[0] and indx_2 <= domain_dimensions[1] :
                
                zz=z[indx_1,indx_2]
                dzz=dz[indx_1,indx_2]
                
                EFD_B_mZ[indx_1,indx_2] = integrate_dI(intensityB_mZ[indx_1,indx_2],zz,dzz)
                EFD_V_mZ[indx_1,indx_2] = integrate_dI(intensityV_mZ[indx_1,indx_2],zz,dzz)
                EFD_I_mZ[indx_1,indx_2] = integrate_dI(intensityI_mZ[indx_1,indx_2],zz,dzz)


                EFD_B_pZ[indx_1,indx_2] = integrate_dI(intensityB_pZ[indx_1,indx_2],zz,dzz)
                EFD_V_pZ[indx_1,indx_2] = integrate_dI(intensityV_pZ[indx_1,indx_2],zz,dzz)
                EFD_I_pZ[indx_1,indx_2] = integrate_dI(intensityI_pZ[indx_1,indx_2],zz,dzz)



            if indx_1 <= domain_dimensions[0] and indx_2 <= domain_dimensions[2] :

                yy=y[indx_1,:,indx_2]
                dyy=dy[indx_1,:,indx_2]
                
                EFD_B_mY[indx_1,indx_2] = integrate_dI(intensityB_mY[indx_1,:,indx_2],yy,dyy)
                EFD_V_mY[indx_1,indx_2] = integrate_dI(intensityV_mY[indx_1,:,indx_2],yy,dyy)
                EFD_I_mY[indx_1,indx_2] = integrate_dI(intensityI_mY[indx_1,:,indx_2],yy,dyy)


                EFD_B_pY[indx_1,indx_2] = integrate_dI(intensityB_pY[indx_1,:,indx_2],yy,dyy)
                EFD_V_pY[indx_1,indx_2] = integrate_dI(intensityV_pY[indx_1,:,indx_2],yy,dyy)
                EFD_I_pY[indx_1,indx_2] = integrate_dI(intensityI_pY[indx_1,:,indx_2],yy,dyy)



            if indx_1 <= domain_dimensions[1] and indx_2 <= domain_dimensions[2] :

                xx=x[:,indx_1,indx_2]
                dxx=dx[:,indx_1,indx_2]
                
                EFD_B_mX[indx_1,indx_2] = integrate_dI(intensityB_mX[:,indx_1,indx_2],xx,dxx)
                EFD_V_mX[indx_1,indx_2] = integrate_dI(intensityV_mX[:,indx_1,indx_2],xx,dxx)
                EFD_I_mX[indx_1,indx_2] = integrate_dI(intensityI_mX[:,indx_1,indx_2],xx,dxx)


                EFD_B_pX[indx_1,indx_2] = integrate_dI(intensityB_pX[:,indx_1,indx_2],xx,dxx)
                EFD_V_pX[indx_1,indx_2] = integrate_dI(intensityV_pX[:,indx_1,indx_2],xx,dxx)
                EFD_I_pX[indx_1,indx_2] = integrate_dI(intensityI_pX[:,indx_1,indx_2],xx,dxx)


    cel_data.set_field('EFD_B_mX', EFD_B_mX)
    cel_data.set_field('EFD_B_pX', EFD_B_pX)
    cel_data.set_field('EFD_V_mX', EFD_V_mX)
    cel_data.set_field('EFD_V_pX', EFD_V_pX)
    cel_data.set_field('EFD_I_mX', EFD_I_mX)
    cel_data.set_field('EFD_I_pX', EFD_I_pX)

    cel_data.set_field('EFD_B_mY', EFD_B_mY)
    cel_data.set_field('EFD_B_pY', EFD_B_pY)
    cel_data.set_field('EFD_V_mY', EFD_V_mY)
    cel_data.set_field('EFD_V_pY', EFD_V_pY)
    cel_data.set_field('EFD_I_mY', EFD_I_mY)
    cel_data.set_field('EFD_I_pY', EFD_I_pY)

    cel_data.set_field('EFD_B_mZ', EFD_B_mZ)
    cel_data.set_field('EFD_B_pZ', EFD_B_pZ)
    cel_data.set_field('EFD_V_mZ', EFD_V_mZ)
    cel_data.set_field('EFD_V_pZ', EFD_V_pZ)
    cel_data.set_field('EFD_I_mZ', EFD_I_mZ)
    cel_data.set_field('EFD_I_pZ', EFD_I_pZ)
    
