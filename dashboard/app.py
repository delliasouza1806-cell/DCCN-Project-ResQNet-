"""
ResQNet Command Centre & Monitoring Dashboard (Phase 5)
Flask Application for Network Topology, Failure Experiments (E1-E7),
Live/Simulated Link Status, and OSPF Dynamic Recovery Analysis.
"""

import os
import csv
import time
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from probe import ping_once, measure_latency

app = Flask(__name__)

# Base path for project data files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "results.csv")

# Baseline Topology State (Aligned with Phase 1 & 4 specifications)
NETWORK_STATE = {
    "sites": [
        {"id": "CORE", "name": "R-CORE Backbone", "role": "Multilayer Switch 3560", "ip": "172.16.0.1", "location": "Central Hub", "status": "ONLINE"},
        {"id": "CTRL", "name": "Control Centre (R-CTRL)", "role": "Command & Emergency Servers", "ip": "172.16.0.2", "location": "Panaji", "status": "ONLINE"},
        {"id": "H1", "name": "Hospital 1 (R-H1)", "role": "District Hospital North", "ip": "172.16.0.6", "location": "Mapusa", "status": "ONLINE"},
        {"id": "H2", "name": "Hospital 2 (R-H2)", "role": "Goa Medical College", "ip": "172.16.0.10", "location": "Bambolim", "status": "ONLINE"},
        {"id": "H3", "name": "Hospital 3 (R-H3)", "role": "District Hospital South", "ip": "172.16.0.14", "location": "Margao", "status": "ONLINE"},
        {"id": "AMB", "name": "Ambulance Centre (R-AMB)", "role": "Emergency Dispatch", "ip": "172.16.0.18", "location": "Ponda", "status": "ONLINE"},
    ],
    "links": [
        {"id": "L-CORE-CTRL", "name": "CORE - CTRL", "from": "CORE", "to": "CTRL", "subnet": "172.16.0.0/30", "port": "Fa0/4", "type": "PRIMARY", "cost": 1, "status": "UP"},
        {"id": "L-CORE-H1", "name": "CORE - Hospital 1", "from": "CORE", "to": "H1", "subnet": "172.16.0.4/30", "port": "Fa0/1", "type": "PRIMARY", "cost": 1, "status": "UP"},
        {"id": "L-CORE-H2", "name": "CORE - Hospital 2", "from": "CORE", "to": "H2", "subnet": "172.16.0.8/30", "port": "Fa0/2", "type": "PRIMARY", "cost": 1, "status": "UP"},
        {"id": "L-CORE-H3", "name": "CORE - Hospital 3", "from": "CORE", "to": "H3", "subnet": "172.16.0.12/30", "port": "Fa0/3", "type": "PRIMARY", "cost": 1, "status": "UP"},
        {"id": "L-CORE-AMB", "name": "CORE - Ambulance", "from": "CORE", "to": "AMB", "subnet": "172.16.0.16/30", "port": "Fa0/5", "type": "PRIMARY", "cost": 1, "status": "UP"},
        {"id": "L-H1-H2", "name": "Hospital 1 - Hospital 2", "from": "H1", "to": "H2", "subnet": "172.16.0.20/30", "port": "G0/2", "type": "BACKUP", "cost": 50, "status": "STANDBY"},
        {"id": "L-H3-CTRL", "name": "Hospital 3 - Control Room", "from": "H3", "to": "CTRL", "subnet": "172.16.0.24/30", "port": "G0/2", "type": "BACKUP", "cost": 50, "status": "STANDBY"},
    ],
    "active_scenario": "NORMAL",
    "active_path_h1_ctrl": "H1 -> CORE -> CTRL (Primary)",
    "active_path_h3_ctrl": "H3 -> CORE -> CTRL (Primary)"
}

