import os
from .config import (
    USE_BRENTHY,
    IPFS_REPO_DIR,
    WALYTIS_BETA_DATA_DIR,
    PRIVATE_BLOCKS_DATA_DIR,
)

if True:  # SENSITIVE IMPORT ORDERS
    if USE_BRENTHY:
        os.environ["WALYTIS_BETA_API_TYPE"] = "WALYTIS_BETA_BRENTHY_API"

    else:
        os.environ["IPFS_TK_MODE"] = "EMBEDDED"
        os.environ["IPFS_REPO_DIR"] = IPFS_REPO_DIR
        os.environ["AUTO_LOAD_BAP_MODULES"] = "false"
        os.environ["WALYTIS_BETA_API_TYPE"] = "WALYTIS_BETA_DIRECT_API"
        os.environ["WALYTIS_BETA_DATA_DIR"] = WALYTIS_BETA_DATA_DIR
    print("Set environ:", os.environ["WALYTIS_BETA_API_TYPE"])

    import brenthy_tools_beta  # depends on AUTO_LOAD_BAP_MODULES environment var

    # disable excessive logging, is slow in flatpak packages
    brenthy_tools_beta.log.RECORD_INFO = False
    brenthy_tools_beta.log.RECORD_DEBUG = False

    if not USE_BRENTHY:
        import walytis_beta_embedded

        walytis_beta_embedded.set_appdata_dir(WALYTIS_BETA_DATA_DIR)
        from brenthy_tools_beta import log

        print(
            "BRENTHY LOG:", os.path.abspath(os.path.join(log.LOG_DIR, log.LOG_FILENAME))
        )
        # print("BRENTHY LOG:",os.path.abspath( log.get_log_file_path()))

    from .ipfs_logging import ENABLE_PUBSUB_LOGGING

    print("IPFS Logging:", ENABLE_PUBSUB_LOGGING)
os.environ["PRIVATE_BLOCKS_DATA_DIR"] = PRIVATE_BLOCKS_DATA_DIR
