import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
  
logger = logging.getLogger(__name__)
sh = logging.StreamHandler()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s','%m-%d %H:%M:%S')
sh.setFormatter(formatter)
logger.addHandler(sh)