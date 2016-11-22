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


def get_epilog():
    return ''' 
=============================
    Author: Pablo Galaviz
    pablo.galaviz@me.com 
=============================

License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html> 
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
    '''




def parse_settings(config_data,arg_data):
            
    for k,v in arg_data.__dict__.items():
        kk = k.replace('_',' ')
        if v != None and kk in config_data: 
            config_data.update({kk:str(v)})
            
    return config_data



def display_welcome():
    
    logging.info("=========================================================")
    logging.info(" ______     ______     __         __    __     ______    ")
    logging.info("/\  ___\   /\  ___\   /\ \       /\ \"-./  \   /\  __ \  ")
    logging.info("\ \ \____  \ \  __\   \ \ \____  \ \ \-./\ \  \ \ \/\ \  ")
    logging.info(" \ \_____\  \ \_____\  \ \_____\  \ \_\ \ \_\  \ \_____\ ")
    logging.info("  \/_____/   \/_____/   \/_____/   \/_/  \/_/   \/_____/ ")
    logging.info("====================== Celmo  16.11 =====================")
    logging.info("")
    logging.info("")
    logging.info("                    Author: Pablo Galaviz     ")
    logging.info("                    Pablo.Galaviz@me.com      ")
    logging.info("")
    logging.info("")
    logging.info("====================== Celmo  16.11 =====================")
    logging.info("")
    logging.info("")

