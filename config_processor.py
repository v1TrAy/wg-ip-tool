import os
import re
from ip_manager import load_used_ips, save_used_ips

ENDPOINT_REGEX = re.compile(r"(Endpoint\s*=\s*)([\d\.]+:\d+)")


def process_configs(config_folder, new_ips):
    config_files = [f for f in os.listdir(
        config_folder) if f.endswith(".conf")]
    used_ips = load_used_ips()
    updated_ips = []
    processed = 0
    skipped = 0
    ip_index = 0

    for filename in config_files:
        if ip_index >= len(new_ips):
            skipped += 1
            continue

        new_ip_port = new_ips[ip_index]

        if new_ip_port in used_ips:
            skipped += 1
            continue

        filepath = os.path.join(config_folder, filename)

        with open(filepath, "r") as f:
            content = f.read()

        match = ENDPOINT_REGEX.search(content)
        if match:
            new_line = f"{match.group(1)}{new_ip_port}"
            content = ENDPOINT_REGEX.sub(new_line, content, count=1)

            with open(filepath, "w") as f:
                f.write(content)

            updated_ips.append(new_ip_port)
            processed += 1
            ip_index += 1
        else:
            skipped += 1

    save_used_ips(used_ips + updated_ips)

    return {"processed": processed, "skipped": skipped}
