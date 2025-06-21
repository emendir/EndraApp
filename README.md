## Endra App

_P2P Messenger_

Based on IPFS, the Walytis database blockchain, and Walytis-Identities DID management technologies, this peer to peer messenger support multiple devices per user, and group chats.

## Run From Source

Install Prerequisites:

```sh
./install_prereqs.sh
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

```sh
USE_PANGO=0 python .
```

### Environment Variables

- `USE_PANGO` (defaults to true on Linux): Use the Pango text provider to enable broader character & emoji text rendering support
- `USE_BRENTHY` (defaults to false): Instead of running an embedded IPFS and Walytis node, use the separately running system services for IPFS and Walytis. This enables faster loading times. To set up IPFS & Walytis in this way, [install Brenthy](https://github.com/emendir/BrenthyAndWalytis)

## DevOps

For speedy starting and termination of the app, on Linux, [install Brenthy](https://github.com/emendir/BrenthyAndWalytis) to run Walytis & IPFS as a systemd service.
Then run Endra with:

```sh
USE_PANGO=0 USE_BRENTHY=1 python tests/test_app.py
```

Pressing Ctrl+C in the terminal should promptly close the Endra app.

Rerunning the app this way overwrites the app's appdata with a cache stored in `tests/appdata`, so that it doesn't matter if the app crashes and corrupts its appdata.

To save the current appdata, close the endra app, and run:

```sh
tests/update_appdata.sh
```

From now on, every time you run `tests/test_app.py`, the new appdata state will be loaded.

To reset the appdata, run:

```sh
rm -rf tests/appdata
```
