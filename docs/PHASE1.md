# Phase 1: Requirements and Network Design Specification

**Project:** ResQNet: Intelligent Emergency Response and Hospital Network Using Dynamic Routing  
**Course:** Data Communications and Computer Networks (CMP-302 / CMP-303)  
**Timeline:** Weeks 1 to 2  
**Owner:** Network Lead (Harsh Raikar)  
**Status:** Approved & Frozen Design  

---

## 1. Executive Summary & Objectives

The goal of Phase 1 is to freeze the complete network topology, device inventory, IPv4 addressing scheme (VLSM), routing architecture (OSPF Area 0), and security access policies on paper **before** touching Cisco Packet Tracer.

Every address and subnet calculation in this specification has been verified:
- Each department LAN uses a **/26 subnet** (yielding 62 usable host addresses).
- Each router-to-router point-to-point link uses a **/30 subnet** (yielding exactly 2 usable host addresses).
- Two dedicated high-cost backup links provide automated redundancy without causing routing loops.

---

## 2. Hardware Inventory & Role Allocation

| Device Identifier | Hardware Model | Primary Role | Interfaces & Connectivity |
| :--- | :--- | :--- | :--- |
| **R-CORE** | Cisco Catalyst 3560-24PS (Multilayer Switch) | Core Backbone Layer 3 routing; central interconnection for all sites | `Gig0/1` to CTRL<br>`Gig0/2` to H1<br>`Gig0/3` to H2<br>`Gig0/4` to H3<br>`Gig0/5` to AMB |
| **R-CTRL** | Cisco 2911 Integrated Services Router | Gateway for Emergency Control Room & Server Farm LAN | `Gig0/0`: 802.1Q trunk to SW-CTRL<br>`Gig0/1`: WAN link to R-CORE<br>`Gig0/2`: WAN backup link to R-H3 |
| **R-H1** | Cisco 2911 Router | Gateway for Hospital 1 (North / District General) | `Gig0/0`: 802.1Q trunk to SW-H1<br>`Gig0/1`: WAN link to R-CORE<br>`Gig0/2`: WAN backup link to R-H2 |
| **R-H2** | Cisco 2911 Router | Gateway for Hospital 2 (Central / Trauma Centre) | `Gig0/0`: 802.1Q trunk to SW-H2<br>`Gig0/1`: WAN link to R-CORE<br>`Gig0/2`: WAN backup link to R-H1 |
| **R-H3** | Cisco 2911 Router | Gateway for Hospital 3 (South / Specialty Care) | `Gig0/0`: 802.1Q trunk to SW-H3<br>`Gig0/1`: WAN link to R-CORE<br>`Gig0/2`: WAN backup link to R-CTRL |
| **R-AMB** | Cisco 2911 Router | Gateway for Ambulance Coordination Centres 1 & 2 | `Gig0/0`: 802.1Q trunk to SW-AMB<br>`Gig0/1`: WAN link to R-CORE |
| **SW-CTRL** | Cisco Catalyst 2960-24TT | Access switch for Control Room staff and central servers | `Fa0/24`: Trunk to R-CTRL<br>`Fa0/1`: Access VLAN 10 (Staff)<br>`Fa0/2`: Access VLAN 20 (Web/DNS)<br>`Fa0/3`: Access VLAN 20 (DHCP) |
| **SW-H1** | Cisco Catalyst 2960-24TT | Layer 2 distribution/access switch for Hospital 1 | `Fa0/24`: Trunk to R-H1<br>`Fa0/1..23`: Access ports for VLANs 110-140 |
| **SW-H2** | Cisco Catalyst 2960-24TT | Layer 2 distribution/access switch for Hospital 2 | `Fa0/24`: Trunk to R-H2<br>`Fa0/1..23`: Access ports for VLANs 110-140 |
| **SW-H3** | Cisco Catalyst 2960-24TT | Layer 2 distribution/access switch for Hospital 3 | `Fa0/24`: Trunk to R-H3<br>`Fa0/1..23`: Access ports for VLANs 110-140 |
| **SW-AMB** | Cisco Catalyst 2960-24TT | Layer 2 distribution/access switch for Ambulance Centres | `Fa0/24`: Trunk to R-AMB<br>`Fa0/1..23`: Access ports for VLANs 10 & 20 |
| **SRV-PORTAL** | Cisco Server-PT | Emergency Web Portal & Internal DNS Server (`portal.resqnet.local`) | Static IP: `10.10.0.66/26` |
| **SRV-DHCP** | Cisco Server-PT | Centralized DHCP Server (relay via IP helper addresses) | Static IP: `10.10.0.67/26` |

