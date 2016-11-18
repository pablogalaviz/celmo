import logging
import sys
from ipywidgets import interact, interact_manual, fixed

logFormatter = logging.Formatter('CELMO %(levelname)s [%(asctime)s] | %(message)s')
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.INFO)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

