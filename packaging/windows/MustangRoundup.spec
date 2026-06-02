# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files, collect_submodules
from pathlib import Path

block_cipher = None
spec_dir = Path(SPECPATH)
repo_root = spec_dir.parents[1]

datas = [
    (str(repo_root / "assets" / "css"), "assets/css"),
    (str(repo_root / "assets" / "js" / "pwa.js"), "assets/js"),
    (str(repo_root / "mustangroundup" / "templates"), "mustangroundup/templates"),
]
datas += collect_data_files("django")

hiddenimports = (
    collect_submodules("mustangroundup")
    + collect_submodules("mustangroundupsite")
    + collect_submodules("qrcode")
    + collect_submodules("whitenoise")
    + [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.messages",
        "django.contrib.sessions",
        "django.contrib.staticfiles",
        "whitenoise.runserver_nostatic",
    ]
)

a = Analysis(
    [str(spec_dir / "server_launcher.py")],
    pathex=[str(repo_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="MustangRoundup",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="MustangRoundup",
)
