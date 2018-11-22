# gebruik log om je *al* je dingen te loggen. (debug, info, warning, error en critical)
import logging, configparser

config = configparser.ConfigParser()
config.read('settings.conf')


def __init__():
    pass


logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(levelname)-8s %(asctime)s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.DEBUG)

# disable all loggers from different files
logging.getLogger('asyncio').setLevel(logging.WARN)
logging.getLogger('asyncio.coroutines').setLevel(logging.WARN)
logging.getLogger('websockets.server').setLevel(logging.WARN)
logging.getLogger('websockets.protocol').setLevel(logging.WARN)


# https://docs.python.org/3/library/logging.html#logging-levels
# 0 = debug
# 20 = info en erger
logger.setLevel(config["General"].getint("log_level"))

log = logger

# check if file is run as module
if __name__ != "__main__":
    __init__()
else:
    crit("script should be run as module")
