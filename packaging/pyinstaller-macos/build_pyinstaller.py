#!/usr/bin/env python3


import pyperclip
import sys
import shutil
import os
import platform
import toml


HIDDEN_IMPORTS = ["kivy_garden", "kivy_garden.qrcode"]
EXCLUDED_IMPORTS = ["PyQt6"]


WORK_DIR = os.path.dirname(__file__)
# os.chdir(os.path.dirname(__file__))
PROJ_DIR = os.path.abspath(os.path.join(WORK_DIR, "..", ".."))
# PROJ_DIR = os.path.join(WORK_DIR, "..", "..")

os.chdir(PROJ_DIR)
print("PROJ DIR:", os.path.abspath(PROJ_DIR))
SOURCE_DIR = os.path.join("src")
ENTRY_POINT = os.path.join(SOURCE_DIR, "main.py")
assert os.path.exists(os.path.abspath(ENTRY_POINT)), "WRONG PROJECT PATH"

ICON_PATH = os.path.join("packaging", "share", "endra-icon.ico")
assert os.path.exists(ICON_PATH)

if True:
    import kivy_garden.qrcode
    import libkubo
    import coincurve
# paths relative to SOURCE_DIR
DATA_FILES = [
    (os.path.join("images", "endra-icon.svg"), ""),
    (os.path.join("endra_app", "*.kv"), ""),
    (
        os.path.join(os.path.dirname(kivy_garden.qrcode.__file__), "qrcode_widget.kv"),
        os.path.join("kivy_garden", "qrcode"),
    ),
    (
        os.path.join(os.path.dirname(libkubo.__file__), "*.*"),
        os.path.join("libkubo"),
    ),
    (
        os.path.join(os.path.dirname(coincurve.__file__), "*.*"),
        os.path.join("coincurve"),
    ),
]


with open(os.path.join(PROJ_DIR, "pyproject.toml"), "r") as file:
    data = toml.load(file)
    project_name = data["project"]["name"]
    version = data["project"]["version"]

# # converting *.ui files to *.py files
# for dirname, dirnames, filenames in os.walk("."):
#     if dirname == "./Plugins" or "./.git" in dirname:
#         continue
#     for filename in filenames:
#         path = os.path.join(dirname, filename)
#         if (filename[-2:] == "ui"):
#             print(filename)
#             os.system(f"pyuic6 {path} -o {path[:-2]}py")
if os.path.exists("build"):
    shutil.rmtree("build")
# shutil.rmtree("dist")
command_appendages = ""
for lib in HIDDEN_IMPORTS:
    command_appendages += f" --hidden-import={lib}"
for lib in EXCLUDED_IMPORTS:
    command_appendages += f" --exclude={lib}"
for file, dest in DATA_FILES:
    if dest == "":
        dest = os.path.dirname(file)
    parts = []
    for part in file.split(os.sep):
        if "*" in part:
            break
        parts.append(part)
    path_to_check = os.sep.join(parts)
    if file[0] == os.sep:
        path_to_check = os.sep + path_to_check
    # prioritise paths relative to SOURC_DIR rather than CWD
    elif os.path.exists(os.path.join(SOURCE_DIR, path_to_check)):
        file = os.path.join(SOURCE_DIR, file)
        path_to_check = os.path.join(SOURCE_DIR, path_to_check)
    if not os.path.exists(path_to_check):
        raise FileNotFoundError(path_to_check)
    print("Found path:", path_to_check)
    command_appendages += (
        f' --add-data="{file}:{dest}"'
        # '."'
    )

match platform.system().lower():
    case "windows":
        print("DON'T FORGET:")
        print(
            "- download and install https://www.microsoft.com/en-US/download/details.aspx?id=40784"
        )
        print("- restart (Oh boy, Windows!)")
        cmd = (
            f"{sys.executable} -m PyInstaller --name={project_name} --windowed --onefile -i {ICON_PATH} "
            f"{ENTRY_POINT} {command_appendages}"
        )

        import pyzbar

        pyzbardir = os.path.dirname(pyzbar.__file__)
        cmd += f' --add-binary="{pyzbardir}\\libiconv.dll;."'
        cmd += f' --add-binary="{pyzbardir}\\libzbar-64.dll;."'
        assert os.path.exists(os.path.join(pyzbardir, "libzbar-64.dll"))
        assert os.path.exists(os.path.join(pyzbardir, "libiconv.dll"))
        print(cmd)
        os.system(cmd)
        dest_dir = os.path.abspath(
            os.path.join(
                "dist",
                f"{project_name}_v{version}_{platform.system().lower()}_"
                f"{platform.machine().lower()}.exe",
            )
        )
        shutil.move(os.path.join("dist", f"{project_name}.exe"), dest_dir)
        pyperclip.copy(dest_dir)
    case "linux":
        cmd = (
            f"pyinstaller --name={project_name} --windowed --onefile "
            f"{ENTRY_POINT} {command_appendages}"
        )
        cmd = "export QT_DEBUG_PLUGINS=1;" + cmd
        print(cmd)
        os.system(cmd)
        dest_dir = os.path.abspath(
            os.path.join(
                "dist",
                f"{project_name}_v{version}_{platform.system().lower()}_"
                f"{platform.machine().lower()}.AppImage",
            )
        )
        shutil.move(
            os.path.join("dist", project_name),
        )
        pyperclip.copy(dest_dir)
    case "macos":
        cmd = (
            f"pyinstaller --name={project_name} --windowed --onefile "
            f"{ENTRY_POINT} {command_appendages}"
        )
        cmd = "export QT_DEBUG_PLUGINS=1;" + cmd
        print(cmd)
        os.system(cmd)
        dest_dir = os.path.abspath(
            os.path.join(
                "dist",
                f"{project_name}_v{version}_{platform.system().lower()}_"
                f"{platform.machine().lower()}.dmg",
            )
        )
        shutil.move(
            os.path.join("dist", project_name),
        )
        pyperclip.copy(dest_dir)
    case _:
        raise Exception("Unknown OS")
