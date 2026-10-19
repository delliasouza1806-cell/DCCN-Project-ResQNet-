#!/usr/bin/env python3
"""ResQNet Phase 0 environment checker.

Run:  python3 scripts/check_env.py        (Windows: py scripts\\check_env.py)

Checks that the tools the project needs are installed and prints a PASS / WARN / FAIL
line for each. Required tools must pass; optional tools (Layer B twin) only warn.
Exit code is 0 when every required check passes, 1 otherwise.
"""
import importlib.util
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_FOLDERS = ["pkt", "configs", "scripts", "dashboard", "captures", "docs"]

results = []  # (status, name, detail)


def record(status, name, detail=""):
    results.append((status, name, detail))
    print(f"[{status:<4}] {name}" + (f" - {detail}" if detail else ""))


def run(cmd):
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        return (out.stdout or out.stderr).strip().splitlines()[0] if (out.stdout or out.stderr) else ""
    except Exception:
        return ""


def check_python():
    v = sys.version_info
    ok = v >= (3, 9)
    record("PASS" if ok else "FAIL", "Python 3.9+", f"found {v.major}.{v.minor}.{v.micro}")


def check_module(mod, pip_name, required):
    found = importlib.util.find_spec(mod) is not None
    if found:
        record("PASS", f"Python package {pip_name}")
    else:
        record("FAIL" if required else "WARN", f"Python package {pip_name}",
               f"install with: pip install {pip_name}")


def check_cmd(cmd, label, required, version_args=("--version",), hint=""):
    path = shutil.which(cmd)
    if path:
        record("PASS", label, run([path, *version_args]) or path)
    else:
        record("FAIL" if required else "WARN", label, hint or "not found on PATH")


def check_wireshark():
    # Wireshark GUI is often not on PATH; tshark or the default Windows folder counts.
    for cmd in ("wireshark", "tshark"):
        if shutil.which(cmd):
            record("PASS", "Wireshark", f"{cmd} found")
            return
    win = Path(os.environ.get("ProgramFiles", "C:\\Program Files")) / "Wireshark" / "Wireshark.exe"
    if win.exists():
        record("PASS", "Wireshark", str(win))
        return
    record("FAIL", "Wireshark", "install from wireshark.org")


def check_packet_tracer():
    # Packet Tracer is a GUI app with no reliable PATH entry; look in common places.
    candidates = [
        shutil.which("packettracer"),
        shutil.which("PacketTracer"),
        shutil.which("PacketTracer7"),
        r"C:\Program Files\Cisco Packet Tracer\bin\PacketTracer.exe",
        "/opt/pt/bin/PacketTracer",
        "/Applications/Cisco Packet Tracer/Cisco Packet Tracer.app",
    ]
    for c in candidates:
        if c and Path(c).exists():
            record("PASS", "Cisco Packet Tracer", str(c))
            return
    record("WARN", "Cisco Packet Tracer",
           "not auto-detected; confirm by opening it and signing in with Networking Academy")


def check_twin_tools():
    on_linux = platform.system() == "Linux"
    if not on_linux:
        record("WARN", "Layer B twin (Mininet, FRRouting)",
               "needs Ubuntu VM or WSL2; optional, finish Option A first")
        return
    check_cmd("mn", "Mininet", False, ("--version",), "optional: sudo apt install mininet")
    check_cmd("vtysh", "FRRouting (vtysh)", False, ("--version",), "optional: sudo apt install frr")


def check_folders():
    missing = [f for f in REQUIRED_FOLDERS if not (ROOT / f).is_dir()]
    if missing:
        record("FAIL", "Repo folders", "missing: " + ", ".join(missing))
    else:
        record("PASS", "Repo folders", ", ".join(REQUIRED_FOLDERS))


def check_ram():
    try:
        if platform.system() == "Linux":
            with open("/proc/meminfo") as f:
                kb = int(f.readline().split()[1])
            gb = kb / 1024 / 1024
            record("PASS" if gb >= 7.5 else "WARN", "RAM 8 GB or more", f"{gb:.1f} GB")
            return
    except Exception:
        pass
    record("WARN", "RAM 8 GB or more", "could not detect; check manually")


def main():
    print(f"ResQNet environment check - {platform.system()} {platform.release()}\n")
    print("Required")
    check_python()
    check_wireshark()
    check_module("flask", "flask", True)
    check_cmd("code", "VS Code", False, hint="optional editor; any editor works")
    check_packet_tracer()
    check_folders()

    print("\nOptional (Layer B measured twin and dashboard extras)")
    check_ram()
    check_module("flask_socketio", "flask-socketio", False)
    check_twin_tools()

    fails = [r for r in results if r[0] == "FAIL"]
    warns = [r for r in results if r[0] == "WARN"]
    print(f"\nSummary: {sum(r[0]=='PASS' for r in results)} passed, "
          f"{len(warns)} warnings, {len(fails)} failed")
    if fails:
        print("Fix the FAIL items above, then run this script again.")
        return 1
    print("Phase 0 environment is ready." + (" Review the warnings when you have time." if warns else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
