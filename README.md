# ResQNet

Intelligent Emergency Response and Hospital Network Using Dynamic Routing.
DCCN Lab Project (CMP-303), B.E. Computer Engineering.

ResQNet is a simulated emergency network joining one control room, three hospitals and two
ambulance centres, designed so communication survives a link or router failure. Recovery is
measured, not assumed.

## Layers

| Layer | What it is | Tools |
|-------|-----------|-------|
| A. Network | VLANs, subnetting, OSPF, DHCP, DNS, HTTP portal, ACLs, failure tests | Cisco Packet Tracer |
| B. Measured twin (recommended) | Small Linux copy of the core routers for real loss and recovery numbers | Mininet or GNS3, FRRouting, Wireshark |
| C. Dashboard | Web page showing link status, test results, recovery graphs | Python, Flask, Chart.js |

## Repository layout

| Folder | Holds |
|--------|-------|
| `pkt/` | Packet Tracer files, versioned: `resqnet_v1.pkt`, `resqnet_v2.pkt`, ... |
| `configs/` | Router and switch running-configs saved as text after every phase |
| `scripts/` | Test scripts, twin network scripts, environment checker |
| `dashboard/` | Flask app (`app.py`, `probe.py`, `templates/`, `static/`) |
| `captures/` | Wireshark `.pcapng` captures and screenshots |
| `docs/` | Phase documentation, synopsis, final report, demo script |

## Quick start (Phase 0)

1. Install the tools listed in `docs/PHASE0.md`.
2. Run the environment checker:
   ```
   python3 scripts/check_env.py
   ```
   On Windows use `py scripts\check_env.py`.
3. Fill in `docs/TEAM.md` with names, roles and roll numbers.
4. Read `CONTRIBUTING.md` for the naming rules.

## Phases

| Phase | Weeks | Status |
|-------|-------|--------|
| 0. Team, tools, setup | 1 | Scaffold ready, see `docs/PHASE0.md` |
| 1. Requirements and design | 1-2 | Complete, see `docs/PHASE1.md` |
| 2. Core network in Packet Tracer | 2-3 | Not started |
| 3. Services and security | 3-4 | Not started |
| 4. Failure and recovery experiments | 4-5 | Not started |
| 5. Dashboard and measured twin | 5-6 | Not started |
| 6. Packet analysis, documentation, demo | 6 | Not started |

## Honesty rules

- Every number on the dashboard comes from a recorded test, never typed in by hand.
- The portal uses demonstration data only, never real patient information.
- Limitations are stated in the report: simulated timings, no real-disaster proof.
