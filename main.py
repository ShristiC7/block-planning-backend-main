"""
FastAPI Backend Server
AI-Powered Automatic Block Planning System - Indian Railways (SIH Project)

Endpoints:
1. GET /defects          -> prioritized task list
2. GET /block-plan        -> optimized block schedule (?horizon=weekly|monthly)
3. GET /summary           -> KPIs, weekly and monthly before/after comparison
4. GET /corridor          -> corridor + sections info
5. GET /goods-forecast     -> goods train forecast (Control Office data)
6. GET /block-requests     -> auto-generated official block request documents

Run with:
uvicorn main:app --reload
"""

import os
from collections import defaultdict
from typing import Optional
from dotenv import load_dotenv
from supabase import create_client, Client
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="AI Block Planning API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "AI Block Planning API is running."}


@app.get("/defects")
def get_defects():
    """
    All defects, sorted by priority_score (most urgent first).
    Used by the dashboard's task inbox section.
    """
    response = supabase.table("defects").select("*").order("priority_score", desc=True).execute()
    return {"count": len(response.data), "defects": response.data}


@app.get("/block-plan")
def get_block_plan(horizon: Optional[str] = None):
    """
    The AI-optimized combined block schedule.
    Filter with ?horizon=weekly or ?horizon=monthly.
    Used by the dashboard's Gantt calendar view.
    """
    query = supabase.table("block_plan_output").select("*").order("planned_date")
    if horizon:
        query = query.eq("plan_horizon", horizon)
    response = query.execute()
    return {"count": len(response.data), "block_plan": response.data}


@app.get("/goods-forecast")
def get_goods_forecast():
    """
    Goods train forecast data, as would be provided by the Control Office.
    Used to show traffic-aware planning in the dashboard.
    """
    response = supabase.table("goods_train_forecast").select("*").order("date").execute()
    return {"count": len(response.data), "goods_forecast": response.data}


@app.get("/corridor")
def get_corridor():
    """
    Basic corridor and section information.
    """
    corridor = supabase.table("corridor").select("*").execute()
    sections = supabase.table("sections").select("*").execute()
    return {"corridor": corridor.data, "sections": sections.data}


def _urgency_label(defect_list):
    if any(d["safety_signal"] for d in defect_list):
        return "URGENT (Safety-critical)"
    max_severity = max((d["severity"] or 0) for d in defect_list)
    if max_severity >= 7:
        return "HIGH"
    elif max_severity >= 4:
        return "MEDIUM"
    return "LOW"


@app.get("/block-requests")
def get_block_requests():
    """
    Auto-generated, ready-to-submit official block request documents.

    For every planned block, this builds the same justification an officer
    would otherwise write manually for BDMS submission - department(s)
    involved, defects covered, priority level, and hours saved through
    joint scheduling versus requesting each department's task separately.

    Hours-saved logic:
    In the siloed (current/manual) process, each department that has work
    on this section would request its OWN full block window separately.
    So the "before" cost is (number of departments involved) x (this
    block's duration) - not the sum of individual task durations, since
    a department cannot get less than one full block for its work.
    The "after" cost is just this single joint block's duration, since
    all departments share it.
    """
    plan_resp = supabase.table("block_plan_output").select("*").order("planned_date").execute()
    block_plans = plan_resp.data

    defects_resp = supabase.table("defects").select("*").execute()
    defects_by_id = {d["defect_id"]: d for d in defects_resp.data}

    requests = []

    for block in block_plans:
        defect_ids = [x.strip() for x in block["defect_ids"].split(",")] if block.get("defect_ids") else []
        defect_list = [defects_by_id[did] for did in defect_ids if did in defects_by_id]

        if not defect_list:
            continue

        joint_hours = block["duration_hours"]
        num_departments = len(set(d["department"] for d in defect_list))

        # Siloed baseline: each department involved would need its own
        # full block of the same duration if requesting separately.
        siloed_estimate_hours = num_departments * joint_hours
        hours_saved = max(siloed_estimate_hours - joint_hours, 0)

        requests.append({
            "section_id": block["section_id"],
            "planned_date": block["planned_date"],
            "start_time": block["start_time"],
            "duration_hours": joint_hours,
            "departments_included": block["departments_included"],
            "plan_horizon": block["plan_horizon"],
            "priority_level": _urgency_label(defect_list),
            "justification": [
                {
                    "defect_id": d["defect_id"],
                    "department": d["department"],
                    "defect_type": d["defect_type"],
                    "severity": d["severity"],
                    "days_overdue": d["days_overdue"],
                    "safety_critical": d["safety_signal"],
                }
                for d in defect_list
            ],
            "estimated_separate_hours": siloed_estimate_hours,
            "hours_saved": hours_saved,
            "status": "Pending Section Controller Approval",
        })

    return {"count": len(requests), "block_requests": requests}


def _horizon_stats(plan_rows, horizon_name):
    rows = [r for r in plan_rows if r.get("plan_horizon") == horizon_name]
    blocks_after = len(rows)
    tasks_scheduled = sum(
        len(r["defect_ids"].split(", ")) for r in rows if r.get("defect_ids")
    )
    blocks_before = tasks_scheduled

    reduction_pct = 0
    if blocks_before > 0:
        reduction_pct = round((1 - blocks_after / blocks_before) * 100, 1)

    joint_blocks = len([
        r for r in rows
        if r.get("departments_included") and len(r["departments_included"].split(", ")) > 1
    ])

    return {
        "blocks_before_siloed": blocks_before,
        "blocks_after_joint": blocks_after,
        "reduction_pct": reduction_pct,
        "joint_multi_department_blocks": joint_blocks,
    }


@app.get("/summary")
def get_summary():
    """
    KPI data for the dashboard - weekly and monthly before/after
    comparison, department breakdown, and safety-critical count.
    """
    defects_resp = supabase.table("defects").select("*").execute()
    defects = defects_resp.data

    plan_resp = supabase.table("block_plan_output").select("*").execute()
    plan_rows = plan_resp.data

    dept_counts = defaultdict(int)
    for d in defects:
        dept_counts[d["department"]] += 1

    safety_critical_count = len([d for d in defects if d["safety_signal"]])

    return {
        "total_defects": len(defects),
        "department_breakdown": dict(dept_counts),
        "safety_critical_count": safety_critical_count,
        "weekly": _horizon_stats(plan_rows, "weekly"),
        "monthly": _horizon_stats(plan_rows, "monthly"),
    }