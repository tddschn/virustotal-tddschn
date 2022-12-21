#!/usr/bin/env python3

from pathlib import Path

browser_str_to_app_name_map = {
    'chrome': 'Google Chrome',
    # 'google-chrome': 'Google Chrome',
    'safari': 'Safari',
    'firefox': 'Firefox',
}

vt_cli_api_key_env_var_name = 'VTCLI_APIKEY'
vt_cli_config_file_path = Path.home() / '.vt.toml'
