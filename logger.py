import logging

def createLog(name):
    logging.basicConfig(filename = f'{name}.log',level = logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
    console_log = logging.StreamHandler()
    console_log.setLevel(logging.DEBUG)
    format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_log.setFormatter(format)
    logging.getLogger('').addHandler(console_log)
    logging.info('Session created')


