import logging

logger = logging.getLogger(__name__)

filehandler = logging.FileHandler("logfile.log")
logger.addHandler(filehandler)

logger.info("This is info.")
logger.debug("This is debug..")
logger.error("This is error..")
logger.warning("This is warning..")
logger.critical("This is critical..")