---

## 3. High-Level Network Topology Diagram

```text
                               +-----------------------------+
                               |           R-CORE            |
                               | (Cisco 3560 Layer 3 Switch) |
                               |     Router-ID: 1.1.1.1      |
                               +--------------+--------------+
                                              |
      +-------------------+-------------------+-------------------+-------------------+
      | (Primary)         | (Primary)         | (Primary)         | (Primary)         | (Primary)
      | 172.16.0.0/30     | 172.16.0.4/30     | 172.16.0.8/30     | 172.16.0.12/30    | 172.16.0.16/30
      v                   v                   v                   v                   v
+-----------+       +-----------+       +-----------+       +-----------+       +-----------+
|  R-CTRL   |       |   R-H1    |       |   R-H2    |       |   R-H3    |       |   R-AMB   |
| (2.2.2.2) |       | (3.3.3.3) |       | (4.4.4.4) |       | (5.5.5.5) |       | (6.6.6.6) |
+-----+-----+       +-----+-----+       +-----+-----+       +-----+-----+       +-----+-----+
      |                   |                   |                   |                   |
      |                   +====[BACKUP]=======+                   |                   |
      |                     172.16.0.20/30 (Cost 50)              |                   |
      |                                                           |                   |
      +==========================[BACKUP]=========================+                   |
                         172.16.0.24/30 (Cost 50)                                     |
      |                   |                   |                   |                   |
  Trunk to            Trunk to            Trunk to            Trunk to            Trunk to
   SW-CTRL             SW-H1               SW-H2               SW-H3               SW-AMB
      |                   |                   |                   |                   |
 +----+----+         +----+----+         +----+----+         +----+----+         +----+----+
 | VLAN 10 |         |VLAN 110 |         |VLAN 110 |         |VLAN 110 |         | VLAN 10 |
 | VLAN 20 |         |VLAN 120 |         |VLAN 120 |         |VLAN 120 |         | VLAN 20 |
 | (Servers|         |VLAN 130 |         |VLAN 130 |         |VLAN 130 |         +---------+
 | & Staff)|         |VLAN 140 |         |VLAN 140 |         |VLAN 140 |
 +---------+         +---------+         +---------+         +---------+
```

### Failover Resiliency Strategy
1. **Normal Operational State:** Traffic between all sites traverses the high-speed gigabit primary links connected to `R-CORE`.
2. **Hospital 1 Uplink Failure:** If link `R-CORE ↔ R-H1` fails, OSPF dead timers expire. OSPF immediately reroutes Hospital 1 traffic through `R-H2` over backup link `172.16.0.20/30`.
3. **Hospital 3 Uplink Failure:** If link `R-CORE ↔ R-H3` fails, OSPF reroutes Hospital 3 traffic through `R-CTRL` over backup link `172.16.0.24/30`.
4. **Metric Preference:** Backup links are configured with `ip ospf cost 50` (compared to default cost 1 on primary links), guaranteeing they remain silent standby links until a link state failure occurs.

---

## 4. Full IPv4 Addressing Plan

Subnet Mask for all LANs: `255.255.255.192` (`/26`, block size 64, 62 usable hosts).  
Subnet Mask for all WAN links: `255.255.255.252` (`/30`, block size 4, 2 usable hosts).

### 4.1 Site LAN Subnets (Hospitals, Control Room, Ambulance Centres)

