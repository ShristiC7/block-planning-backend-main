# Project Deployment Matrix: All APIs & URLs Reference
## AI-Powered Automatic Block Planning System (SIH 2026 | PS 26027)

---

## 1. Production Backend Service Details
* **Base URL:** `https://railblock-api.onrender.com`
* **Swagger / OpenAPI Interactive Docs:** `https://railblock-api.onrender.com/docs`
* **ReDoc Interactive Reference:** `https://railblock-api.onrender.com/redoc`
* **OpenAPI JSON Schema:** `https://railblock-api.onrender.com/openapi.json`

---

## 2. Comprehensive API Endpoints Inventory

| Method | Endpoint Path | Function & Data Returned | Integration in Frontend |
|---|---|---|---|
| `GET` | `/` | **Health check** returning API operational status string | Live connectivity check on dashboard load |
| `GET` | `/summary` | **High-Level KPIs & Impact Summary**:<br>• Total defect counts<br>• Breakdown by Dept (`TMS`, `SMMS`, `TDMS`)<br>• Safety-critical defect tally<br>• Weekly & monthly before/after block reduction percentages & multi-dept counts | [`operations_analytics.html`](file:///c:/Users/shris/Downloads/block-planning-backend-main%20(1)/block-planning-backend-main/frontend/operations_analytics.html) & Top Header telemetry badges |
| `GET` | `/defects` | **Prioritized Defect Backlog**:<br>• All maintenance records sorted in descending order by `priority_score`<br>• Asset IDs, start/end KMs, severity, days overdue, and safety signal flags | [`command_center_network_map_2.html`](file:///c:/Users/shris/Downloads/block-planning-backend-main%20(1)/block-planning-backend-main/frontend/command_center_network_map_2.html) & [`ai_planner_optimizer.html`](file:///c:/Users/shris/Downloads/block-planning-backend-main%20(1)/block-planning-backend-main/frontend/ai_planner_optimizer.html) |
| `GET` | `/block-plan` | **AI-Optimized Schedule Output**:<br>• Filterable by query parameter `?horizon=weekly` or `?horizon=monthly`<br>• Start times, duration hours, departments included, and bundled defect IDs | Timeline Gantt in [`index.html`](file:///c:/Users/shris/Downloads/block-planning-backend-main%20(1)/block-planning-backend-main/frontend/index.html) & Optimizer Workspace |
| `GET` | `/block-requests` | **Auto-Generated BDMS Block Approval Documents**:<br>• Formal block justification for Section Controllers<br>• Estimated separate hours vs joint hours saved<br>• Safety critical justification tags | Modal inspection & Human Approval lifecycle |
| `GET` | `/corridor` | **Corridor & Section Infrastructure Model**:<br>• Corridor names, station boundaries (`from_station`, `to_station`), start/end KMs, and traffic density | Network Hierarchy & Leaflet GIS Map in [`command_center_network_map_1.html`](file:///c:/Users/shris/Downloads/block-planning-backend-main%20(1)/block-planning-backend-main/frontend/command_center_network_map_1.html) |
| `GET` | `/goods-forecast` | **Goods Train Forecasts (Control Office Data)**:<br>• Forecasted freight paths, section arrival/departure, and operational slots | Traffic-aware constraint validation in [`railway_engine.js`](file:///c:/Users/shris/Downloads/block-planning-backend-main%20(1)/block-planning-backend-main/frontend/railway_engine.js) |

---

## 3. Frontend Pages & Screen URLs

When deployed to Render (or served locally), the application exposes the following views:

| Page / Screen | File Path | Purpose & Key Features |
|---|---|---|
| **System Access Portal** | `login.html` | Secure employee authentication (`EMP-9021` / `admin`). |
| **Command Center Dashboard** | `index.html` | Main operations overview, corridor status, Gantt timeline, live telemetry stream. |
| **GIS Network Map** | `command_center_network_map_1.html` | Real-time Leaflet GIS railway track view with live moving trains and active maintenance block pulses. |
| **Multi-Dept Task Explorer** | `command_center_network_map_2.html` | Interactive task map, asset inspection, PRD priority score breakdowns, and department filters. |
| **AI Planner & Optimizer** | `ai_planner_optimizer.html` | CP-SAT constraint optimization workspace, multi-department bundle discovery (`B-104`, `B-105`), XAI "WHY?" reasoning, What-If simulator. |
| **Data Ingestion & DB Hub** | `data_upload_center.html` | Multi-department CSV upload (TMS/SMMS/TDMS), manual task entry, JSON database backup/restore, One-Click Render API Cloud Sync. |
| **Operations Analytics Suite** | `operations_analytics.html` | PRD Section 19 KPI comparative analysis, before vs after delay reduction curves, department allocation metrics. |
| **Asset Digital Twin** | `asset_digital_twin_explorer.html` | 3D structural asset explorer (bridges, track, catenary), sensor telemetry modes, dynamic defect injection. |

---

## 4. Third-Party CDNs & External Resources Required

Ensure the production hosting environment allows outbound connections to:
* **Leaflet GIS Map Tiles & Assets:**
  * CSS: `https://unpkg.com/leaflet@1.9.4/dist/leaflet.css`
  * JS: `https://unpkg.com/leaflet@1.9.4/dist/leaflet.js`
  * CartoDB Basemap: `https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png`
* **Styling & Fonts:**
  * Tailwind CDN: `https://cdn.tailwindcss.com`
  * Google Fonts: `https://fonts.googleapis.com` (`Inter`, `Noto Sans`, `JetBrains Mono`, `Source Code Pro`)
  * Google Material Symbols: `https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined`
* **Cloud Database:**
  * Supabase: `https://*.supabase.co`
