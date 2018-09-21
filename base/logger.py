import logging
import coloredlogs

coloredlogs.install(level='DEBUG')


FORMAT = '%(asctime)-15s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO, datefmt='%Y-%m-%dT%H:%M:%S')


def get_logger(derive_name_from):
    if hasattr(derive_name_from, 'im_class'):
        name = "{}:{}:{}".format(derive_name_from.__module__,
                                 derive_name_from.im_class.__name__,
                                 derive_name_from.__name__)
    elif callable(derive_name_from):
        name = "{}:{}".format(derive_name_from.__module__,
                              derive_name_from.__name__)
    else:
        name = str(derive_name_from)
    return logging.getLogger(name)
