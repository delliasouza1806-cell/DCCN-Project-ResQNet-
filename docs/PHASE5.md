# Phase 5: Command Centre Dashboard and Measured Twin

**Project:** ResQNet: Intelligent Emergency Response and Hospital Network Using Dynamic Routing  
**Course:** Data Communications and Computer Networks (CMP-302 / CMP-303)  
**Timeline:** Weeks 5 to 6  
**Status:** Complete and Verified  

---

## 1. Executive Summary & Goals

The primary objective of **Phase 5** is to bridge network simulation with real-world visibility by providing an interactive web-based **Command Centre Monitoring Dashboard** (Layer C) alongside an automated **Network Measurement Probe** (Layer B).

### The Golden Honesty Rule
A core tenet of the ResQNet project is academic and engineering honesty:
> **Every single number, packet loss percentage, convergence duration, and routing path displayed on the dashboard is derived directly from the recorded Phase 4 experiment runs (E1 through E7). No metric is hardcoded, guessed, or typed by hand.**

---

## 2. System Architecture

The Phase 5 subsystem operates as follows:

```
+-----------------------------------------------------------------------+
|                    Layer C: Command Centre Dashboard                  |
|          (HTML5 / CSS3 / JavaScript / Chart.js / SVG Topology)        |
+-----------------------------------------------------------------------+
                                    ▲
                                    │ REST API JSON
                                    ▼
+-----------------------------------------------------------------------+
|                    Flask Application (dashboard/app.py)               |
|   Endpoints: /, /api/status, /api/experiments, /api/simulate, /api/events |
+-----------------------------------------------------------------------+
          ▲                                           ▲
          │ Loads verified data                       │ Probes & tests
          ▼                                           ▼
+-----------------------------+             +---------------------------+
|    dashboard/results.csv    |             |    dashboard/probe.py     |
|   35 Measured Runs (E1-E7)  |             | ICMP & TCP Service Probes |
+-----------------------------+             +---------------------------+
```

---

## 3. Component Details

### 3.1 Data Store (`dashboard/results.csv`)
Stores all 35 experimental runs recorded during Phase 4 across experiments E1 to E7:
* **E1 (Baseline)**: 5 runs, 0/60 pings lost, 0.0s outage. Normal path `H1 -> CORE -> CTRL`.
* **E2 (Cut CORE-H1 Link - Default OSPF)**: 5 runs, 1/60 pings lost, 1.0s outage. Failover to backup link `H1 -> H2 -> CORE -> CTRL` (Cost 52).
* **E3 (Cut CORE-H3 Link)**: 5 runs, 1/60 pings lost, 1.0s outage. Failover to direct backup link `H3 -> CTRL` (Cost 51).
* **E4 (Power Off Router R-H2)**: 5 runs, 0/60 pings lost from H1. Proves isolated failure does not disrupt independent hospital communication.
* **E5 (Dual Link Cut - CORE-H1 & H1-H2)**: 5 runs, 50-51 pings lost (83-85% loss). Demonstrates topological limit (H1 completely isolated).
* **E6 (Cut CORE-H1 - Tuned Timers 1s/3s)**: 5 runs, 1/60 pings lost, 0.8s outage. Proves hello/dead timer tuning accelerates convergence.
* **E7 (Static Routing Baseline)**: 5 runs, 49/60 pings lost (81.7% loss, unrecovered). Proves static routing lacks dynamic healing capabilities.

### 3.2 Network Probe (`dashboard/probe.py`)
* Implements cross-platform ICMP reachability (`ping_once`), latency measurement (`measure_latency`), TCP socket service check (`check_tcp_port`), and continuous outage interval tracking (`measure_outage`).
* Supports Windows (`ping -n 1 -w 1000`) and POSIX (`ping -c 1 -W 1`).

### 3.3 Backend API (`dashboard/app.py`)
Flask REST server providing:
| Route | Method | Purpose |
| :--- | :--- | :--- |
| `/` | `GET` | Serves the interactive Command Centre Dashboard UI. |
| `/api/status` | `GET` | Returns live/simulated state of all 6 sites and 7 WAN links. |
| `/api/experiments` | `GET` | Returns parsed records and aggregated summary statistics from `results.csv`. |
| `/api/simulate` | `POST` | Toggles dynamic failure scenarios (`NORMAL`, `E2_CUT`, `E3_CUT`, `E4_H2_OFF`, `E5_DUAL`, `E7_STATIC`). |
| `/api/events` | `GET` | Returns the latest chronological event log of network state transitions. |
| `/api/probe` | `POST` | Executes real-time ping against an IP target. |

### 3.4 Frontend Command Centre (`index.html`, `style.css`, `app.js`)
* **Live Dynamic SVG Topology**: R-CORE in center connected to R-CTRL, R-H1, R-H2, R-H3, and R-AMB. Primary links render green (UP) or red dashed (DOWN); backup links render standby dashed or pulsing blue (ACTIVE FAILOVER).
* **Interactive Scenario Replay**: Evaluators can click scenario buttons to visually witness Dijkstra SPF route convergence and backup link activation in real-time.
* **Chart.js Visualizations**:
  1. *Packet Loss Bar Chart*: Compares % packet loss across all seven failure scenarios.
  2. *Convergence Duration Comparison*: Demonstrates Default OSPF (1.0s) vs Tuned OSPF (0.8s) vs Static Routing (Permanent Drop / Unrecovered).
* **Searchable Experiment Run Table**: Shows all 35 recorded trials with filtering by experiment ID.
* **Real-Time Event Terminal**: Displays timestamped alerts for routing updates and link cuts.

---

## 4. Running the Dashboard

### Prerequisites
Ensure Python 3 and Flask are installed:
```powershell
pip install Flask
```

### Starting the Server
From the project root:
```powershell
cd dashboard
python app.py
```

Open a web browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 5. Demonstration & Viva Guide (3 Minutes)

1. **Overview & Topology**: Point out the 6-node topology with the central 3560 switch (R-CORE), 5 edge routers, and the two high-cost backup links (H1-H2 and H3-CTRL). Show the KPI ribbon showing all 5 primary links healthy.
2. **Dynamic OSPF Failover (E2 Simulation)**: Click **"Cut CORE-H1 Link (E2)"**. Point out how link Fa0/1 turns red, the backup link H1-H2 activates in blue, and the active path updates from metric 2 to metric 52 (`H1 -> H2 -> CORE -> CTRL`).
3. **Data Integrity & Honesty**: Scroll to the Chart.js graphs and the 35-run experiment table to demonstrate that every data point reflects genuine measured runs from Phase 4.
4. **Static vs Dynamic Comparison**: Click **"Static Routes Cut (E7)"** and show that without dynamic OSPF, packets are permanently blackholed (>80% packet loss, no failover).
