"""Collect hardware information using native RHCOS tools.

Fallback for lshw when the node cannot reach external package
repositories. Uses dmidecode, lscpu, lsblk, lspci, and ip,
all shipped with RHCOS.

Output mimics the top-level structure of lshw -json so the
downstream save task (from_json | dot_to_underscore) works
without changes.
"""

import json
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


def collect_network():
    raw = run("ip -j link show")
    if raw:
        try:
            return {
                "id": "network",
                "class": "network",
                "children": json.loads(raw),
            }
        except json.JSONDecodeError:
            pass
    return {"id": "network", "class": "network", "children": []}


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
