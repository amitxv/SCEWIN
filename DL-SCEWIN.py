import contextlib
import glob
import os
import re
import shutil
import subprocess
import sys
import zipfile

import requests
from distutils.spawn import find_executable


def download_innoextract(output_path: str) -> None:
    response = requests.get(
        "https://api.github.com/repos/dscharrer/innoextract/releases/latest",
        timeout=5,
    )
    data = response.json()

    for asset in data["assets"]:
        file_name = asset["name"]
        if file_name.endswith("windows.zip"):
            response = requests.get(asset["browser_download_url"], timeout=5)
            file_path = f"{os.environ['TEMP']}\\{file_name}"

            with open(file_path, "wb") as file:
                file.write(response.content)

            with zipfile.ZipFile(file_path, "r") as file:
                file.extract("innoextract.exe", output_path)


def main() -> int:
    if find_executable("innoextract") is None:
        download_innoextract("C:\\Windows")

    msi_center_zip = f"{os.environ['TEMP']}\\MSI-Center.zip"
    extract_path = f"{os.environ['TEMP']}\\MSI-Center"

    response = requests.get(
        "https://download.msi.com/uti_exe/gaming-gear/MSI-Center.zip",
        timeout=5,
    )

    # Download MSI Center
    with open(msi_center_zip, "wb") as file:
        file.write(response.content)

    os.makedirs(extract_path, exist_ok=True)

    with zipfile.ZipFile(msi_center_zip, "r") as file:
        file.extractall(extract_path)

    msi_center_installer = glob.glob(f"{extract_path}\\MSI Center_*.exe")

    if not msi_center_installer:
        print("error: MSI Center executable installer not found")
        return 1

    # get version from file name
    msi_center_ver = re.search(
        r"_([\d.]+)\.exe$",
        os.path.basename(msi_center_installer[0]),
    )

    if not msi_center_ver:
        print("error: Failed to obtain MSI Center version")
        return 1

    msi_center_version = msi_center_ver.group(1)

    subprocess.call(
        ["innoextract", msi_center_installer[0], "--output-dir", extract_path],
    )

    appxbundle = glob.glob(f"{extract_path}\\app\\*.appxbundle")

    if not appxbundle:
        print("error: Appx bundle file not found")
        return 1

    appx_file_name = f"MSI%20Center_{msi_center_version}_x64.appx"

    with zipfile.ZipFile(appxbundle[0], "r") as file:
        file.extract(appx_file_name, extract_path)

    msi_center_sdk_path = "DCv2/Package/MSI%20Center%20SDK.exe"

    with zipfile.ZipFile(f"{extract_path}\\{appx_file_name}", "r") as file:
        file.extract(msi_center_sdk_path, extract_path)

    subprocess.call(
        [
            "innoextract",
            f"{extract_path}\\{msi_center_sdk_path}",
            "--output-dir",
            extract_path,
        ],
    )

    prepackage_path = f"{extract_path}\\tmp\\PrePackage"

    engine_lib_installer = glob.glob(f"{prepackage_path}\\Engine Lib_*.exe")

    if not engine_lib_installer:
        print("error: Engine Lib installer not found")
        return 1

    subprocess.call(
        ["innoextract", engine_lib_installer[0], "--output-dir", extract_path],
    )

    scewin_path = f"{extract_path}\\app\\Lib\\SCEWIN"

    scewin_version_folder = glob.glob(f"{scewin_path}\\*\\")

    if not scewin_version_folder:
        print("error: SCEWIN version folder not found")
        return 1

    # remove residual files
    for file in ("BIOSData.db", "BIOSData.txt", "SCEWIN.bat"):
        with contextlib.suppress(FileNotFoundError):
            os.remove(f"{scewin_version_folder[0]}\\{file}")

    for script in ("Import.bat", "Export.bat"):
        shutil.copy2(script, scewin_version_folder[0])

    shutil.move(scewin_path, ".")

    return 0


if __name__ == "__main__":
    sys.exit(main())