| Location | VLAN ID | Purpose / Department | Subnet Network | Subnet Mask | Usable Host Range | Default Gateway | Broadcast Address |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Hospital 1** | 110 | Administration | `10.1.0.0/26` | `255.255.255.192` | `10.1.0.2` – `10.1.0.62` | `10.1.0.1` (`g0/0.110`) | `10.1.0.63` |
| **Hospital 1** | 120 | Doctors | `10.1.0.64/26` | `255.255.255.192` | `10.1.0.66` – `10.1.0.126` | `10.1.0.65` (`g0/0.120`) | `10.1.0.127` |
| **Hospital 1** | 130 | Nurses | `10.1.0.128/26` | `255.255.255.192` | `10.1.0.130` – `10.1.0.190` | `10.1.0.129` (`g0/0.130`) | `10.1.0.191` |
| **Hospital 1** | 140 | Emergency Critical | `10.1.0.192/26` | `255.255.255.192` | `10.1.0.194` – `10.1.0.254` | `10.1.0.193` (`g0/0.140`) | `10.1.0.255` |
| **Hospital 2** | 110 | Administration | `10.2.0.0/26` | `255.255.255.192` | `10.2.0.2` – `10.2.0.62` | `10.2.0.1` (`g0/0.110`) | `10.2.0.63` |
| **Hospital 2** | 120 | Doctors | `10.2.0.64/26` | `255.255.255.192` | `10.2.0.66` – `10.2.0.126` | `10.2.0.65` (`g0/0.120`) | `10.2.0.127` |
| **Hospital 2** | 130 | Nurses | `10.2.0.128/26` | `255.255.255.192` | `10.2.0.130` – `10.2.0.190` | `10.2.0.129` (`g0/0.130`) | `10.2.0.191` |
| **Hospital 2** | 140 | Emergency Critical | `10.2.0.192/26` | `255.255.255.192` | `10.2.0.194` – `10.2.0.254` | `10.2.0.193` (`g0/0.140`) | `10.2.0.255` |
| **Hospital 3** | 110 | Administration | `10.3.0.0/26` | `255.255.255.192` | `10.3.0.2` – `10.3.0.62` | `10.3.0.1` (`g0/0.110`) | `10.3.0.63` |
| **Hospital 3** | 120 | Doctors | `10.3.0.64/26` | `255.255.255.192` | `10.3.0.66` – `10.3.0.126` | `10.3.0.65` (`g0/0.120`) | `10.3.0.127` |
| **Hospital 3** | 130 | Nurses | `10.3.0.128/26` | `255.255.255.192` | `10.3.0.130` – `10.3.0.190` | `10.3.0.129` (`g0/0.130`) | `10.3.0.191` |
| **Hospital 3** | 140 | Emergency Critical | `10.3.0.192/26` | `255.255.255.192` | `10.3.0.194` – `10.3.0.254` | `10.3.0.193` (`g0/0.140`) | `10.3.0.255` |
| **Control Room** | 10 | Control Staff Operations | `10.10.0.0/26` | `255.255.255.192` | `10.10.0.2` – `10.10.0.62` | `10.10.0.1` (`g0/0.10`) | `10.10.0.63` |
| **Control Room** | 20 | Central Server Farm | `10.10.0.64/26` | `255.255.255.192` | `10.10.0.68` – `10.10.0.126` | `10.10.0.65` (`g0/0.20`) | `10.10.0.127` |
| **Ambulance Centre 1** | 10 | Dispatch Terminals | `10.20.0.0/26` | `255.255.255.192` | `10.20.0.2` – `10.20.0.62` | `10.20.0.1` (`g0/0.10`) | `10.20.0.63` |
| **Ambulance Centre 2** | 20 | Dispatch Terminals | `10.20.0.64/26` | `255.255.255.192` | `10.20.0.66` – `10.20.0.126` | `10.20.0.65` (`g0/0.20`) | `10.20.0.127` |

### 4.2 Central Dedicated Server Assignments

| Server Description | FQDN / Service Name | IP Address | Subnet Mask | Default Gateway | Connected Switch Port |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Emergency Web & DNS Server** | `portal.resqnet.local` | `10.10.0.66` | `255.255.255.192` | `10.10.0.65` | SW-CTRL `Fa0/2` (VLAN 20) |
| **DHCP Server** | `dhcp.resqnet.local` | `10.10.0.67` | `255.255.255.192` | `10.10.0.65` | SW-CTRL `Fa0/3` (VLAN 20) |

*Note: All subinterfaces across all hospital routers must be configured with `ip helper-address 10.10.0.67` to relay DHCP discover broadcasts across the routed network.*

### 4.3 Point-to-Point WAN Subnets

| Link Segment | Subnet CIDR | Side A Device & Port | Side A IP | Side B Device & Port | Side B IP | Link Category | OSPF Metric Cost |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CORE to CTRL** | `172.16.0.0/30` | R-CORE `Gig0/1` | `172.16.0.1` | R-CTRL `Gig0/1` | `172.16.0.2` | Primary | 1 (Default) |
| **CORE to H1** | `172.16.0.4/30` | R-CORE `Gig0/2` | `172.16.0.5` | R-H1 `Gig0/1` | `172.16.0.6` | Primary | 1 (Default) |
| **CORE to H2** | `172.16.0.8/30` | R-CORE `Gig0/3` | `172.16.0.9` | R-H2 `Gig0/1` | `172.16.0.10` | Primary | 1 (Default) |
| **CORE to H3** | `172.16.0.12/30` | R-CORE `Gig0/4` | `172.16.0.13` | R-H3 `Gig0/1` | `172.16.0.14` | Primary | 1 (Default) |
| **CORE to AMB** | `172.16.0.16/30` | R-CORE `Gig0/5` | `172.16.0.17` | R-AMB `Gig0/1` | `172.16.0.18` | Primary | 1 (Default) |
| **H1 to H2** | `172.16.0.20/30` | R-H1 `Gig0/2` | `172.16.0.21` | R-H2 `Gig0/2` | `172.16.0.22` | Backup | 50 (`ip ospf cost 50`) |
| **H3 to CTRL** | `172.16.0.24/30` | R-H3 `Gig0/2` | `172.16.0.25` | R-CTRL `Gig0/2` | `172.16.0.26` | Backup | 50 (`ip ospf cost 50`) |

