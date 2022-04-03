import logging


class Logger:
    """Universal logger
    """

    @property
    def logger(self):
        logging.basicConfig(format='[%(asctime)s] %(levelname)s - %(message)s', 
                            datefmt='%d-%m-%Y %H:%M:%S',
                            level=logging.DEBUG)
        logger = logging.getLogger()
        logger.setLevel('INFO')
        return logger
