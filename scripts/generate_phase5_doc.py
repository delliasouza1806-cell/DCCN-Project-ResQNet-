"""
ResQNet Phase 5 Document Generator
Builds formatted Word Document (.docx) matching the exact styling of ResQNet_Phase1.docx.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls


def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)


def style_table(table, col_widths, col_names):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = table.rows[0]
    for i, name in enumerate(col_names):
        cell = hdr.cells[i]
        cell.text = name
        set_cell_background(cell, '0F4C81')
        set_cell_margins(cell, top=140, bottom=140, left=150, right=150)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for r in p.runs:
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            r.font.size = Pt(9.5)
            r.font.name = 'Calibri'

    for row in table.rows[1:]:
        for cell in row.cells:
            set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.size = Pt(9)
                r.font.name = 'Calibri'
                r.font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    for row in table.rows:
        for i, w in enumerate(col_widths):
            row.cells[i].width = Inches(w)


def build_phase5_doc(output_path):
    doc = docx.Document()

    # Page setup
    for sec in doc.sections:
        sec.top_margin = Inches(0.75)
        sec.bottom_margin = Inches(0.75)
        sec.left_margin = Inches(0.75)
        sec.right_margin = Inches(0.75)
        sec.page_width = Inches(8.5)
        sec.page_height = Inches(11.0)

    # Document Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    r_title = p_title.add_run('ResQNet')
    r_title.bold = True
    r_title.font.size = Pt(24)
    r_title.font.name = 'Calibri'
    r_title.font.color.rgb = RGBColor(0x0F, 0x4C, 0x81)

    # Subtitle
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(4)
    r_sub = p_sub.add_run('Phase 5: Command Centre Dashboard and Measured Twin')
    r_sub.bold = True
    r_sub.font.size = Pt(16)
    r_sub.font.name = 'Calibri'
    r_sub.font.color.rgb = RGBColor(0x32, 0x32, 0x32)

    # Metadata line
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_before = Pt(0)
    p_meta.paragraph_format.space_after = Pt(16)
    r_meta = p_meta.add_run('Intelligent Emergency Response and Hospital Network Using Dynamic Routing  |  DCCN Lab (CMP-303)  |  Week 5 to 6')
    r_meta.font.size = Pt(9.5)
    r_meta.font.name = 'Calibri'
    r_meta.font.color.rgb = RGBColor(0x64, 0x64, 0x64)

    def add_h1(text):
        h = doc.add_heading(text, level=1)
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(6)
        for r in h.runs:
            r.font.name = 'Calibri'
            r.font.color.rgb = RGBColor(0x0F, 0x4C, 0x81)
            r.font.bold = True
        return h

    def add_p(text, bold_prefix='', space_after=6):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.bold = True
            rb.font.name = 'Calibri'
            rb.font.size = Pt(10)
            rb.font.color.rgb = RGBColor(0x11, 0x11, 0x11)
        r = p.add_run(text)
        r.font.name = 'Calibri'
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
        return p

    # Section 1
    add_h1('1. What is Phase 5?')
    add_p('Phase 5 is the network visibility, analytical visualization, and measured twin implementation stage. In earlier phases, the team completed network design (Phase 1), Packet Tracer OSPF core routing (Phase 2), network services and access security (Phase 3), and comprehensive failure/recovery experiments E1 through E7 (Phase 4). The goal of Phase 5 is to bridge network simulation with real-world visibility by providing an interactive web-based Command Centre Monitoring Dashboard (Layer C) alongside an automated network probe and measured twin capability (Layer B).')
    add_p('Phase 5 is done when: the web dashboard is operational on Flask, the complete dataset of 35 measured experiment runs from Phase 4 is integrated into an honest results store without fabricated figures, interactive SVG topology visualizations reflect real-time link/node status with dynamic OSPF rerouting, Chart.js graphs illustrate packet loss and recovery times across all scenarios, and an interactive failure simulator allows live re-enactment of link outages for project evaluation.')

    # Section 2
    add_h1('2. What you do in Phase 5')
    t_tasks = doc.add_table(rows=6, cols=2)
    style_table(t_tasks, [2.2, 4.8], ['Phase 5 Task', 'Deliverable & Implementation Objective'])
    tasks_data = [
        ('1. Construct Results Data Store', 'Populate dashboard/results.csv with all 35 recorded trials across experiments E1 to E7 directly from the Phase 4 Implementation Report.'),
        ('2. Implement Network Probe', 'Develop dashboard/probe.py providing cross-platform ICMP echo, latency tracking, TCP port auditing, and continuous outage interval measurement.'),
        ('3. Develop Backend REST API', 'Build dashboard/app.py in Python Flask with endpoints for dynamic topology states (/api/status), experiment summaries (/api/experiments), live link cutting (/api/simulate), and event logging (/api/events).'),
        ('4. Build Command Centre UI', 'Create dashboard/templates/index.html and dashboard/static/style.css with an emergency command-centre theme, live KPI ribbon, and interactive SVG topology map.'),
        ('5. Visualizations & Simulator', 'Implement Chart.js analytical charts comparing packet loss % and recovery times (OSPF vs Static), alongside an interactive failure scenario replay console.')
    ]
    for row_idx, (t_name, t_desc) in enumerate(tasks_data, start=1):
        t_tasks.rows[row_idx].cells[0].paragraphs[0].add_run(t_name).bold = True
        t_tasks.rows[row_idx].cells[1].paragraphs[0].add_run(t_desc)

    # Section 3
    add_h1('3. ResQNet System Architecture & Layer Breakdown')
    add_p('The complete ResQNet project is partitioned into three complementary layers to ensure that every evaluation claim is backed by rigorous empirical measurements:')
    t_layers = doc.add_table(rows=4, cols=3)
    style_table(t_layers, [1.4, 2.8, 2.8], ['Layer', 'What It Is', 'Tools & Technologies'])
    layers_data = [
        ('Layer A\n(Core Network)', 'Complete network simulation including VLANs, 802.1Q trunks, subinterfaces, OSPF Area 0, DHCP Relay, DNS, HTTP Emergency Portal, and Extended ACLs.', 'Cisco Packet Tracer v8.2+, 2911 Routers, 3560 Multilayer Switch, 2960 Switches.'),
        ('Layer B\n(Measured Twin)', 'Automated network measurement probe and twin capability for measuring latency, service responsiveness, and packet outage duration during convergence.', 'Python 3, probe.py (Windows ping -n / Linux ping -c), TCP sockets, Wireshark.'),
        ('Layer C\n(Command Centre)', 'Interactive web dashboard providing real-time status tiles, dynamic SVG link failover animation, Chart.js metric graphs, and experiment filtering.', 'Python Flask, HTML5, CSS3, JavaScript (ES6+), Chart.js, REST API.')
    ]
    for row_idx, (l_name, l_desc, l_tools) in enumerate(layers_data, start=1):
        t_layers.rows[row_idx].cells[0].paragraphs[0].add_run(l_name).bold = True
        t_layers.rows[row_idx].cells[1].paragraphs[0].add_run(l_desc)
        t_layers.rows[row_idx].cells[2].paragraphs[0].add_run(l_tools)

    # Section 4
    add_h1('4. The Honesty Rule & Phase 4 Experiment Dataset')
    add_p('A foundational requirement of ResQNet is academic and engineering honesty. The Flask dashboard strictly obeys the following principle:')
    add_p('\"Every single number, packet loss percentage, convergence duration, and routing path displayed on the dashboard is derived directly from the recorded Phase 4 experiment runs (E1 through E7). No metric is hardcoded, guessed, or typed by hand.\"', bold_prefix='Core Honesty Mandate: ')
    add_p('The dashboard ingests dashboard/results.csv, representing 35 measured runs across 7 distinct operational and failure scenarios:')

    t_exp = doc.add_table(rows=8, cols=6)
    style_table(t_exp, [0.6, 1.8, 1.1, 0.9, 1.2, 1.4], ['Exp', 'Scenario Name', 'Failure Applied', 'Avg Loss', 'Recovery', 'Routing Path Outcome'])
    exp_data = [
        ('E1', 'Baseline (No Failure)', 'None', '0.0%', '0.0s', 'Primary H1 > CORE > CTRL (Metric 2)'),
        ('E2', 'Cut CORE-H1 Link', 'Fa0/1 shutdown', '1.7% (1/60)', '1.0s', 'OSPF Failover: H1 > H2 > CORE > CTRL (Metric 52)'),
        ('E3', 'Cut CORE-H3 Link', 'Fa0/3 shutdown', '1.7% (1/60)', '1.0s', 'OSPF Failover: H3 > CTRL direct (Metric 51)'),
        ('E4', 'Power Off R-H2', 'R-H2 Power Off', '0.0%', '0.0s', 'Independent ring survives; only H2 down'),
        ('E5', 'Dual Link Failure', 'Fa0/1 + G0/2 cut', '83.7%', 'None', 'Topological boundary limit; H1 isolated'),
        ('E6', 'Tuned OSPF Timers', 'Fa0/1 (1s/3s timers)', '1.7% (1/60)', '0.8s', 'Accelerated convergence via hello 1s / dead 3s'),
        ('E7', 'Static Routing Baseline', 'Fa0/1 shutdown', '81.7%', 'None', 'Permanent blackhole; no dynamic healing')
    ]
    for row_idx, (eid, ename, efail, eloss, erec, epath) in enumerate(exp_data, start=1):
        t_exp.rows[row_idx].cells[0].paragraphs[0].add_run(eid).bold = True
        t_exp.rows[row_idx].cells[1].paragraphs[0].add_run(ename)
        t_exp.rows[row_idx].cells[2].paragraphs[0].add_run(efail)
        t_exp.rows[row_idx].cells[3].paragraphs[0].add_run(eloss)
        t_exp.rows[row_idx].cells[4].paragraphs[0].add_run(erec)
        t_exp.rows[row_idx].cells[5].paragraphs[0].add_run(epath)

    # Section 5
    add_h1('5. Dashboard UI Components and Visualizer')
    add_p('The web interface is styled with a modern, high-contrast command centre theme (dark slate background with emerald, cyan, amber, and red status indicators):')
    add_p('Displays real-time operational counts: 6 Monitored Devices (1 Core 3560 + 5 2911 Routers), 5/5 Primary Links UP (Cost 1), 2 Redundant Backup Links STANDBY (Cost 50), and average convergence duration (0.8s - 1.0s).', bold_prefix='1. Executive KPI Ribbon: ')
    add_p('An interactive vector map rendered via SVG. R-CORE sits at the centre (380, 240) interconnecting R-CTRL (Panaji), R-H1 (Mapusa), R-H2 (Bambolim), R-H3 (Margao), and R-AMB (Ponda). Primary links appear in green (#10b981). When cut, severed links switch to dashed red (#ef4444) while backup standby links pulse in electric blue (#3b82f6) indicating active failover.', bold_prefix='2. Dynamic Topology Visualizer: ')
    add_p('Provides one-click simulation buttons allowing examiners to trigger scenarios (E1 Baseline, E2 Cut Fa0/1, E3 Cut Fa0/3, E4 Power Down H2, E5 Dual Cut, and E7 Static Route Cut). The backend updates the network state, triggers Dijkstra recalculation, and updates the active path banner in real time.', bold_prefix='3. Interactive Failure Simulator: ')
    add_p('Dual analytical charts: (a) Packet Loss Bar Chart illustrating the 0% loss of normal baseline, minimal 1.7% loss of OSPF failovers, and catastrophic >80% loss of static blackholes; (b) Convergence Comparison Chart demonstrating default timers (1.0s) vs tuned timers (0.8s) vs static failure (unrecovered).', bold_prefix='4. Chart.js Analytical Visualizations: ')
    add_p('A searchable and filterable table displaying every individual run from results.csv with run number, ping counts, loss percentages, timestamps, and path outcomes.', bold_prefix='5. Phase 4 Experiment Run Records Table: ')
    add_p('A terminal console window logging time-stamped network state transitions, Dijkstra SPF recalculation events, and link health alerts.', bold_prefix='6. Real-Time Event Terminal: ')

    # Section 6
    add_h1('6. Backend REST API & Probe Specification')
    add_p('The Flask backend (dashboard/app.py) exposes clean, decoupled REST endpoints:')
    t_api = doc.add_table(rows=7, cols=3)
    style_table(t_api, [1.5, 1.1, 4.4], ['Endpoint Route', 'HTTP Method', 'Function & Response Payload'])
    api_data = [
        ('/', 'GET', 'Renders the primary HTML5 Command Centre Dashboard interface.'),
        ('/api/status', 'GET', 'Returns JSON containing dynamic operational states of all 6 sites, 7 links, and the currently active OSPF routing path.'),
        ('/api/experiments', 'GET', 'Returns parsed dataset of all 35 experimental trials from results.csv along with aggregated scenario summaries.'),
        ('/api/simulate', 'POST', 'Accepts JSON payload {"scenario": "E2_CUT"} to dynamically sever or restore links, recalculating Dijkstra path states and triggering alert logs.'),
        ('/api/events', 'GET', 'Returns chronological list of recent routing events, neighbor state transitions, and topology alerts.'),
        ('/api/probe', 'POST', 'Accepts {"ip": "<target>"} and executes a live measurement via probe.py, returning round-trip latency and success state.')
    ]
    for row_idx, (a_route, a_method, a_desc) in enumerate(api_data, start=1):
        t_api.rows[row_idx].cells[0].paragraphs[0].add_run(a_route).bold = True
        t_api.rows[row_idx].cells[1].paragraphs[0].add_run(a_method)
        t_api.rows[row_idx].cells[2].paragraphs[0].add_run(a_desc)

    # Section 7
    add_h1('7. Verification and Test Results')
    add_p('The complete Phase 5 subsystem underwent automated verification using Python test suites:')
    add_p('The Flask server was validated using Werkzeug test client. Endpoints /, /api/experiments, /api/simulate, and /api/events responded with HTTP 200 OK. Dynamic failover paths and scenario resets executed cleanly with zero exceptions.', bold_prefix='1. REST API Integration Test: ')
    add_p('All 35 records from results.csv were verified against the Phase 4 Implementation Report. Aggregated means matched empirical data exactly: E1 (0.0% loss), E2 (1.7% loss, 1.0s recovery), E3 (1.7% loss, 1.0s recovery), E6 (1.7% loss, 0.8s recovery), and E7 (81.7% loss, no failover).', bold_prefix='2. Experiment Data Parser Verification: ')
    add_p('probe.py was tested with Windows ping commands (-n 1 -w 1000) and socket connections, demonstrating robust error handling even in isolated network sandbox environments.', bold_prefix='3. Network Probe Resilience: ')

    # Section 8
    add_h1('8. Demonstration and Viva Presentation Guide (3-Minute Script)')
    add_p('During the laboratory evaluation or project viva, present Phase 5 using the following sequence:')
    add_p('Launch the dashboard (python app.py) and open http://127.0.0.1:5000 in Chrome/Edge. Explain the hub-and-spoke architecture with R-CORE (3560) joining the 5 edge routers. Point out the KPI ribbon showing all 5 primary links healthy.', bold_prefix='Step 1 (0:00 - 0:45) - Architecture & Baseline: ')
    add_p('Click "Cut CORE-H1 Link (E2)". Direct the examiner\'s attention to the SVG map: link Fa0/1 turns dashed red, backup link H1-H2 pulses in blue, and the active path updates from metric 2 to metric 52 (H1 > H2 > CORE > CTRL). Explain that OSPF detected the loss and rerouted traffic automatically.', bold_prefix='Step 2 (0:45 - 1:45) - Dynamic OSPF Convergence: ')
    add_p('Scroll to Chart.js visualizations. Point out the convergence comparison: default OSPF recovers in 1.0s, tuned timers (1s/3s) recover in 0.8s, whereas static routing (E7) drops packets permanently. Highlight the 35-run results table to prove that all metrics come from recorded trials.', bold_prefix='Step 3 (1:45 - 2:30) - Empirical Proof & Honesty Rule: ')
    add_p('Click "Dual Link Cut (E5)" to demonstrate the topological limit where Hospital 1 becomes isolated, proving the team understands both the capabilities and the boundaries of the network design.', bold_prefix='Step 4 (2:30 - 3:00) - Design Boundaries & Limitations: ')

    # Ensure parent dir exists
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    doc.save(output_path)
    print(f'Document successfully created at: {output_path}')


if __name__ == '__main__':
    build_phase5_doc('DCCN-Project-ResQNet-/docs/ResQNet_Phase5.docx')
    build_phase5_doc('ResQNet_Phase5.docx')
