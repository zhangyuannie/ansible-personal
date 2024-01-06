#!/usr/bin/env python3
# MIT License
# Copyright (c) Zhangyuan Nie

from ansible.module_utils.basic import AnsibleModule
import subprocess
from urllib import request
import os
import tarfile
from io import BytesIO
import shutil
import re


def main():
    module = AnsibleModule(
        argument_spec={
            "dest": {"type": "str", "required": True},
            "version": {"type": "str"},
        },
        supports_check_mode=True,
    )
    dest = module.params["dest"]
    target_version = module.params["version"]
    if target_version:
        target_version = "go" + target_version
    else:
        target_version_raw = (
            request.urlopen("https://go.dev/VERSION?m=text").read().decode("utf-8")
        )
        target_version = re.search(r"go\d+\.\d+\.\d+", target_version_raw)
        if target_version:
            target_version = target_version.group(0)
        else:
            module.fail_json(f"Failed to fetch latest go version: {target_version_raw}")

    if os.path.exists(os.path.join(dest, "go")):
        p = subprocess.run(
            [os.path.join(dest, "go/bin/go"), "version"],
            text=True,
            capture_output=True,
        )
        if p.returncode != 0:
            module.fail_json(p.stderr.strip())
        if target_version in p.stdout:
            module.exit_json(changed=False)

    if not module.check_mode:
        res = request.urlopen(f"https://go.dev/dl/{target_version}.linux-amd64.tar.gz")
        os.makedirs(dest, exist_ok=True)
        shutil.rmtree(os.path.join(dest, "go"), True)

        with tarfile.open(fileobj=BytesIO(res.read())) as file:
            file.extractall(dest)

    module.exit_json(changed=True)


if __name__ == "__main__":
    main()
