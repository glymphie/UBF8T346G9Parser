import logging


class Logger:
    """Universal logger
    """

    @property
    def logger(self):
        logging.basicConfig(format='%(levelname)s [%(asctime)s] %(message)s', level=logging.DEBUG)
        logger = logging.getLogger()
        logger.setLevel('WARNING')
        return logger
