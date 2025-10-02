from .config import BOOTSTRAP_PEERS_PATH, PEER_MONITOR_PATH
from ipfs_tk_peer_monitor import PeerMonitor
from walytis_beta_embedded import ipfs
import os

BOOTSTRAP_PEERS = {
    "12D3KooWPjNuQHAHzgBEdK9cHzP2hjFgJRbjE3r11vby9hs5eC7o": [
        "/ip4/5.252.54.190/tcp/4001",
        "/ip6/2605:a140:3017:8450::1/tcp/4001",
    ],
}


def load_bootstrap_config():
    if os.path.exists(BOOTSTRAP_PEERS_PATH):
        with open(BOOTSTRAP_PEERS_PATH, "r") as file:
            lines = file.readlines()
        for line in lines:
            BOOTSTRAP_PEERS.append(line)


load_bootstrap_config()
bootstrap_peer_monitor = PeerMonitor(ipfs, PEER_MONITOR_PATH)
for peer_id, multiaddrs in BOOTSTRAP_PEERS.items():
    bootstrap_peer_monitor.get_or_add_peer(peer_id, multiaddrs)
