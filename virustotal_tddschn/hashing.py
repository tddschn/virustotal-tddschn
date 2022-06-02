#!/usr/bin/env python3

from os import PathLike
def sha256_checksum(filename: PathLike, block_size=65536) -> str:
    import hashlib
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()


def sha256_checksum_from_fh(fh, block_size=65536):
    import hashlib
    sha256 = hashlib.sha256()
    for block in iter(lambda: fh.read(block_size), b''):
        sha256.update(block)
    return sha256.hexdigest()
