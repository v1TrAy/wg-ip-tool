import json
import os

USED_IPS_FILE = "used_ips.json"


def load_ip_list(filepath):
    with open(filepath, "r") as f:
        all_ips = [line.strip() for line in f if line.strip()]
    used_ips = load_used_ips()
    return [ip for ip in all_ips if ip not in used_ips]


def load_used_ips():
    if not os.path.exists(USED_IPS_FILE):
        return []
    with open(USED_IPS_FILE, "r") as f:
        return json.load(f)


def save_used_ips(used_ips):
    with open(USED_IPS_FILE, "w") as f:
        json.dump(used_ips, f)
