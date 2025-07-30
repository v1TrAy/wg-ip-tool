import os
import re


def load_ip_list(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]


def list_config_files(config_folder):
    return [f for f in os.listdir(config_folder) if f.endswith('.conf')]


def load_unused_ips(ip_file_path, used_ip_file_path):
    with open(ip_file_path, 'r') as f:
        all_ips = [line.strip() for line in f if line.strip()]

    used_ips = []
    if os.path.exists(used_ip_file_path):
        with open(used_ip_file_path, 'r') as f:
            used_ips = [line.strip() for line in f if line.strip()]

    unused_ips = [ip for ip in all_ips if ip not in used_ips]
    return unused_ips, used_ips


def save_used_ips(used_ip_file_path, newly_used_ips):
    with open(used_ip_file_path, 'a') as f:
        for ip in newly_used_ips:
            f.write(ip + '\n')


def replace_ip_in_config(content, raw_input_ip, default_port=51820):
    # Check if IP already includes a port
    if ':' in raw_input_ip:
        ip, port = raw_input_ip.split(':')
    else:
        ip = raw_input_ip
        port = str(default_port)

    # Replace the Endpoint line properly
    return re.sub(r'Endpoint\s*=\s*[\d.]+:\d+', f'Endpoint = {ip}:{port}', content)


def process_configs(ip_list, config_folder, output_folder, port=51820):
    config_files = list_config_files(config_folder)

    if not config_files:
        raise ValueError("No config files found.")

    if len(ip_list) < len(config_files):
        raise ValueError(
            f"Not enough IPs ({len(ip_list)}) for {len(config_files)} config files.")

    newly_used_ips = []

    for i, filename in enumerate(config_files):
        ip = ip_list[i]
        in_path = os.path.join(config_folder, filename)
        out_path = os.path.join(output_folder, filename)

        with open(in_path, 'r') as f:
            content = f.read()

        updated = replace_ip_in_config(content, ip, port)

        with open(out_path, 'w') as f:
            f.write(updated)

        yield filename, ip
        newly_used_ips.append(ip)

    return newly_used_ips
