import FreeSimpleGUI as sg
from processor import load_ip_list, process_configs


def run_gui():
    layout = [
        [sg.Text("IP List File:"), sg.Input(), sg.FileBrowse(key="ip_file")],
        [sg.Text("Config Folder:"), sg.Input(),
         sg.FolderBrowse(key="config_folder")],
        [sg.Text("Output Folder:"), sg.Input(),
         sg.FolderBrowse(key="output_folder")],
        [sg.Button("Start"), sg.Button("Exit")],
        [sg.Output(size=(80, 20))]
    ]

    window = sg.Window("WireGuard IP Replacer", layout)

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Exit"):
            break

        if event == "Start":
            try:
                ip_list = load_ip_list(values["ip_file"])
                for file, ip in process_configs(ip_list, values["config_folder"], values["output_folder"]):
                    print(f"✅ {file} → {ip}")
                print("🎉 All done.")
            except Exception as e:
                print(f"❌ Error: {e}")

    window.close()
