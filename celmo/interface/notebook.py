import logging
import sys
from ipywidgets import interact, interact_manual, fixed

logFormatter = logging.Formatter('CELMO %(levelname)s [%(asctime)s] | %(message)s')
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.INFO)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

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
