import logging

logger = logging

logger.basicConfig(
    filename='logs/pipeline.log',
    level=logging.DEBUG,
    filemode='a',
    force=True, 
    format="%(asctime)s - %(levelname)s - %(filename)s - "
    "%(funcName)s - %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S"
)

logging.getLogger("urllib3").setLevel(logging.WARNING)