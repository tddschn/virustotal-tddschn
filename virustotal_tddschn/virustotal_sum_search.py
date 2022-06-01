#!/usr/bin/env python3
"""
Author : tscp <tscp@localhost>
Date   : 2021-05-12
Purpose: Search file or Homebrew package's checksum on VitusTotal
"""

from pathlib import Path
import platform
import glob
import subprocess

# import webbrowser
import hashlib
import sys
import argparse
import os
from os import PathLike
import re
from typing import Any, Literal
from . import __version__

# cSpell:disable
__app_name__ = 'vtpy'
# cSpell:enable
browser_str_to_app_name = {
    'chrome': 'Google Chrome',
    'google-chrome': 'Google Chrome',
    'safari': 'Safari',
    'firefox': 'Firefox',
}


def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        prog=__app_name__,
        description='Search file or Homebrew package checksum on VirusTotal',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument('--hash', metavar='HASH', type=str, help='The hash to search')

    parser.add_argument(
        '-f',
        '--file',
        metavar='FILE',
        type=argparse.FileType('rb'),
        help='The file to hash and check',
    )

    parser.add_argument(
        '-b',
        '--browser',
        help='Browser to open URLs',
        metavar='browser',
        type=str,
        choices=['google-chrome', 'firefox', 'safari'],
        default='google-chrome',
    )

    parser.add_argument(
        '-B', '--no-browser', help='Do not open URLs in a browser', action='store_true'
    )

    parser.add_argument(
        '-ldl',
        '--latest-download',
        help='Use the latest downloaded file',
        action='store_true',
    )

    parser.add_argument(
        '-w',
        '--brew',
        metavar='BREW',
        help='Use the checksum in Homebrew formula or cask file',
        type=str,
    )

    # parser.add_argument(
    # '-F', '--formula', help='Use formula if a cask exists with the same name', action='store_true', default=None)
    parser.add_argument(
        '-C', '--cask', help='Use cask', action='store_true', default=None
    )

    parser.add_argument(
        '-c', '--brew-cache', metavar='BREW', help='Use brew downloaded cache'
    )

    parser.add_argument(
        '-m', '--mac', metavar='APP', help='Path to app bundle', type=str
    )

    parser.add_argument(
        '-V', '--version', action='version', version=f'%(prog)s {__version__}'
    )

    args = parser.parse_args()
    if brew_name := args.brew:
        if not re.match('[a-zA-Z@._-]+', brew_name):
            sys.exit(f'Invalid --brew argument: {brew_name} .')
    return args


def sha256_checksum(filename: PathLike, block_size=65536) -> str:
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()


def sha256_checksum_from_fh(fh, block_size=65536):
    sha256 = hashlib.sha256()
    for block in iter(lambda: fh.read(block_size), b''):
        sha256.update(block)
    return sha256.hexdigest()


def open_url(url: str, browser: str):
    # webbrowser.get(browser).open(url)
    # this sucks!
    # raise Error("could not locate runnable browser")

    browser_app_name = browser_str_to_app_name[browser]
    subprocess.call(['/usr/bin/open', '-a', browser_app_name, url])


def brew_get_type_from_path(brew_file_path: str) -> Literal['f'] | Literal['c'] | None:
    with open(brew_file_path) as fh:
        file_content = fh.read()
    if re.match(r'class [a-zA-Z0-9]+ < Formula\n', file_content):
        return 'f'
    elif re.match(r'cask "[a-zA-Z0-0@._-]+" do\n', file_content):
        return 'c'
    else:
        return None


def brew_get_type_and_paths(brew_name: str) -> dict[str, Any]:
    brew_type = {'f': 0, 'c': 0}
    formula_paths: list[str] = []
    cask_paths: list[str] = []
    output_dict = {
        'brew_type': brew_type,
        'formula_paths': formula_paths,
        'cask_paths': cask_paths,
    }

    brew_tap_dir = subprocess.getoutput('brew --prefix') + '/Homebrew/Library/Taps'
    if match := re.match(
        r'([a-zA-Z0-9@._-]+)/([a-zA-Z0-9@._-]+)/([a-zA-Z0-9@._-]+)$', brew_name
    ):
        brew_tap_dir = os.path.join(
            brew_tap_dir, match.group(1), 'homebrew-' + match.group(2)
        )
        brew_name = match.group(3)
    matched_files = glob.glob(brew_tap_dir + f'/**/{brew_name}.rb', recursive=True)
    if matched_files:
        for file in matched_files:
            file_type = brew_get_type_from_path(file)
            if file_type == 'f':
                brew_type['f'] = 1
                formula_paths.append(file)
            elif file_type == 'c':
                brew_type['c'] = 1
                cask_paths.append(file)
    return output_dict


