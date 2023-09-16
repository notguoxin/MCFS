import os
import json
import subprocess
from pathlib import Path
import pyuac
import time
import string
import random
import uuid
import requests
from termcolor import colored
import shutil

from lib.file import move_file

global temp_dir
def download_file(url, file_name):
    print(f"\n{file_name} downloading from {url}.")
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    if not os.path.exists(temp_dir):
            os.mkdir(temp_dir)
    downloaded = 0
    with open(f"{temp_dir}/{file_name}", 'wb') as file:
        for data in response.iter_content(chunk_size=8192):
            downloaded += len(data)
            file.write(data)
            percentage = int(downloaded * 100 / total_size)
            animation_frames = ["|", "/", "-", "\\"]
            animation_frame = animation_frames[percentage % len(animation_frames)]
            print(f"\rDownloading: [{animation_frame}] {percentage}% ", end="")
    print("Download successed.")

def generate_random_username(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_random_uuid():
    return str(uuid.uuid4()).replace('-', '')

def update_hmcl_config():
    config_path = os.path.join(os.getenv("APPDATA"), ".hmcl", "accounts.json")
    config_folder = os.path.join(os.getenv("APPDATA"), ".hmcl")
    try:
        if not os.path.exists(config_folder):
            os.mkdir(config_folder)
        username = generate_random_username()
        uuid_value = generate_random_uuid()
        
        config_data = [
            {
                "username": username,
                "uuid": uuid_value,
                "skin": {
                    "type": "steve",
                    "cslApi": "",
                    "textureModel": "default"
                },
                "type": "offline"
            }
        ]
        
        with open(config_path, "w") as config_file:
            json.dump(config_data, config_file, indent=4)
    
        print("HMCL configuration updated with new username and UUID:", username, uuid_value)
    except Exception as e:
        print("Error updating HMCL configuration:", e)

def install_exe_silently(exe_path, command_line, software_name):
    try:
        subprocess.run([exe_path, f"{command_line}"], check=True)  # Run the installer silently
        print(f"{software_name} installation successful!")
    except Exception as e:
        print(f"{software_name} installation failed:", e)

def main():
    try:
        print(
            
                "Project: Auto Installer for MCC (MCreator Championship)\nStable: 1.0.1\n Full Version: 1.28.5\nAuthor: GuoXin\n",
        )
        destination_folder = os.path.join(Path.home(), "Desktop", "MCC")
        print(f"[~] Set temp directory to {temp_dir}")
        print(f"[~] Set the destination_folder to {destination_folder}")
        download_file("https://github.com/MCreator/MCreator/releases/download/2022.3.48217/MCreator.2022.3.Windows.64bit.exe","Mcreator.exe")
        download_file("https://github.com/huanghongxun/HMCL/releases/download/release-3.5.5/HMCL-3.5.5.exe","HMCL.exe")
        download_file("https://download.oracle.com/java/19/archive/jdk-19.0.2_windows-x64_bin.exe","java-jdk-19.exe")
        print(f"[~] Starting")
        if not os.path.exists(destination_folder):
            print(f"[~] folder not exists... Creating...")
            os.mkdir(destination_folder)

        move_file([f"{temp_dir}//HMCL.exe"], destination_folder)
        print(f"[~] Installing Mcreator")
        install_exe_silently(f"{temp_dir}//MCreator.exe", "/S", "MCreator")
        print(f"[~] Installing JAVA")
        install_exe_silently(f"{temp_dir}//java-jdk-19.exe", "/s", "Java")
        print(f"[~] Updating config for HMCL")
        update_hmcl_config()
        print(f"[~] Starting HMCL")
        subprocess.run(f"{destination_folder}//HMCL.exe")
        shutil.rmtree(temp_dir, ignore_errors=True)
        os.system("cls")
        print("EXIT: 0")
        print("It's save to close now.")
        time.sleep(120)
    except Exception as e:
        print(f"Err: {e}")
        print("EXIT: 1")
        time.sleep(5000)

if __name__ == "__main__":
    try:
        if not pyuac.isUserAdmin():
            print("WARNING: DO NOT CLOSE THIS WINDOW!")
            pyuac.runAsAdmin()
        else:
            temp_dir = os.path.join(os.getenv("TEMP"), ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5)))
            main()  # Already an admin here.
    except Exception as e:
        print(f"Err: Start Error: {e}")
        print("EXIT: 1")
        time.sleep(69420)
