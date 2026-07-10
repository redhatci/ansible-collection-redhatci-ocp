"""Collect hardware information using native RHCOS tools.

Fallback for lshw when the node cannot reach external package
repositories. Uses dmidecode, lscpu, lsblk, lspci, and ip,
all shipped with RHCOS.

Output mimics the top-level structure of lshw -json so the
downstream save task (from_json | dot_to_underscore) works
without changes.
"""

import json
import os
import subprocess


def run(cmd):
    try:
        return subprocess.check_output(
            cmd, shell=True, stderr=subprocess.DEVNULL, timeout=30
        ).decode().strip()
    except Exception:
        return ""


def collect_system():
    return {
        "description": run("dmidecode -s system-product-name"),
        "vendor": run("dmidecode -s system-manufacturer"),
    }


def collect_bios():
    return {
        "id": "firmware",
        "class": "memory",
        "description": "BIOS",
        "vendor": run("dmidecode -s bios-vendor"),
        "version": run("dmidecode -s bios-version"),
    }


def collect_cpu():
    cpu = {}
    for line in run("lscpu").splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            cpu[k.strip()] = v.strip()
    mhz = cpu.get("CPU MHz", cpu.get("CPU max MHz", "0"))
    return {
        "id": "cpu",
        "class": "processor",
        "product": cpu.get("Model name", "Unknown"),
        "vendor": cpu.get("Vendor ID", "Unknown"),
        "units": "Hz",
        "size": int(float(mhz) * 1_000_000),
        "configuration": {
            "cores": cpu.get("CPU(s)", "0"),
            "sockets": cpu.get("Socket(s)", "1"),
            "threads_per_core": cpu.get("Thread(s) per core", "1"),
        },
    }


def collect_memory():
    with open("/proc/meminfo") as f:
        for line in f:
            if line.startswith("MemTotal"):
                return {
                    "id": "memory",
                    "class": "memory",
                    "description": "System Memory",
                    "units": "bytes",
                    "size": int(line.split()[1]) * 1024,
                }
    return {"id": "memory", "class": "memory", "size": 0}


def collect_storage():
    raw = run("lsblk -Jb -o NAME,SIZE,TYPE,MODEL")
    if raw:
        try:
            blk = json.loads(raw)
            return {
                "id": "storage",
                "class": "storage",
                "children": blk.get("blockdevices", []),
            }
        except json.JSONDecodeError:
            pass
    return {"id": "storage", "class": "storage", "children": []}


def collect_pci():
    children = []
    for line in run("lspci -nn").splitlines():
        parts = line.split(" ", 1)
        if len(parts) == 2:
            children.append({
                "businfo": "pci@" + parts[0],
                "description": parts[1],
            })
    return {"id": "pci", "class": "bus", "children": children}


def collect_nic_firmware():
    """Collect NIC driver and firmware versions via ethtool -i.

    Only probes physical (PCI-backed) interfaces by checking for
    /sys/class/net/<iface>/device.
    """
    children = []
    try:
        ifaces = sorted(os.listdir("/sys/class/net"))
    except OSError:
        return children
    for iface in ifaces:
        if not os.path.exists(f"/sys/class/net/{iface}/device"):
            continue
        info = run(f"ethtool -i {iface}")
        if not info:
            continue
        props = {}
        for line in info.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                props[k.strip()] = v.strip()
        if props.get("firmware-version"):
            children.append({
                "logicalname": iface,
                "configuration": {
                    "driver": props.get("driver", ""),
                    "firmware": props.get("firmware-version", ""),
                },
            })
    return children


def collect_network():
    link_info = []
    raw = run("ip -j link show")
    if raw:
        try:
            link_info = json.loads(raw)
        except json.JSONDecodeError:
            pass
    firmware_info = collect_nic_firmware()
    return {
        "id": "network",
        "class": "network",
        "children": link_info,
        "firmware": firmware_info,
    }


def main():
    system = collect_system()
    data = {
        "id": "computer",
        "class": "system",
        "description": system["description"],
        "vendor": system["vendor"],
        "serial": "REDACTED",
        "configuration": {"collection_method": "native-tools-fallback"},
        "children": [
            collect_bios(),
            collect_cpu(),
            collect_memory(),
            collect_storage(),
            collect_pci(),
            collect_network(),
        ],
    }
    print(json.dumps(data))


if __name__ == "__main__":
    main()