def brew_get_file_path(brew_name: str, use_cask: bool = False) -> str | None:
    type_and_paths = brew_get_type_and_paths(brew_name)
    if use_cask:
        output = type_and_paths['cask_paths'][0]
    else:
        # test ['f'] first, if it's FC, f would be used
        if type_and_paths['brew_type']['f']:
            output = type_and_paths['formula_paths'][0]
        elif type_and_paths['brew_type']['c']:
            output = type_and_paths['cask_paths'][0]
        else:
            return None
    if output:
        return output


def macos_get_version_codename() -> str:
    # version_info is like this: ('10.16', ('', '', ''), 'x86_64')
    version_info = platform.mac_ver()

    macos_version = version_info[0]
    macos_arch = version_info[2]
    macos_version_lookup = {'10.14': 'mojave', '10.15': 'catalina', '10.16': 'big_sur'}
    codename = macos_version_lookup[macos_version]
    if macos_arch != 'x86_64':
        codename = 'arm64_' + codename
    return codename


def get_checksum_from_brew_file(
    brew_file_path: str | None, codename: str | None = None
) -> str | None:
    if brew_file_path is None:
        return None
    if brew_type := brew_get_type_from_path(brew_file_path):
        with open(brew_file_path) as fh:
            file_content = fh.read()
        # if brew_type == 'f':
        #     pass
        # elif brew_type == 'c':
        #     if match := re.findall('^(?:  )+sha256 "([a-f0-9]{64})"$',
        #                            file_content, re.MULTILINE):
        #         return match[0]

        # for multilang casks like firefox
        if multilang_cask := re.search(
            'default: true do\n(?:  )+sha256 "([a-f0-9]{64})"$',
            file_content,
            re.MULTILINE,
        ):
            return multilang_cask.group(1)

        # for single lang formulas and casks
        # - for formulas, only checks source sha256, not the bottle's
        elif match := re.search(
            '^(?:  )+sha256 "([a-f0-9]{64})"$', file_content, re.MULTILINE
        ):
            return match.group(1)
        else:
            sys.exit(f'Failed to find sha256 checksum in {brew_file_path} .')
    else:
        sys.exit(f'{brew_file_path} doesn\'t seem like a formula for cask file.')
        # return None


def get_brew_cache_path(brew_name: str, use_cask: bool = False) -> str:
    brew_type = brew_get_type_and_paths(brew_name)['brew_type']
    if use_cask:
        cache_flag = '--cask'
    elif sum(brew_type.values()) == 2:
        cache_flag = '--formula'
    else:
        cache_flag = ''

    brew_cache_command = 'brew --cache ' + cache_flag + ' ' + brew_name
    cache_path = subprocess.getoutput(brew_cache_command).strip()
    if cache_path:
        return cache_path
    else:
        sys.exit(f'Failed to get the cache path for {brew_name} .')


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


def main():
    args = get_args()
    if args.hash:
        hash = args.hash
        print_path_and_open_vt_link(None, hash)
    else:
        if args.file:
            hash = sha256_checksum_from_fh(args.file)
            file_path = args.file.name
            print_path_and_open_vt_link(file_path, hash)
        else:
            if args.mac:
                exec_name = Path(os.path.basename(args.mac)).with_suffix('')
                file_path = os.path.join(args.mac, 'Contents/MacOS', exec_name)
                hash = sha256_checksum(file_path)  # type: ignore
                print_path_and_open_vt_link(file_path, hash)
            elif args.brew:
                brew_file_path = brew_get_file_path(
                    brew_name=args.brew, use_cask=args.cask
                )
                hash = get_checksum_from_brew_file(brew_file_path=brew_file_path)
                file_path = brew_file_path
                print_path_and_open_vt_link(file_path, hash)
            elif brew_cache := args.brew_cache:
                file_path = get_brew_cache_path(brew_cache, use_cask=args.cask)
                hash = sha256_checksum(file_path)  # type: ignore
                print_path_and_open_vt_link(file_path, hash)
            elif args.latest_download:
                file_path = get_latest_downloaded_file()
                hash = sha256_checksum(file_path)
                print_path_and_open_vt_link(file_path, hash)


def print_path_and_open_vt_link(file_path, hash):
    args = get_args()
    if file_path:
        print(f'File path:       {file_path}')
    if hash:
        vt_url = 'https://www.virustotal.com/gui/search/' + hash
        print(f'SHA256 checksum: {hash}')
        print(f'VirusTotal URL:  {vt_url}')
        if not args.no_browser:
            open_url(url=vt_url, browser=args.browser)


if __name__ == '__main__':
    main()