EVENT_LOG = [
    {"timestamp": datetime.now().strftime("%H:%M:%S"), "level": "INFO", "source": "OSPF-Engine", "message": "All 5 OSPF Area 0 neighbors reached FULL state on R-CORE."},
    {"timestamp": datetime.now().strftime("%H:%M:%S"), "level": "INFO", "source": "Services", "message": "DNS portal.resqnet.local and DHCP Relay operational on 10.10.0.66/67."},
    {"timestamp": datetime.now().strftime("%H:%M:%S"), "level": "SUCCESS", "source": "System", "message": "ResQNet Phase 5 Command Centre initialized."}
]


def load_results():
    """Load and parse the verified Phase 4 experiment results from results.csv."""
    results = []
    if not os.path.exists(CSV_PATH):
        return results

    with open(CSV_PATH, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            results.append({
                "experiment_id": row["experiment_id"],
                "experiment_name": row["experiment_name"],
                "run": int(row["run"]),
                "source_host": row["source_host"],
                "target_host": row["target_host"],
                "failure_applied": row["failure_applied"],
                "pings_sent": int(row["pings_sent"]),
                "pings_lost": int(row["pings_lost"]),
                "packet_loss_pct": float(row["packet_loss_pct"]),
                "recovery_time_s": float(row["recovery_time_s"]),
                "path_before": row["path_before"],
                "path_after": row["path_after"],
                "recovered": row["recovered"].lower() == "true",
                "notes": row["notes"]
            })
    return results


def log_event(level: str, source: str, message: str):
    """Append a timestamped event into the memory event log."""
    EVENT_LOG.insert(0, {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "level": level,
        "source": source,
        "message": message
    })
    # Keep only the latest 50 events
    if len(EVENT_LOG) > 50:
        EVENT_LOG.pop()


@app.route("/")
def index():
    """Render the primary ResQNet Command Centre dashboard."""
    return render_template("index.html")


@app.route("/api/status")
def api_status():
    """Return the current dynamic topology and site status."""
    return jsonify({
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "network": NETWORK_STATE
    })


@app.route("/api/experiments")
def api_experiments():
    """Return recorded experiment metrics and computed aggregation summaries."""
    results = load_results()

    # Aggregate summaries by experiment
    summary = {}
    for r in results:
        eid = r["experiment_id"]
        if eid not in summary:
            summary[eid] = {
                "id": eid,
                "name": r["experiment_name"],
                "failure": r["failure_applied"],
                "total_runs": 0,
                "avg_loss_pct": 0.0,
                "avg_recovery_s": 0.0,
                "recovered": r["recovered"],
                "path_before": r["path_before"],
                "path_after": r["path_after"]
            }
        summary[eid]["total_runs"] += 1
        summary[eid]["avg_loss_pct"] += r["packet_loss_pct"]
        if r["recovery_time_s"] >= 0:
            summary[eid]["avg_recovery_s"] += r["recovery_time_s"]

    for eid, s in summary.items():
        if s["total_runs"] > 0:
            s["avg_loss_pct"] = round(s["avg_loss_pct"] / s["total_runs"], 1)
            s["avg_recovery_s"] = round(s["avg_recovery_s"] / s["total_runs"], 2)

    return jsonify({
        "status": "success",
        "total_records": len(results),
        "results": results,
        "summary": summary
    })


@app.route("/api/events")
def api_events():
    """Return recent events from the monitoring timeline."""
    return jsonify({
        "status": "success",
        "events": EVENT_LOG
    })


@app.route("/api/simulate", methods=["POST"])
def api_simulate():
    """
    Simulate a failure/recovery scenario to demonstrate dynamic rerouting.
    Scenarios:
      - 'NORMAL': All links restored, OSPF converged on primary.
      - 'E2_CUT': Primary CORE-H1 cut; failover to H1-H2 backup.
      - 'E3_CUT': Primary CORE-H3 cut; failover to H3-CTRL backup.
      - 'E4_H2_OFF': Router R-H2 powered down.
      - 'E5_DUAL': Both CORE-H1 and H1-H2 cut; H1 isolated.
      - 'E7_STATIC': CORE-H1 cut under static routing (permanent drop).
    """
    data = request.get_json() or {}
    scenario = data.get("scenario", "NORMAL").upper()

    # Reset all links to default
    for link in NETWORK_STATE["links"]:
        if link["type"] == "PRIMARY":
            link["status"] = "UP"
        else:
            link["status"] = "STANDBY"
    for site in NETWORK_STATE["sites"]:
        site["status"] = "ONLINE"

    NETWORK_STATE["active_scenario"] = scenario

    if scenario == "NORMAL":
        NETWORK_STATE["active_path_h1_ctrl"] = "H1 -> CORE -> CTRL (Primary Metric 2)"
        NETWORK_STATE["active_path_h3_ctrl"] = "H3 -> CORE -> CTRL (Primary Metric 2)"
        log_event("SUCCESS", "Simulator", "Network reset to Normal Baseline (All Primary Links UP).")

    elif scenario == "E2_CUT":
        for link in NETWORK_STATE["links"]:
            if link["id"] == "L-CORE-H1":
                link["status"] = "DOWN"
            elif link["id"] == "L-H1-H2":
                link["status"] = "ACTIVE"
        NETWORK_STATE["active_path_h1_ctrl"] = "H1 -> H2 -> CORE -> CTRL (OSPF Failover Metric 52)"
        log_event("WARNING", "OSPF-Dijkstra", "Link Fa0/1 DOWN! R-H1 rerouting traffic via H1-H2 backup link (cost 50).")

    elif scenario == "E3_CUT":
        for link in NETWORK_STATE["links"]:
            if link["id"] == "L-CORE-H3":
                link["status"] = "DOWN"
            elif link["id"] == "L-H3-CTRL":
                link["status"] = "ACTIVE"
        NETWORK_STATE["active_path_h3_ctrl"] = "H3 -> CTRL direct backup (OSPF Failover Metric 51)"
        log_event("WARNING", "OSPF-Dijkstra", "Link Fa0/3 DOWN! R-H3 rerouting traffic via H3-CTRL direct backup link.")

    elif scenario == "E4_H2_OFF":
        for site in NETWORK_STATE["sites"]:
            if site["id"] == "H2":
                site["status"] = "OFFLINE"
        for link in NETWORK_STATE["links"]:
            if "H2" in [link["from"], link["to"]]:
                link["status"] = "DOWN"
        log_event("DANGER", "Health-Monitor", "R-H2 router unreachable (Power Loss). Other hospital rings unaffected.")

    elif scenario == "E5_DUAL":
        for link in NETWORK_STATE["links"]:
            if link["id"] in ["L-CORE-H1", "L-H1-H2"]:
                link["status"] = "DOWN"
        for site in NETWORK_STATE["sites"]:
            if site["id"] == "H1":
                site["status"] = "ISOLATED"
        NETWORK_STATE["active_path_h1_ctrl"] = "None (No route to destination - Hospital 1 Isolated)"
        log_event("DANGER", "Topology-Limit", "Dual link failure! Primary Fa0/1 and backup G0/2 severed. H1 is isolated.")

    elif scenario == "E7_STATIC":
        for link in NETWORK_STATE["links"]:
            if link["id"] == "L-CORE-H1":
                link["status"] = "DOWN"
        NETWORK_STATE["active_path_h1_ctrl"] = "None (Blackholed: Static routing has no alternative path)"
        log_event("DANGER", "Routing-Table", "Fa0/1 DOWN! Static routes cannot converge dynamically; 100% packet loss.")

    return jsonify({
        "status": "success",
        "scenario": scenario,
        "network": NETWORK_STATE
    })


@app.route("/api/probe", methods=["POST"])
def api_probe():
    """Trigger a probe measurement against a specified target IP."""
    data = request.get_json() or {}
    ip = data.get("ip", "10.10.0.66")
    res = measure_latency(ip, count=2)
    # If in sandbox or IP is unreachable, fall back gracefully
    if not res["success"]:
        res["note"] = "Local driver ping blocked or host unreachable (expected inside isolated sandbox)."
    return jsonify(res)


if __name__ == "__main__":
    # Run dashboard on default port 5000
    print("Starting ResQNet Command Centre Dashboard on http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
