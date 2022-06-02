#!/usr/bin/env python3


import os
from pathlib import Path
from .config import browser_str_to_app_name_map


def open_url(url: str, browser: str):
    # webbrowser.get(browser).open(url)
    # this sucks!
    # raise Error("could not locate runnable browser")

    import subprocess

    browser_app_name = browser_str_to_app_name_map[browser]
    # subprocess.call(['/usr/bin/open', '-a', browser_app_name, url])
    subprocess.call(['open', '-a', browser_app_name, url])


def macos_get_version_codename() -> str:
    # version_info is like this: ('10.16', ('', '', ''), 'x86_64')
    # on monterey 12.4: ('12.4', ('', '', ''), 'x86_64')
    import platform

    version_info = platform.mac_ver()

    macos_version = version_info[0]
    macos_arch = version_info[2]
    macos_version_lookup = {'10.14': 'mojave', '10.15': 'catalina', '10.16': 'big_sur'}
    if macos_version in macos_version_lookup:
        codename = macos_version_lookup[macos_version]
    else:
        macos_version_major = macos_version.split('.')[0]
        if macos_version_major == '11':
            codename = 'big_sur'
        elif macos_version_major == '12':
            codename = 'monterey'
        else:
            raise ValueError(f'Unrecognized macos version: {macos_version}')

    if macos_arch != 'x86_64':
        codename = 'arm64_' + codename
    return codename

def get_latest_downloaded_file() -> Path:
    # download_list = glob.glob(str(Path.home() / 'Downloads') + '/*')
    # latest_downloaded_file = max(filter(os.path.isfile, download_list),
    #                              key=os.path.getctime)
    # return latest_downloaded_file
    download_gen = (Path.home() / 'Downloads').glob('*')
    latest_downloaded_file = max(
        (f for f in download_gen if f.is_file()), key=os.path.getctime
    )
    return latest_downloaded_file