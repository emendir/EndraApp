from ipfs_tk_transmission.log import logger_transm, logger_conv
from threading import Thread
from .config import ENABLE_PUBSUB_LOGGING, APPDATA_DIR
import logging
from .log import logger_endra
from walytis_beta_embedded import ipfs
from kivy import platform
import os
from walytis_identities.log import (
    logger_walid,
    logger_dm,
    logger_gdm,
    logger_ckm,
    logger_gdm_join,
    logger_datatr,
    logger_dmws,
    logger_keys,
    MillisecondFormatter,
    LOG_TIMESTAMP_FORMAT,
)
from walytis_offchain.log import logger_waloff

IPFS_LOG_TOPIC = f"endra_logs_{platform}"


class IPFSHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        ipfs.pubsub.publish(IPFS_LOG_TOPIC, f"{log_entry}\n")


ipfs_handler = IPFSHandler()
ipfs_handler.setFormatter(
    MillisecondFormatter(
        "%(asctime)s [%(levelname)-8s] %(name)-16s | %(message)s",
        datefmt=LOG_TIMESTAMP_FORMAT,
    )
)

if ENABLE_PUBSUB_LOGGING:
    logger_endra.info("PUBSUB LOGGING enabled.")
    logger_endra.debug(IPFS_LOG_TOPIC)
    logger_endra.addHandler(ipfs_handler)
    logger_walid.addHandler(ipfs_handler)
    logger_dm.addHandler(ipfs_handler)
    logger_gdm.addHandler(ipfs_handler)
    logger_ckm.addHandler(ipfs_handler)
    logger_gdm_join.addHandler(ipfs_handler)
    logger_datatr.addHandler(ipfs_handler)
    logger_dmws.addHandler(ipfs_handler)
    logger_keys.addHandler(ipfs_handler)

    logger_waloff.addHandler(ipfs_handler)


class IPFSHandler2(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        ipfs.pubsub.publish(f"{IPFS_LOG_TOPIC}-IPFS_TK", f"{log_entry}\n")


ipfs_handler_2 = IPFSHandler2()
ipfs_handler_2.setFormatter(
    MillisecondFormatter(
        "%(asctime)s [%(levelname)-8s] %(name)-16s | %(message)s",
        datefmt=LOG_TIMESTAMP_FORMAT,
    )
)
logger_conv.setLevel(logging.DEBUG)
logger_transm.setLevel(logging.DEBUG)

logger_transm.addHandler(ipfs_handler_2)
logger_conv.addHandler(ipfs_handler_2)
