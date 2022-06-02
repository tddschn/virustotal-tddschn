#!/usr/bin/env python3

import os, re
from pathlib import Path
from typing import Any, Literal


def get_brew_tap_dir() -> str:
    def get_brew_tap_dir_with_subprocess():
        import subprocess

        return subprocess.getoutput('brew --prefix') + '/Homebrew/Library/Taps'

    homebrew_repo_path = os.getenv('HOMEBREW_REPOSITORY')
    if homebrew_repo_path is not None:
        tap_dir_path = Path(homebrew_repo_path) / 'Library' / 'Taps'
        if tap_dir_path.exists():
            return str(tap_dir_path)
        return get_brew_tap_dir_with_subprocess()
    else:
        return get_brew_tap_dir_with_subprocess()


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
    import glob

    brew_type = {'f': 0, 'c': 0}
    formula_paths: list[str] = []
    cask_paths: list[str] = []
    output_dict = {
        'brew_type': brew_type,
        'formula_paths': formula_paths,
        'cask_paths': cask_paths,
    }

    brew_tap_dir = get_brew_tap_dir()
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


def get_checksum_from_brew_file(
    brew_file_path: str | None, codename: str | None = None
) -> str | None:
    import sys

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
    import subprocess, sys
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
