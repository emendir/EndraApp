from threading import Thread
from .config import ENABLE_PUBSUB_LOGGING, APPDATA_DIR
import logging
from .log import logger_endra as logger
from walytis_beta_embedded import ipfs
from kivy import platform
import os

IPFS_LOG_TOPIC = f"endra_logs_{platform}"


class IPFSHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        ipfs.pubsub.publish(IPFS_LOG_TOPIC, f"{log_entry}\n")


ipfs_handler = IPFSHandler()
ipfs_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)

if ENABLE_PUBSUB_LOGGING:
    logger.addHandler(ipfs_handler)
