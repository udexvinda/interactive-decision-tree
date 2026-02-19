import json
from datetime import datetime
import streamlit as st

st.set_page_config(page_title="Enterprise Direction Diagnostic (Decision Tree)", layout="wide")

# -----------------------------
# Decision tree definition
# -----------------------------
TREE = {
    "Operational Excellence": {
        "question_lvl1": "Q2A: What is the primary driver?",
        "options_lvl1": {
            "Cost / Efficiency": {
                "outcome_lvl2": "Margin-protection / cost-to-serve reduction focus.",
                "question_lvl2": "Q3A1: Where is cost leaking most?",
                "options_lvl2": [
                    "Labor effort (manual work / overtime)",
                    "Rework / repeat handling",
                    "Hand-offs & delays",
                    "Vendor / procurement cost",
                    "Technology / licensing / legacy cost",
                ],
                "question_lvl3": "Q4A1: What is the biggest root pattern?",
                "options_lvl3": [
                    "No standard work / unclear SOPs",
                    "Work intake unmanaged (too much WIP)",
                    "Poor demand forecasting / staffing model",
                    "Process variation across teams/sites",
                    "Systems fragmentation (multiple tools, re-keying)",
                ],
                "metrics": [
                    "Cost-to-serve trend (12–18 months)",
                    "Unit cost per transaction (before/after)",
                    "% value-add time vs waiting time",
                    "Overtime hours, backlog age",
                    "Savings realized vs 'paper savings'",
                ],
            },
            "Quality / Defects": {
                "outcome_lvl2": "Defect reduction and right-first-time stability focus.",
                "question_lvl2": "Q3A2: What type of quality failure dominates?",
                "options_lvl2": [
                    "Data accuracy errors",
                    "Compliance/validation errors",
                    "Customer-impacting defects",
                    "Rework loops (case reopened)",
                    "Supplier/3rd party defects",
                ],
                "question_lvl3": "Q4A2: Where is the defect source most likely?",
                "options_lvl3": [
                    "Inputs (bad data / incomplete request)",
                    "Methods (no control plan / no checks)",
                    "People (skills / training gaps)",
                    "Systems (rule gaps / automation logic)",
                    "Environment (handoffs / queueing / pressure)",
                ],
                "metrics": [
                    "First-pass yield / right-first-time %",
                    "Defect rate per 1,000 transactions",
                    "Rework hours and cost of poor quality",
                    "Audit findings trend",
                    "% recurring defects (Pareto repeat)",
                ],
            },
            "SLA / Customer Experience": {
                "outcome_lvl2": "Reliability, responsiveness and customer trust focus.",
                "question_lvl2": "Q3A3: What is breaking SLA performance?",
                "options_lvl2": [
                    "Peaks/seasonality demand",
                    "Bottleneck steps",
                    "Long approvals",
                    "Rework loops",
                    "External dependencies",
                ],
                "question_lvl3": "Q4A3: Which control mechanism is missing?",
                "options_lvl3": [
                    "Clear SLA definitions & segmentation",
                    "Real-time visibility (dashboards)",
                    "Queue/WIP limits and prioritization rules",
                    "Escalation rules & triage",
                    "Ownership and daily management rhythm",
                ],
                "metrics": [
                    "SLA attainment % by segment",
                    "Aging distribution (p50/p90/p99)",
                    "Customer satisfaction (CSAT/NPS) trend",
                    "Backlog size and burn-down",
                    "# escalations / complaints per month",
                ],
            },
            "Regulatory / Risk": {
                "outcome_lvl2": "Assurance, audit readiness and risk containment focus.",
                "question_lvl2": "Q3A4: What risk class is most critical?",
                "options_lvl2": [
                    "Regulatory compliance breaches",
                    "Financial / reporting risk",
                    "Operational risk (process failures)",
                    "Data privacy & security",
                    "Third-party / vendor risk",
                ],
                "question_lvl3": "Q4A4: Where is the control weakness?",
                "options_lvl3": [
                    "Control design missing / outdated",
                    "Control execution inconsistent",
                    "Evidence not captured",
                    "Roles unclear (RACI gaps)",
                    "Monitoring not proactive (only after incident)",
                ],
                "metrics": [
                    "Audit issues count & severity trend",
                    "Control effectiveness rate",
                    "Time to close audit findings",
                    "Incident frequency & loss impact",
                    "% processes with documented controls + evidence",
                ],
            },
            "Productivity / Capacity Scaling": {
                "outcome_lvl2": "Handle higher volumes without proportional headcount.",
                "question_lvl2": "Q3A5: What is limiting throughput?",
                "options_lvl2": [
                    "Too much manual handling",
                    "Skills capacity / specialization constraints",
                    "Bottleneck roles / approvals",
                    "Tool limitations / system latency",
                    "Poor demand management / intake quality",
                ],
                "question_lvl3": "Q4A5: What scaling lever is most feasible?",
                "options_lvl3": [
                    "Standard work + training academy",
                    "Automation (RPA/workflow)",
                    "Self-service / better inputs",
                    "Role redesign / cross-skilling",
                    "Load balancing across teams/sites",
                ],
                "metrics": [
                    "Output per FTE trend",
                    "Volume vs headcount ratio",
                    "Cycle time trend under peak loads",
                    "Utilization vs burnout indicators",
                    "Automation coverage (% steps automated)",
                ],
            },
        },
    },
    "Innovation": {
        "question_lvl1": "Q2B: Which innovation type is dominant?",
        "options_lvl1": {
            "Product / Service": {
                "outcome_lvl2": "Differentiation through new offerings.",
                "question_lvl2": "Q3B1: Where is the innovation bottleneck?",
                "options_lvl2": [
                    "Weak customer insight / VOC",
                    "Too many ideas, no selection",
                    "Slow prototyping",
                    "Poor handoff to delivery/ops",
                    "Weak go-to-market",
                ],
                "question_lvl3": "Q4B1: Which engine is missing?",
                "options_lvl3": [
                    "Innovation funnel + stage gates",
                    "Rapid experimentation (MVP discipline)",
                    "Portfolio prioritization (value vs effort)",
                    "Cross-functional squads",
                    "Commercialization playbook",
                ],
                "metrics": [
                    "Time-to-market",
                    "% revenue from new offerings (12–24 months)",
                    "Win/loss rate of launches",
                    "Adoption and retention",
                    "Pipeline value vs conversion rate",
                ],
            },
            "Digital Experience": {
                "outcome_lvl2": "Better customer/employee experience via digital.",
                "question_lvl2": "Q3B2: What’s the dominant barrier?",
                "options_lvl2": [
                    "Legacy platforms",
                    "Fragmented journeys",
                    "Poor UX ownership",
                    "Data fragmentation",
                    "Adoption resistance",
                ],
                "question_lvl3": "Q4B2: Where will impact be highest?",
                "options_lvl3": [
                    "End-to-end journey redesign",
                    "Omnichannel integration",
                    "Digital self-service",
                    "Personalization",
                    "Digital governance & product ownership",
                ],
                "metrics": [
                    "Digital adoption rate",
                    "Drop-off / abandonment rate",
                    "Journey time reduction",
                    "Self-service containment %",
                    "CSAT/NPS change by journey",
                ],
            },
            "AI / Data Innovation": {
                "outcome_lvl2": "Competing with intelligence (prediction, automation, decision support).",
                "question_lvl2": "Q3B3: What’s the biggest constraint?",
                "options_lvl2": [
                    "Data quality / availability",
                    "Governance & privacy",
                    "Skills (ML/AI/product)",
                    "Use-case prioritization",
                    "MLOps / deployment capability",
                ],
                "question_lvl3": "Q4B3: What is the AI operating model today?",
                "options_lvl3": [
                    "Experiments only (PoCs)",
                    "Pilots in isolated teams",
                    "Embedded into workflows",
                    "Scaled platform capability",
                    "AI governance + measurable value engine",
                ],
                "metrics": [
                    "# AI use cases scaled (not just PoC)",
                    "Model performance + drift control",
                    "Time from idea → deployment",
                    "Savings/revenue attributable to AI",
                    "Adoption of AI features in daily work",
                ],
            },
            "Business Model": {
                "outcome_lvl2": "Changing how you create/capture value (pricing, subscriptions, ecosystem).",
                "question_lvl2": "Q3B4: What is forcing the model change?",
                "options_lvl2": [
                    "Margin compression",
                    "New entrant disruption",
                    "Channel disintermediation",
                    "Customer preference shifts",
                    "Regulation/market structure",
                ],
                "question_lvl3": "Q4B4: Which model shift are you exploring?",
                "options_lvl3": [
                    "Subscription / recurring revenue",
                    "Outcome-based pricing",
                    "Platform/ecosystem partnerships",
                    "Bundling/unbundling",
                    "New cost structure (variable vs fixed)",
                ],
                "metrics": [
                    "Gross margin improvement",
                    "Recurring revenue %",
                    "CAC/LTV metrics",
                    "Churn and expansion revenue",
                    "Partner contribution to revenue",
                ],
            },
            "Market / Channel Expansion": {
                "outcome_lvl2": "Growth through new geographies, segments, channels.",
                "question_lvl2": "Q3B5: Where is friction?",
                "options_lvl2": [
                    "Weak segment targeting",
                    "Sales enablement gaps",
                    "Operational capability not ready",
                    "Partner/channel strategy unclear",
                    "Brand trust barrier",
                ],
                "question_lvl3": "Q4B5: What capability is missing to scale expansion?",
                "options_lvl3": [
                    "Segment strategy & ICP definition",
                    "Channel operating model (direct/partner)",
                    "Fulfillment readiness",
                    "Local compliance readiness",
                    "Marketing/sales performance engine",
                ],
                "metrics": [
                    "Market share change",
                    "Revenue growth by segment",
                    "Channel conversion rates",
                    "Fulfillment SLA in new markets",
                    "Expansion cost vs plan",
                ],
            },
        },
    },
    "Hybrid": {
        "question_lvl1": "Q2C: Which pattern best describes you?",
        "options_lvl1": {
            "Stabilize core first, then innovate": {
                "outcome_lvl2": "Foundation and trust-building first.",
                "question_lvl2": "Q3C1: What must be stabilized?",
                "options_lvl2": [
                    "Process standardization",
                    "KPI governance & visibility",
                    "Control effectiveness",
                    "Capability baseline (training)",
                    "Tech reliability / tooling",
                ],
                "question_lvl3": "Q4C1: What is the best stabilization lever?",
                "options_lvl3": [
                    "Standard work + daily management",
                    "Controls & audit readiness program",
                    "Process ownership model",
                    "Skills academy + certifications",
                    "System simplification / workflow",
                ],
                "metrics": [
                    "Stability indicators (variance reduction)",
                    "SLA reliability (p90 aging)",
                    "Audit/control metrics trend",
                    "Process compliance rate",
                    "# stabilized processes ready for innovation",
                ],
            },
            "Innovate while fixing": {
                "outcome_lvl2": "High-velocity change with KPI/conflict risk.",
                "question_lvl2": "Q3C2: Where is conflict appearing?",
                "options_lvl2": [
                    "Cost vs growth priorities",
                    "Compliance vs experimentation",
                    "Talent allocation conflict",
                    "Tooling/platform conflict",
                    "Governance confusion",
                ],
                "question_lvl3": "Q4C2: Which guardrail model fits you?",
                "options_lvl3": [
                    "Innovation sandbox with controls",
                    "Dual KPI scoreboard (exploit/explore)",
                    "Portfolio governance (capacity allocation)",
                    "Dual operating system (core vs venture)",
                    "Clear escalation and decision rights",
                ],
                "metrics": [
                    "Capacity split (core vs innovation)",
                    "Innovation throughput (# experiments/month)",
                    "Core performance not degrading (SLA/cost)",
                    "Engagement/burnout trends",
                    "Risk incidents during experimentation",
                ],
            },
            "Separate units (ambidextrous by design)": {
                "outcome_lvl2": "Structural ambidexterity with different operating rules.",
                "question_lvl2": "Q3C3: How is separation implemented?",
                "options_lvl2": [
                    "Separate teams under same leadership",
                    "Separate P&L/business units",
                    "Innovation lab / venture studio",
                    "Platform team supporting both",
                    "Outsourced innovation partners",
                ],
                "question_lvl3": "Q4C3: What integration mechanism is missing?",
                "options_lvl3": [
                    "Shared architecture principles",
                    "Transition path (pilot → core ops)",
                    "Governance on prioritization",
                    "Talent rotation model",
                    "Shared data platform",
                ],
                "metrics": [
                    "% pilots successfully transitioned to ops",
                    "Time to industrialize innovation",
                    "Duplicate work reduction",
                    "Decision speed (governance cycle time)",
                    "Combined scorecard health (margin + growth)",
                ],
            },
        },
    },
}

