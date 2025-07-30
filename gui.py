import FreeSimpleGUI as sg
from config_processor import process_configs
from ip_manager import load_ip_list, save_used_ips


def run_gui():
    sg.theme("DarkGrey5")

    layout = [
        [sg.Text("WireGuard Config Folder"), sg.InputText(
            key="CONFIG_FOLDER"), sg.FolderBrowse()],
        [sg.Text("IP List File (.txt)"), sg.InputText(
            key="IP_FILE"), sg.FileBrowse()],
        [sg.Button("Process"), sg.Button("Exit")]
    ]

    window = sg.Window("WireGuard IP Replacer", layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Exit":
            break

        if event == "Process":
            config_folder = values["CONFIG_FOLDER"]
            ip_file = values["IP_FILE"]

            try:
                ip_list = load_ip_list(ip_file)
                result = process_configs(config_folder, ip_list)
                sg.popup("Processing Completed",
                         f"{result['processed']} files updated.\n{result['skipped']} files skipped.")
            except Exception as e:
                sg.popup_error(f"Error: {str(e)}")

    window.close()
