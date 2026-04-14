import logging

from chromalog.mark.helpers.simple import error
from chromalog.mark.helpers.simple import important
from chromalog.mark.helpers.simple import success

import chromalog

chromalog.basicConfig(fmt="%(message)s", level=logging.INFO)
logger = logging.getLogger()

filename = r"/var/lib/status"

logger.info("Booting up system: %s", success("OK"))
logger.info("Booting up network: %s", error("FAIL"))
logger.info("Reading file at %s: %s", important(filename), success("OK"))