FINAL_OUTCOMES = [
    "Financial (EBITDA, margin, cost-to-serve)",
    "Customer (NPS/CSAT, complaints)",
    "Process (cycle time, defects, SLA)",
    "Risk (audit findings, incidents)",
    "Capability (skills index, adoption, engagement)",
]

# -----------------------------
# Helpers
# -----------------------------
def reset():
    for k in list(st.session_state.keys()):
        if k.startswith("sel_") or k.startswith("txt_") or k.startswith("chk_"):
            del st.session_state[k]

def now_iso():
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


# -----------------------------
# UI
# -----------------------------
st.title("Enterprise Strategic Direction — Interactive Decision Tree")
st.caption("Deep branching diagnostic (Direction → Driver/Type → Constraint/Pattern → Metrics → Outcomes).")

with st.sidebar:
    st.header("Controls")
    if st.button("Reset all selections"):
        reset()
        st.rerun()

col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("Q1. On which direction is the company moving?")
    direction = st.radio(
        "Select one",
        ["Operational Excellence", "Innovation", "Hybrid"],
        key="sel_direction",
        horizontal=True,
    )

    node = TREE[direction]

    st.divider()
    st.subheader(node["question_lvl1"])
    lvl1_choice = st.selectbox(
        "Choose the best fit",
        list(node["options_lvl1"].keys()),
        key="sel_lvl1",
    )

    leaf = node["options_lvl1"][lvl1_choice]

    st.info(f"**Outcome:** {leaf['outcome_lvl2']}")

    st.divider()
    st.subheader(leaf["question_lvl2"])
    lvl2_choice = st.selectbox(
        "Select one",
        leaf["options_lvl2"],
        key="sel_lvl2",
    )

    st.divider()
    st.subheader(leaf["question_lvl3"])
    lvl3_choice = st.selectbox(
        "Select one",
        leaf["options_lvl3"],
        key="sel_lvl3",
    )