---

## 5. Dynamic Routing Architecture (OSPF Area 0)

1. **Protocol:** Open Shortest Path First Version 2 (OSPFv2), Single Backbone Area `0`.
2. **Process ID:** `1` across all routers and Layer 3 switches.
3. **Explicit Router IDs (Preventing Ambiguity):**
   - `R-CORE`: `1.1.1.1`
   - `R-CTRL`: `2.2.2.2`
   - `R-H1`: `3.3.3.3`
   - `R-H2`: `4.4.4.4`
   - `R-H3`: `5.5.5.5`
   - `R-AMB`: `6.6.6.6`
4. **Network Type Configuration:** Every WAN link interface must specify:
   ```cisco
   ip ospf network point-to-point
   ```
   *Benefit:* Eliminates unnecessary DR/BDR (Designated Router) elections on point-to-point links, accelerating convergence time.
5. **Passive Interface Strategy:**
   - LAN subinterfaces facing hospital PCs, control room consoles, and servers do not run OSPF neighbor adjacencies.
   - Global standard:
     ```cisco
     router ospf 1
      passive-interface default
      no passive-interface <wan_interface_1>
      no passive-interface <wan_interface_2>
     ```
   *Benefit:* Blocks OSPF Hello packet leaks into end-user segments, securing the control plane against rogue neighbor attacks.

---

## 6. Access Control Policy (Security Matrix)

Extended Access Control Lists (ACLs) enforce strict department isolation and traffic priority:

| Source | Destination | Protocol / Port | Action | Purpose / Requirement |
| :--- | :--- | :--- | :--- | :--- |
| **Any LAN VLAN** | SRV-PORTAL (`10.10.0.66`) | HTTP (TCP 80), DNS (UDP 53), ICMP | **PERMIT** | Everyone must be able to resolve and view the portal |
| **Any LAN VLAN** | SRV-DHCP (`10.10.0.67`) | BootPS (UDP 67) | **PERMIT** | DHCP requests relayed by router must succeed |
| **Nurses (VLAN 130)** | Hospital Admin (`10.x.0.0/26`) | IP (All) | **DENY** | Strict HIPAA/privacy isolation between nurses and admin records |
| **Hospital Admin (VLAN 110)** | Doctors (`10.x.0.64/26`) | IP (All) | **DENY** | Administrative terminals cannot directly probe clinical doctor systems |
| **Emergency (VLAN 140)** | Control Staff (`10.10.0.0/26`) | All IP | **PERMIT** | High-priority emergency coordination channel |
| **Ambulance Dispatch** | Control Staff & Emergency Server | All required | **PERMIT** | Ambulance coordination and portal reporting |
| **Ambulance Dispatch** | Hospital Admin / Nurse VLANs | IP (All) | **DENY** | Ambulances have no clinical or administrative records access |
| **Any Non-Management VLAN** | Any Router VTY Lines | Telnet / SSH (TCP 22, 23) | **DENY** | Management access strictly reserved for Control Staff (`10.10.0.0/26`) |

*Critical Implementation Rule:* All extended ACLs applied inbound on router subinterfaces must start with `permit udp any any eq bootps` so host DHCP lease negotiation is not severed by the implicit deny.

---

## 7. Phase 1 Sign-Off & Verification Criteria

This network design is considered frozen and validated when:
- [x] All 16 department and server LAN subnets fit within standard private IPv4 address spaces without overlap.
- [x] All 7 point-to-point WAN links are assigned distinct `/30` blocks.
- [x] All primary and backup interface paths are clearly delineated with explicit metric costs.
- [x] Router-on-a-stick subinterface VLAN tags align exactly with switch 802.1Q trunk encap IDs.
- [x] Phase 1 blueprint is checked into source control ready for Phase 2 implementation.
