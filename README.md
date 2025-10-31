# USB Flash Drive Detector

A Linux command-line utility that monitors your system for newly connected USB flash drives in real time.

This tool helps you identify USB sticks, showing their **device path, vendor, model, and size**,  while ignoring large external hard drives.

---

## What’s the Purpose of This Utility?

1. **Detect newly inserted USB flash drives** in real time and display their device paths, vendor, model, and size.
2. **Useful when creating bootable USB drives** - helps you identify the correct target device (e.g., `/dev/sdb`) before using tools like `dd`.
   This prevents accidental overwriting of your **internal hard drive**, which can lead to **data loss or corruption**.

---

## Installation

To install the utility system-wide, simply clone the repository and run the installer script:

```bash
git clone https://github.com/neoviki/linux.detect.usb.flash.drive
cd linux.detect.usb.flash.drive
./installer.sh
```

---

## Uninstallation

To remove the utility completely:

```bash
./uninstaller.sh
```

---

## Usage

Once installed, run:

```bash
detect.usb.flash.drive
```

Then plug in a USB flash drive to see the detected USB flash drive details.

---

### Example Output

```
Plug your USB flash drive (press 'q' to quit)

[ NEWLY CONNECTED USB DEVICE LIST ]

 [ 0 ] -> [ Path: /dev/sdb ] | [ Vendor: SanDisk ] | [ Model: Ultra Fit ] | [ Size: 32.0 GB ]
```

---

## Features

    1. Detects newly inserted USB flash drives
    2. Displays **path, vendor, model, and size**
    3. Ignores large USB HDDs (>256 GB by default)
    4. Non-blocking key listener - press **`q`** anytime to quit
    5. Works on **Linux** systems (tested on Ubuntu/Debian/Fedora)

---

## Requirements

* **Python 3.6+**
* **Linux** with `/sys` and `lsblk` support
* `bash` shell for the wrapper script

---

## Tested Systems

This utility has been tested and verified on:

    1. Ubuntu 24.04 LTS

Other modern Linux distributions with lsblk and /sys support should work, but have not been tested.