with col2:
    st.subheader("How did you do? (Evidence & metrics)")
    st.write("Pick the metrics you already track and add notes if needed.")
    metric_checks = {}
    for m in leaf["metrics"]:
        metric_checks[m] = st.checkbox(m, key=f"chk_{m}")

    st.text_area(
        "Notes / evidence (optional)",
        placeholder="e.g., last 12-month trend, current baseline, target, data source, owner…",
        key="txt_notes",
        height=140,
    )

    st.divider()
    st.subheader("Final outcomes (12–18 months)")
    outcomes = st.multiselect(
        "Pick top 3 outcomes that must improve",
        FINAL_OUTCOMES,
        default=[],
        key="sel_outcomes",
        max_selections=3,
    )

    st.text_input(
        "Success statement (one line)",
        placeholder="e.g., Reduce cost-to-serve by 12% while sustaining SLA ≥ 95%.",
        key="txt_success",
    )

# -----------------------------
# Summary + Export
# -----------------------------
st.divider()
st.header("Diagnostic summary")

selected_metrics = [m for m, v in metric_checks.items() if v]

summary = {
    "timestamp_utc": now_iso(),
    "direction": direction,
    "level_1_choice": lvl1_choice,
    "level_2_choice": lvl2_choice,
    "level_3_choice": lvl3_choice,
    "recommended_metrics": leaf["metrics"],
    "selected_metrics_tracked": selected_metrics,
    "notes": st.session_state.get("txt_notes", ""),
    "target_outcomes_12_18_months": st.session_state.get("sel_outcomes", []),
    "success_statement": st.session_state.get("txt_success", ""),
}

