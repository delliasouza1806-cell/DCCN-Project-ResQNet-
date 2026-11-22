"""
ResQNet Network Probe (Layer B / Dashboard Utility)
Measures latency, packet drops, service reachability, and outage recovery times.
Cross-platform: Windows (-n 1 -w ms) and POSIX (-c 1 -W s).
"""

import subprocess
import platform
import time
import socket


def ping_once(ip: str, timeout_ms: int = 1000) -> bool:
    """Send a single ICMP echo request to the target IP address."""
    is_windows = platform.system().lower() == "windows"
    if is_windows:
        cmd = ["ping", "-n", "1", "-w", str(timeout_ms), ip]
    else:
        timeout_s = max(1, timeout_ms // 1000)
        cmd = ["ping", "-c", "1", "-W", str(timeout_s), ip]

    try:
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return res.returncode == 0
    except Exception:
        return False


def measure_latency(ip: str, count: int = 3) -> dict:
    """Measure average round-trip time and packet success rate."""
    is_windows = platform.system().lower() == "windows"
    if is_windows:
        cmd = ["ping", "-n", str(count), "-w", "1000", ip]
    else:
        cmd = ["ping", "-c", str(count), "-W", "1", ip]

    t0 = time.time()
    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
        elapsed = round((time.time() - t0) * 1000 / count, 2)
        success = (res.returncode == 0)
        return {
            "target": ip,
            "success": success,
            "latency_ms": elapsed if success else None,
            "details": res.stdout.strip()
        }
    except Exception as e:
        return {
            "target": ip,
            "success": False,
            "latency_ms": None,
            "error": str(e)
        }


def check_tcp_port(ip: str, port: int, timeout: float = 1.5) -> bool:
    """Check if a TCP service (HTTP: 80, DNS: 53) is reachable."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((ip, port))
        sock.close()
        return True
    except Exception:
        return False


def measure_outage(ip: str, duration: float = 15.0, step: float = 0.5) -> dict:
    """
    Continually probes an IP over a time window and records packet drop timeline
    to calculate real recovery / outage duration.
    """
    log = []
    t0 = time.time()
    while (time.time() - t0) < duration:
        timestamp_offset = round(time.time() - t0, 2)
        is_up = ping_once(ip, timeout_ms=int(step * 1000))
        log.append({"time_s": timestamp_offset, "ok": is_up})
        time.sleep(step)

    lost = [entry["time_s"] for entry in log if not entry["ok"]]
    outage_seconds = round((lost[-1] - lost[0] + step), 2) if lost else 0.0

    return {
        "target": ip,
        "total_probes": len(log),
        "lost_count": len(lost),
        "loss_percent": round((len(lost) / len(log)) * 100, 1) if log else 0.0,
        "outage_s": outage_seconds,
        "timeline": log
    }


if __name__ == "__main__":
    test_ip = "127.0.0.1"
    print(f"Testing local probe against {test_ip}...")
    up = ping_once(test_ip)
    print(f"Ping result: {'UP' if up else 'DOWN'}")
    latency = measure_latency(test_ip, count=2)
    print(f"Latency check: {latency}")
