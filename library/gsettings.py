#!/usr/bin/env python3
# MIT License
# Copyright (c) Zhangyuan Nie

from ansible.module_utils.basic import AnsibleModule
import subprocess


def main():
    module = AnsibleModule(
        argument_spec={
            "schema": {"type": "str", "required": True},
            "path": {"type": "str", "default": ""},
            "key": {"type": "str"},
            "value": {"type": "str"},
            "entries": {"type": "dict"},
        },
        supports_check_mode=True,
    )

    def gsettings_get(schema: str, path: str, key: str):
        if path:
            schema += f":{path}"
        p = subprocess.run(
            ["gsettings", "get", schema, key],
            text=True,
            capture_output=True,
        )
        if p.returncode != 0:
            module.fail_json(p.stderr.strip())
        return p.stdout.strip()

    def gsettings_set(schema: str, path: str, key: str, value: str):
        if path:
            schema += f":{path}"
        p = subprocess.run(
            ["gsettings", "set", schema, key, value],
            text=True,
            capture_output=True,
        )
        if p.returncode != 0:
            module.fail_json(p.stderr.strip())

    schema = module.params["schema"]
    path = module.params["path"]
    key = module.params["key"]
    value = module.params["value"]
    entries = module.params["entries"] or {}
    if key and value:
        entries[key] = value

    changed = False
    for k, v in entries.items():
        cur_value = gsettings_get(schema, path, k)
        changed = changed or cur_value != v

        if cur_value != v and not module.check_mode:
            gsettings_set(schema, path, k, v)

    module.exit_json(changed=changed)


if __name__ == "__main__":
    main()