left, right = st.columns([1.2, 1])

with left:
    st.markdown("### What we learned")
    st.write(f"**Direction:** {summary['direction']}")
    st.write(f"**Driver/Type:** {summary['level_1_choice']}")
    st.write(f"**Primary pain/constraint:** {summary['level_2_choice']}")
    st.write(f"**Likely root pattern / lever:** {summary['level_3_choice']}")
    if summary["target_outcomes_12_18_months"]:
        st.write("**12–18 month outcomes:** " + "; ".join(summary["target_outcomes_12_18_months"]))
    if summary["success_statement"]:
        st.success(summary["success_statement"])

    if selected_metrics:
        st.write("**Metrics currently tracked:**")
        st.write("- " + "\n- ".join(selected_metrics))
    else:
        st.warning("No metrics selected yet. Consider choosing at least 2–3 metrics for evidence.")

with right:
    st.markdown("### Export")
    st.download_button(
        "Download summary as JSON",
        data=json.dumps(summary, indent=2),
        file_name="enterprise_direction_diagnostic_summary.json",
        mime="application/json",
        use_container_width=True,
    )
    st.code(json.dumps(summary, indent=2), language="json")

st.caption("Tip: This app is a discovery tool. The next step is converting the summary into a roadmap, maturity score, and project portfolio.")
