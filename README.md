# VirusTotal Utility Library and Command Line Tools

- [VirusTotal Utility Library and Command Line Tools](#virustotal-utility-library-and-command-line-tools)
  - [Installation](#installation)
    - [pipx](#pipx)
    - [pip](#pip)
  - [Utilities](#utilities)
    - [vtpy](#vtpy)
      - [Features](#features)
        - [Homebrew integration](#homebrew-integration)
        - [macOS specific features](#macos-specific-features)
      - [Usage](#usage)
  - [Develop](#develop)

## Installation

### pipx

This is the recommended installation method.

```
$ pipx install virustotal-tddschn
```

### [pip](https://pypi.org/project/virustotal-tddschn/)

```
$ pip install virustotal-tddschn
```

## Utilities

### vtpy


#### Features

##### Homebrew integration
- `--brew` & `--cask`: Parsing Homebrew's DSL `formula` and `cask` files, extracting the package checksum with matching CPU arch

    <details>
    <summary>Click to expand example</summary>

    ```
    $ vtpy -w inkscape -B
    
    File path:       /usr/local/Homebrew/Library/Taps/homebrew/homebrew-cask/Casks/inkscape.rb
    SHA256 checksum: 8117d5d864358c9f626ce574d07d2f121ad96fc96a535cc3fddaba3c74bd3279
    VirusTotal URL:  https://www.virustotal.com/gui/search/8117d5d864358c9f626ce574d07d2f121ad96fc96a535cc3fddaba3c74bd3279
    ```
    <!-- Two important rules:
    Make sure you have an empty line after the closing </summary> tag, otherwise the markdown/code blocks won't show correctly.
    Make sure you have an empty line after the closing </details> tag if you have multiple collapsible sections. -->
    </details>


- `--brew-cache`: Locating the `brew`-downloaded package in `brew`'s cache

    <details>
    <summary>Click to expand example</summary>

    ```
    $ vtpy -c google-chrome -b firefox -B
    
    File path:       /Users/tscp/Library/Caches/Homebrew/downloads/88881e66883c4776fff9b3019b48a26795020439a33ddbedd3bd4620283aecd2--googlechrome.dmg
    SHA256 checksum: 201739d3cf941d33daf605351160f22bdd5877070267e2b42f37efa661378772
    VirusTotal URL:  https://www.virustotal.com/gui/search/201739d3cf941d33daf605351160f22bdd5877070267e2b42f37efa661378772
    ```
    <!-- Two important rules:
    Make sure you have an empty line after the closing </summary> tag, otherwise the markdown/code blocks won't show correctly.
    Make sure you have an empty line after the closing </details> tag if you have multiple collapsible sections. -->
    </details>


##### macOS specific features
- `--mac`: Locating binaries inside macOS app bundles (the `.app` directories).

    <details>
    <summary>Click to expand example</summary>

    ```
    $ vtpy -m /Applications/kitty.app -B
    
    File path:       /Applications/kitty.app/Contents/MacOS/kitty
    SHA256 checksum: ca6aabac5bd9cd9dde7e3c713eae2031aabec08129218817aecbccb5408b3b0b
    VirusTotal URL:  https://www.virustotal.com/gui/search/ca6aabac5bd9cd9dde7e3c713eae2031aabec08129218817aecbccb5408b3b0b
    ```
    <!-- Two important rules:
    Make sure you have an empty line after the closing </summary> tag, otherwise the markdown/code blocks won't show correctly.
    Make sure you have an empty line after the closing </details> tag if you have multiple collapsible sections. -->
    </details>


#### Usage

```
$ vtpy --help

usage: vtpy [-h] [--hash HASH] [-f FILE] [-b browser] [-B] [-ldl] [-w BREW] [-C] [-c BREW] [-m APP] [-F PATH] [-V]

Search file or Homebrew package checksum on VirusTotal

options:
  -h, --help            show this help message and exit
  --hash HASH           The hash to search (default: None)
  -f FILE, --file FILE  The file to hash and check (default: None)
  -b browser, --browser browser
                        Browser to open URLs (default: chrome)
  -B, --no-browser      Do not open URLs in a browser (default: False)
  -ldl, --latest-download
                        Use the latest downloaded file (default: False)
  -w BREW, --brew BREW  Use the checksum in Homebrew formula or cask file (default: None)
  -C, --cask            Use cask (default: None)
  -c BREW, --brew-cache BREW
                        Use brew downloaded cache (default: None)
  -m APP, --mac APP     Path to app bundle (default: None)
  -F PATH, --brew-file PATH
                        Use the checksum in the brew formula or cask file (default: None)
  -V, --version         show program's version number and exit
```




## Develop

```
$ git clone https://github.com/tddschn/virustotal-tddschn.git
$ cd virustotal-tddschn
$ poetry install
```