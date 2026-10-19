# Phase 0: Team, Tools and Setup

**Project:** ResQNet (CMP-303 DCCN Lab) | **Timeline:** Week 1 | **Source:** ResQNet Implementation Plan, Phase 0

**Goal:** everyone can open the same project file and run the same tools.

**Done when:** all four roles are assigned, every team member has passed the environment check,
the repository is shared with its folder structure, and the naming and config-saving rules are agreed.

---

## 1. What Phase 0 delivers

| Deliverable | Location | Status |
|-------------|----------|--------|
| Project folder with the six subfolders | `resqnet/` | Created |
| Folder guides | `*/README.md` | Created |
| Naming and config-saving rules | `CONTRIBUTING.md` | Created |
| Environment checker | `scripts/check_env.py` | Created |
| Team and roles sheet | `docs/TEAM.md` | Template ready, team to fill in |
| Tool installs on every laptop | Each member's machine | Team to complete (section 4) |
| Project folder shared with the team | Shared drive or zip | Team to complete (section 3) |

Items marked "Team to complete" need accounts and installs on your own machines, which cannot
be done from here.

## 2. Repository structure

```
resqnet/
├── README.md            project overview and quick start
├── CONTRIBUTING.md      naming and config-saving rules
├── requirements.txt     Python packages (Flask for the dashboard)
├── pkt/                 Packet Tracer files (resqnet_v1.pkt, ...)
├── configs/             running-configs as text, one folder per phase
├── scripts/             check_env.py now; probes and twin scripts later
├── dashboard/           Flask app (Phase 5)
├── captures/            Wireshark captures and screenshots
└── docs/                PHASE0.md, TEAM.md, later the report and demo script
```

## 3. Shared setup procedure

### 3.1 Share the project folder

1. Extract `resqnet_phase0.zip` to a folder on one laptop, for example `C:\Users\<you>\resqnet`.
2. Put a copy in a shared place the whole team can reach (Google Drive, OneDrive, or a
   pen drive) and have every member copy it to their own laptop.
3. Because `.pkt` files cannot be merged, the shared copy is only updated by whoever holds
   the latest `.pkt` (see 3.2). Everyone else copies the newest version down before working.

### 3.2 Agree the Packet Tracer file rule

`.pkt` files are binary and cannot be merged, so two people's edits cannot be combined. The plan's rule is the safe one:

- Name versions `resqnet_v1.pkt`, `resqnet_v2.pkt`, and so on.
- Never overwrite a working version; use File > Save As with the next number.
- One person edits at a time and announces it in the team chat.
- Log each version in `pkt/README.md`.

### 3.3 Agree the config-saving rule

After every phase, on every device:

```
copy running-config startup-config
show running-config
```

Paste the output into `configs/<phase>/<device>.txt` (for example `configs/phase2/R-H1.txt`).

These text files are the recovery path if a `.pkt` file is
lost or corrupted.

## 4. Install checklist (per team member)

| Tool | Purpose | Where to get it | Required |
|------|---------|-----------------|----------|
| Cisco Packet Tracer | Build and simulate the network (Layer A) | Free via Cisco Networking Academy (netacad link in the lab syllabus) | Yes |
| Wireshark | Packet analysis | wireshark.org | Yes |
| Python 3 | Test scripts and Flask dashboard | python.org | Yes |
| VS Code | Editing scripts and docs | code.visualstudio.com | Recommended |
| draw.io | Topology and flow diagrams | diagrams.net | Recommended |
| Ubuntu VM or WSL2 | Host for the measured twin | Microsoft Store (WSL2) or any VM tool | Optional (Layer B) |
| Mininet, FRRouting | Measured twin network | `sudo apt install mininet frr` inside Ubuntu | Optional (Layer B) |

Hardware guidance from the synopsis: a laptop with 8 GB RAM or more, running Windows or Linux
(WSL2 or an Ubuntu VM for the optional twin).

### Python setup

```
cd resqnet
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 5. Verify the setup

Run the checker from the repository root:

```
python3 scripts/check_env.py     # Windows: py scripts\check_env.py
```

How to read the output:

| Status | Meaning |
|--------|---------|
| PASS | Found and working |
| WARN | Optional tool missing, or a GUI app that cannot be auto-detected (Packet Tracer) |
| FAIL | Required item missing; fix and re-run |

The script exits with code 0 only when every required check passes. Each member runs it on their
own laptop and ticks their name in the sign-off table below.

Packet Tracer is a GUI application, so the script can only look in common install locations. If
it shows WARN, confirm manually: open Packet Tracer, sign in with your Networking Academy
account, and open a blank project.

## 6. Roles

Suggested split from the plan (merge if the team is smaller). Names go in `docs/TEAM.md`.

| Role | Owns | Main phases |
|------|------|-------------|
| Network lead | Topology, addressing, routers, OSPF | 1, 2, 4 |
| Services and security lead | DHCP, DNS, HTTP portal, VLANs, ACLs | 2, 3 |
| Dashboard developer | Flask app, test scripts, twin network | 5 |
| Testing and documentation lead | Experiments, Wireshark, synopsis, report, demo | 4, 6 |

For a team of three, merge Testing and documentation into the Network lead's experiment work
and give the Dashboard developer the documentation. For two, pair Network with Services and
Dashboard with Testing.

## 7. Sign-off checklist

Phase 0 is complete when every box is ticked.

- [ ] All roles assigned in `docs/TEAM.md`, lab submission date recorded
- [ ] Project folder copied to every member's laptop and a shared copy agreed
- [ ] Packet Tracer installed and opening a blank project on every laptop
- [ ] Wireshark and Python 3 installed on every laptop
- [ ] `scripts/check_env.py` shows no FAIL on every laptop
- [ ] Naming rule (`resqnet_vN.pkt`) and single-editor rule agreed
- [ ] Config-saving rule agreed and understood
- [ ] Decision made on Layer B: attempt the measured twin or start with Option A only

| Member | check_env.py passed | Packet Tracer opens | Date |
|--------|---------------------|---------------------|------|
| | | | |
| | | | |
| | | | |
| | | | |

## 8. Risks specific to this phase

| Risk | Fix |
|------|-----|
| Two people save over the same `.pkt` | Single-editor rule, versioned names, version log in `pkt/README.md` |
| `.pkt` file lost or corrupted | Saved text configs in `configs/` rebuild every device |
| Packet Tracer access delayed (Networking Academy sign-up) | Start enrolment on day one; it is the longest lead item |
| Twin setup eats time later | Decide now: Option A first, Layer B as an upgrade |
| Windows laptop cannot run Mininet | Use WSL2 or an Ubuntu VM; or skip Layer B and use Option A |

## 9. Handover to Phase 1

Phase 1 freezes the topology and addressing plan on paper before touching Packet Tracer.
The addressing in the implementation plan is already complete and checked (each /26 holds 62
hosts, each /30 holds 2), so Phase 1 is a review and approval step. Bring the team sheet,
the signed-off checklist above, and a draw.io topology diagram based on Figure 1 of the synopsis.
