#!/usr/bin/env python3
"""
Author : Xinyuan Chen <45612704+tddschn@users.noreply.github.com>
Date   : 2021-05-12
Purpose: Search file or Homebrew package's checksum on VitusTotal
"""
import argparse, re, sys
import os
from pathlib import Path
from . import __version__
from .hashing import sha256_checksum, sha256_checksum_from_fh
from .config import browser_str_to_app_name_map
from .utils import (
    get_latest_downloaded_file,
    browser_str_to_app_name_map,
    open_url,
    macos_get_version_codename,
)
from .brew_utils import (
    brew_get_file_path,
    get_brew_cache_path,
    get_checksum_from_brew_file,
)

# cSpell:disable
__app_name__ = 'vtpy'
# cSpell:enable

CREATE_ARG_PARSER_ARGS = (
    __app_name__,
    __version__,
    'Search file or Homebrew package checksum on VirusTotal',
)


def create_arg_parser(
    __app_name__: str,
    __version__: str,
    description: str,
    add_help: bool = True,
    brew_related_options_only: bool = False,
):

    parser = argparse.ArgumentParser(
        prog=__app_name__,
        add_help=add_help,
        description=description,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    if brew_related_options_only:
        parser.add_argument(
            'brew',
            metavar='BREW',
            help='The formula or cask name to check',
            type=str,
        )

    if not brew_related_options_only:
        parser.add_argument(
            '--hash', metavar='HASH', type=str, help='The hash to search'
        )

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
        choices=list(browser_str_to_app_name_map),
        default='chrome',
    )

    parser.add_argument(
        '-B', '--no-browser', help='Do not open URLs in a browser', action='store_true'
    )

    if not brew_related_options_only:
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

    if not brew_related_options_only:
        parser.add_argument(
            '-m', '--mac', metavar='APP', help='Path to app bundle', type=str
        )

    parser.add_argument(
        '-V', '--version', action='version', version=f'%(prog)s {__version__}'
    )
    return parser


def parse_args(
    parser: argparse.ArgumentParser, brew_related_options_only: bool = False
) -> argparse.Namespace:

    args = parser.parse_args()
    if brew_name := args.brew:
        if not re.match('[a-zA-Z@._-]+', brew_name):
            if brew_related_options_only:
                parser.error(f'Invalid brew formula / cask name: {brew_name}')
            parser.error(f'Invalid --brew argument: {brew_name} .')
    return args


def main():
    parser = create_arg_parser(*CREATE_ARG_PARSER_ARGS)
    args = parse_args(parser)
    if args.hash:
        hash = args.hash
        print_path_and_open_vt_link(None, hash, args)
    else:
        if args.file:
            hash = sha256_checksum_from_fh(args.file)
            file_path = args.file.name
            print_path_and_open_vt_link(file_path, hash, args)
        else:
            if args.mac:
                exec_name = Path(os.path.basename(args.mac)).with_suffix('')
                file_path = os.path.join(args.mac, 'Contents/MacOS', exec_name)
                hash = sha256_checksum(file_path)  # type: ignore
                print_path_and_open_vt_link(file_path, hash, args)
            elif args.brew:
                brew_file_path = brew_get_file_path(
                    brew_name=args.brew, use_cask=args.cask
                )
                hash = get_checksum_from_brew_file(brew_file_path=brew_file_path)
                file_path = brew_file_path
                print_path_and_open_vt_link(file_path, hash, args)
            elif brew_cache := args.brew_cache:
                file_path = get_brew_cache_path(brew_cache, use_cask=args.cask)
                hash = sha256_checksum(file_path)  # type: ignore
                print_path_and_open_vt_link(file_path, hash, args)
            elif args.latest_download:
                file_path = get_latest_downloaded_file()
                hash = sha256_checksum(file_path)
                print_path_and_open_vt_link(file_path, hash, args)


def print_path_and_open_vt_link(file_path, hash, args):
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
