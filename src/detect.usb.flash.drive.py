"""
MIT License

Copyright (c) 2025 Viki (VN)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Contact: contact@viki.design
Website: https://www.viki.design

"""


import os
import subprocess
import time
import threading
import time
import sys
import termios
import tty
import select

# Ignore large USB HDDs
MAX_USB_STICK_SIZE_GB = 256

quit_flag = False

def keyboard_listener():
    global quit_flag
    while not quit_flag:
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            ch = sys.stdin.read(1)
            if ch.lower() == 'q':
                quit_flag = True
                break
        time.sleep(0.1)

def get_block_devices():
    result = subprocess.run(["lsblk", "-dn", "-o", "NAME"], capture_output=True, text=True)
    return set(result.stdout.strip().split("\n"))

def read_sys_file(path):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def get_device_info(dev):
    info = {
        "name": dev,
        "path": f"/dev/{dev}",
        "size_gb": 0,
        "removable": False,
        "bus": "unknown",
        "vendor": "Unknown",
        "model": "Unknown",
    }

    size_str = read_sys_file(f"/sys/block/{dev}/size")
    if size_str and size_str.isdigit():
        sectors = int(size_str)
        info["size_gb"] = round(sectors * 512 / (1024 ** 3), 2)

    info["removable"] = read_sys_file(f"/sys/block/{dev}/removable") == "1"

    syspath = os.path.realpath(f"/sys/block/{dev}")
    if "usb" in syspath.lower():
        info["bus"] = "usb"

    vendor = read_sys_file(os.path.join(syspath, "device/vendor"))
    model = read_sys_file(os.path.join(syspath, "device/model"))
    if vendor:
        info["vendor"] = vendor.strip()
    if model:
        info["model"] = model.strip()

    return info

def detect_usb_stick(dev):
    info = get_device_info(dev)
    if info["bus"] == "usb" and info["removable"] and info["size_gb"] <= MAX_USB_STICK_SIZE_GB:
        return info
    return None

def main():
    global quit_flag
    initially_connected_usb_devices = get_block_devices()
    print("")
    print("Plug your USB flash drive (press 'q' to quit)")
    print("")

    listener_thread = threading.Thread(target=keyboard_listener, daemon=True)
    listener_thread.start()

    i = 0
    while not quit_flag:
        time.sleep(0.25)
        currently_connected_usb_devices = get_block_devices()
        newly_connected_usb_devices = list(currently_connected_usb_devices - initially_connected_usb_devices)
        initially_connected_usb_devices = currently_connected_usb_devices

        if newly_connected_usb_devices:
            print("")
            print("[ NEWLY CONNECTED USB DEVICE LIST ]")
            print("")

            for dev in newly_connected_usb_devices:
                info = detect_usb_stick(dev)
                if info:
                    print(f" [ {i} ] -> [ Path: {info['path']} ] | [ Vendor: {info['vendor']} ] | [ Model: {info['model']} ] | [ Size: {info['size_gb']} GB ]")
                else:
                    print(f" [ {i} ] -> [ {dev} is not recognized as a USB flash drive. ] ")
                i += 1

            i=0

if __name__ == "__main__":
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        main()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
