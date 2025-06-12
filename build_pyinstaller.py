#!/bin/python
""":"
# Shell: re-execute this script with Python
exec python3 "$0" "$@"
exit 0
"""

from metadata import version, project_name
import shutil
import os
import platform
HIDDEN_IMPORTS = [
    "kivy",
    "kivymd",
    "kivy-garden.qrcode",
    "qrcode",
    "cffi",
    "coincurve",
    "pycryptodome==3.20.0",
    "toolz",
    "typing_extensions",
    "eth_typing",
    "eth_hash",
    "cytoolz",
    "eth_utils",
    "eth_keys",
    "eciespy",
    "multi_crypt",
    "ipfs_node",
    "ipfs_tk>=0.1.3",
    "appdirs",
    "termcolor",
    "tqdm",
    "android",
    "walytis_beta_embedded>=0.0.3",
    "ipfs_toolkit==0.6.0rc1",
    "brenthy_tools_beta",
    "walytis_beta_api",
    "rfc3987",
    "decorate_all",
    "py_strict_typing",
    "loguru",
    "dataclasses-json",
    "marshmallow",
    "typing_inspect",
    "mypy_extensions",
    "portalocker",

]
EXCLUDED_IMPORTS = [
    "PyQt5",
    "PyQt6",
]


WORKDIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(WORKDIR, "src")
ENTRY_POINT = os.path.join(SOURCE_DIR, "__main__.py")

DATA_FILES = [
    os.path.join("endra_app", "tech.emendir.Endra.svg")
]

if os.path.exists("build"):
    shutil.rmtree("build")
# shutil.rmtree("dist")
command_appendages = ""
for lib in HIDDEN_IMPORTS:
    command_appendages += f" --hidden-import={lib}"
for lib in EXCLUDED_IMPORTS:
    command_appendages += f" --exclude={lib}"
for file in DATA_FILES:
    command_appendages += (
        f" --add-data='{os.path.join(SOURCE_DIR, file)}:"
        f"{os.path.dirname(file)}'"
    )


if (platform.system().lower() == "windows"):
    cmd = (
        f"pyinstaller --name={project_name} --windowed --onefile "
        f"{ENTRY_POINT} {command_appendages}"
    )

    import pyzbar
    pyzbardir = os.path.dirname(pyzbar.__file__)
    cmd += f" --add-binary={pyzbardir}\\libiconv.dll;."
    cmd += f" --add-binary={pyzbardir}\\libzbar-64.dll;."
    os.system(cmd)
    shutil.move(os.path.join("dist", f"{project_name}.exe"),
                os.path.join("dist", f"{project_name}_v{version}_{platform.system().lower()}_{platform.machine().lower().replace('x86_64', 'amd64')}.exe"))
else:
    cmd = (
        f"pyinstaller --name={project_name} --windowed --onefile "
        f"{ENTRY_POINT} {command_appendages}"
    )
    cmd = "export QT_DEBUG_PLUGINS=1;" + cmd
    print(cmd)
    os.system(cmd)
    shutil.move(os.path.join("dist", project_name),
                os.path.join("dist", f"{project_name}_v{version}_{platform.system().lower()}_{platform.machine().lower().replace('x86_64', 'amd64')}.AppImage"))
