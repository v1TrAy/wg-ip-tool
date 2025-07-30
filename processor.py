import os
import re


def load_ip_list(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]


def list_config_files(config_folder):
    return [f for f in os.listdir(config_folder) if f.endswith('.conf')]


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

    for i, filename in enumerate(config_files):
        ip = ip_list[i % len(ip_list)]
        in_path = os.path.join(config_folder, filename)
        out_path = os.path.join(output_folder, filename)

        with open(in_path, 'r') as f:
            content = f.read()

        updated = replace_ip_in_config(content, ip, port)

        with open(out_path, 'w') as f:
            f.write(updated)

        yield filename, ip  # Useful for GUI to log progress
