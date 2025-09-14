import logging
from .log import logger
from walytis_beta_embedded import ipfs
from kivy import platform
import os

IPFS_LOG_TOPIC = f"endra_logs_{platform}"
IPFS_LOG_PEERS = []


class IPFSHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        ipfs.pubsub.publish(IPFS_LOG_TOPIC, f"{log_entry}\n")


ipfs_handler = IPFSHandler()
ipfs_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)

logger.addHandler(ipfs_handler)

PEERS_FILEPATH = os.path.join(os.path.dirname(__file__), "ipfs_bootstrap_peers.txt")
for peer in IPFS_LOG_PEERS:
    peer_id = [part for part in peer.split("/") if part][-1]
    if peer_id == ipfs.peer_id:
        continue
    logger.info(f"endra_app.endra_logging: connecting to  peer {peer}")
    ipfs.peers.connect(peer)
