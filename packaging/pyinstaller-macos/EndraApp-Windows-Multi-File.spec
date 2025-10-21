# -*- mode: python ; coding: utf-8 -*-
from kivy_deps import sdl2, glew, angle
import kivy_garden

data_files = [
(os.path.join('src', 'endra_app', '*.kv'), '.'),
(os.path.join('src', 'endra_app', '*.kv'), 'endra_app'),
(os.path.join('src/endra_app/*.kv'), '.'),
(os.path.join('src/endra_app/*.kv'), 'endra_app'),
]
a = Analysis(
    ['src\\main.py'],
    pathex=[],
    binaries=[],
    datas=data_files,
    hiddenimports=['Kivy-Garden','kivy-garden','kivy_garden','kivy-garden.qrcode','kivy_garden.qrcode', 'kivy_deps.glew', 'kivy_deps.sdl2', 'kivy_deps.angle'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='EndraApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe, Tree('src'), Tree('C:\\Users\\weden\\AppData\\Roaming\\Python\\Python313\\site-packages'),
    a.binaries,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins + angle.dep_bins)],
    strip=False,
    upx=True,
    upx_exclude=[],
    name='EndraApp',
)
