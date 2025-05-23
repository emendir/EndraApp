from loguru import logger
from walytis_beta_embedded import ipfs
from kivy import platform
IPFS_LOG_TOPIC = f"endra_logs_{platform}"
IPFS_LOG_PEERS = [
    
]


def log_to_ipfs(log_message):
    ipfs.pubsub.publish(IPFS_LOG_TOPIC, log_message)


logger.add(log_to_ipfs)

import os
PEERS_FILEPATH=os.path.join(os.path.dirname(__file__), "ipfs_bootstrap_peers.txt")
for peer in IPFS_LOG_PEERS:
    peer_id = [part for part in peer.split("/") if part][-1]
    if peer_id == ipfs.peer_id:
        continue
    logger.info(f"endra_app.endra_logging: connecting to  peer {peer}")
    ipfs.peers.connect(peer)
    
    
