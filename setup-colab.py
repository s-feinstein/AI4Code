import json
import os
from getpass import getpass
from pathlib import Path
from typing import Dict, List, Optional, Union


def load_secrets(secrets: Optional[Union[str, Dict[str, str]]] = None, overwrite=False) -> None:
    """
    Loads secrets and sets up some env vars and credential files.

    If the `secrets` param is empty, you will be prompted to input a stringified json dict containing your secrets. Otherwise, the secrets will be loaded from the given string or dict.

    The following types of credentials are supported:

    GitHub Credentials:
        `github_user`: GitHub Username
        `github_pat`: GitHub Personal Access Token

    Kaggle API Token:
        `kaggle_username`: Kaggle Username
        `kaggle_secret_access_key`: Kaggle API Access Key
    """

    if secrets and isinstance(secrets, str):
        secrets = json.loads(secrets)

    if not secrets:
        input = getpass("Secrets (JSON string): ")
        secrets = json.loads(input) if input else {}

    if "github_user" in secrets:
        os.environ["GH_USER"] = secrets["github_user"]
        os.environ["GH_PAT"] = secrets["github_pat"]
        # provide a custom credential helper to git so that it uses your env vars
        os.system("""git config --global credential.helper '!f() { printf "%s\n" "username=$GH_USER" "password=$GH_PAT"; };f'""")

    if "kaggle_username" in secrets:
        home = Path.home()
        kaggle_user = secrets["kaggle_username"]
        kaggle_key = secrets["kaggle_secret_access_key"]
        (home / ".kaggle/").mkdir(parents=True, exist_ok=True)
        with open(home / ".kaggle/kaggle.json", "w") as fp:
            fp.write(f"[default]\nkaggle_username = {kaggle_user}\nkaggle_secret_access_key = {kaggle_key}\n")
