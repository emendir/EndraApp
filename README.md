## Endra App

A P2P encrypted messenger supporting multiple devices per user.

Endra combines Walytis' peer-to-peer distributed database, WalytisIdentities' identity & cryptography management, and WalytisOffchain's secure data storage & transmission, and WalytisMutability's database editing abstraction to form a fully featured messaging protocol.

It can be used for more than just instant messaging - shared calendars, project management tools and an endless amount of distributed communications systems can be built using it.


## Features

- fully peer to peer, no servers of any kind
- can function independently of internet connectivity
- full end-to-end encryption ephemeral keys, algorithm-agnostic & future-proof
- multiple devices per profile (user account)
- multiple profiles per device
- can be used as a library for embedding into other applications
- will become part of an expandable ecosystem incl. calendar and file-sharing
- [app for desktop and mobile](https://github.com/emendir/EndraApp) (tested on Linux (Ubuntu x86-64) and Android (arm-64))

### Disadvantages

- higher resource usage on user devices compared to conventional messengers

## Documentation

The thorough documentation for this project and the technologies it's based on live in a dedicated repository:

https://github.com/emendir/WalytisTechnologies

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
- `KIVY_NO_CONSOLELOG` (defaults to false): stop kivy logging to console
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

## Related Projects
### The Endra Tech Stack

- [IPFS](https://ipfs.tech):  A p2p communication and content addressing protocol developed by ProtocolLabs.
- [Walytis](https://github.com/emendir/Walytis_Beta): A flexible, lightweight, nonlinear database-blockchain, built on IPFS.
- [WalytisIdentities](https://github.com/emendir/WalytisIdentities): P2P multi-controller cryptographic identity management, built on Walytis.
- [WalytisOffchain](https://github.com/emendir/WalytisOffchain): Secure access-controlled database-blockchain, built on WalytisIdentities.
- [WalytisMutability](https://github.com/emendir/WalytisMutability): A Walytis blockchain overlay featuring block mutability.
- [Endra](https://github.com/emendir/Endra): A p2p encrypted messaging protocol with multiple devices per user, built on Walytis.
- [EndraApp](https://github.com/emendir/EndraApp): A p2p encrypted messenger supporting multiple devices per user, built on Walytis.

### Alternative Technologies
- Berty: a p2p messenger for mobile phones built on IPFS & OrbitDB
