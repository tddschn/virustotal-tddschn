from virustotal_tddschn import virustotal_sum_search as vtss
from virustotal_tddschn.virustotal_sum_search import (
    open_url,
    brew_get_file_path,
    brew_get_type_and_paths,
    brew_get_type_from_path,
    macos_get_version_codename,
    get_checksum_from_brew_file,
    get_brew_cache_path,
    get_latest_downloaded_file,
)

# ! warning: test cases in this files are outdated


def test_open_url():
    url = 'https://google.com'
    open_url(url, 'safari')
    assert False


def test_brew_get_type_and_paths():
    assert brew_get_type_and_paths('docker')['brew_type'] == {'f': 1, 'c': 1}
    # assert brew_get_type_and_paths('docker') == {'f': 1, 'c': 1}
    # assert brew_get_type_and_paths('python@3.9') == {'f': 1, 'c': 0}
    # assert brew_get_type_and_paths('google-chrome') == {'f': 0, 'c': 1}
    # cSpell:disable
    # assert brew_get_type_and_paths('clintmod/formulas/macprefs') == {'f': 1, 'c': 0}
    # assert brew_get_type_and_paths('tddschn/tddschn/aliwangwang') == {'f': 0, 'c': 1}
    # cSpell:enable
    assert brew_get_type_and_paths('python@3.9') == {
        'brew_type': {'f': 1, 'c': 0},
        'formula_paths': [
            '/usr/local/Homebrew/Library/Taps/homebrew/homebrew-core/Formula/python@3.9.rb'
        ],
        'cask_paths': [],
    }
    assert brew_get_type_and_paths('docker')['cask_paths'].__len__() == 1


def test_brew_get_file_path():
    assert (
        brew_get_file_path('python@3.9')
        == '/usr/local/Homebrew/Library/Taps/homebrew/homebrew-core/Formula/python@3.9.rb'
    )
    assert (
        brew_get_file_path('docker')
        == '/usr/local/Homebrew/Library/Taps/homebrew/homebrew-core/Formula/docker.rb'
    )
    assert (
        brew_get_file_path('docker', True)
        == '/usr/local/Homebrew/Library/Taps/homebrew/homebrew-cask/Casks/docker.rb'
    )


def test_macos_get_version_codename():
    assert macos_get_version_codename() == 'big_sur'


def test_get_checksum_from_brew_file():
    # single lang cask
    assert (
        get_checksum_from_brew_file(
            '/usr/local/Homebrew/Library/Taps/homebrew/homebrew-cask/Casks/surge.rb'
        )
        == '63b2f399d7a99484ff630eddb414065a5d5ea9fcbeb553784dfa37a1db9ac36c'
    )

    # multilang cask
    assert (
        get_checksum_from_brew_file(
            '/usr/local/Homebrew/Library/Taps/homebrew/homebrew-cask/Casks/firefox.rb'
        )
        == '9feddc71ac61a527848495bb94360238a0e9aac9d2b91604be48c7f3ac34377d'
    )

    # popular formula
    assert (
        get_checksum_from_brew_file(
            '/usr/local/Homebrew/Library/Taps/homebrew/homebrew-core/Formula/python@3.9.rb'
        )
        == '0c5a140665436ec3dbfbb79e2dfb6d192655f26ef4a29aeffcb6d1820d716d83'
    )


def test_get_brew_cache_path():
    assert (
        get_brew_cache_path('surge')
        == '/Users/tscp/Library/Caches/Homebrew/downloads/10cd592c0c1fc6345bf16eec963b459bfbb5ac2c9eb5ae650363685f8dea5626--Surge-4.1.0-1298-f07b1b8713b2397518f4b252b5786452.zip'
    )
    assert (
        get_brew_cache_path('docker')
        == '/Users/tscp/Library/Caches/Homebrew/downloads/798e00fcc42cd3e8767ec60fda19d190e7a5e13daaeb78560df91f3627aab254--docker--20.10.6.big_sur.bottle.tar.gz'
    )
    assert (
        get_brew_cache_path('docker', use_cask=True)
        == '/Users/tscp/Library/Caches/Homebrew/downloads/2cc36211072280d8bce8a8aba0b9c65c40eb3bcddbcea07053f9627b483071db--Docker.dmg'
    )
    assert (
        get_brew_cache_path('python@3.9')
        == '/Users/tscp/Library/Caches/Homebrew/downloads/54d39614b98a3ad69c6e35ef3ef238b53dcf186cf958ebb666c807bba5e3622e--python@3.9--3.9.5.big_sur.bottle.tar.gz'
    )


def test_get_latest_downloaded_file():
    assert get_latest_downloaded_file() == None
