from __future__ import annotations

from pathlib import Path
from typing import List
import math
import re

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Flower DevEx Agent Studio")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class AnalyzeRequest(BaseModel):
    team_name: str
    workflow: str
    challenge: str
    constraints: str = ""
    objective: str = ""


def tokenize(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z0-9_\-]+", text.lower())


def score_text(text: str) -> int:
    words = tokenize(text)
    unique = len(set(words))
    total = len(words)
    bonus = 0
    keywords = {
        "github": 8,
        "ci": 8,
        "cd": 8,
        "actions": 7,
        "cursor": 7,
        "claude": 7,
        "agent": 9,
        "review": 6,
        "test": 7,
        "deployment": 6,
        "quality": 7,
        "context": 6,
        "docs": 4,
        "energy": 6,
        "python": 5,
    }
    for word in words:
        bonus += keywords.get(word, 0)
    base = min(50, total * 2 + unique)
    return min(100, 25 + base + bonus)


def pick_workflow_type(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["pull request", "pr", "review"]):
        return "Pull Request Copilot"
    if any(k in t for k in ["test", "qa", "verification"]):
        return "Quality Gate Agent"
    if any(k in t for k in ["docs", "documentation", "readme"]):
        return "Documentation Assistant"
    if any(k in t for k in ["deploy", "release", "ci", "cd"]):
        return "Release Reliability Agent"
    return "Developer Workflow Agent"


def build_context_cards(req: AnalyzeRequest) -> List[dict]:
    workflow_type = pick_workflow_type(req.workflow + " " + req.challenge)
    return [
        {
            "title": "Discovery Agent",
            "icon": "◆",
            "summary": f"Reframes the request for the {req.team_name or 'platform'} team and identifies where an AI agent can reduce repetitive engineering work in a {workflow_type} flow.",
            "signals": [
                "Clarifies expected inputs, outputs, and handoff boundaries",
                "Identifies where context must be attached before an agent acts",
                "Flags where deterministic automation may outperform an agent",
            ],
        },
        {
            "title": "Trust Agent",
            "icon": "◈",
            "summary": "Designs guardrails for correctness, code quality, and verifiability before agent-generated changes can be accepted.",
            "signals": [
                "Requires tests, linting, and explicit success criteria",
                "Checks whether the agent has enough repo context and tooling access",
                "Surfaces hallucination, drift, and partial-context risks",
            ],
        },
        {
            "title": "Workflow Agent",
            "icon": "⬢",
            "summary": "Maps a workflow that connects editor tooling, repository context, and CI signals into one developer loop.",
            "signals": [
                "Suggests where Cursor, Claude Code, or an SDK-style agent fits best",
                "Defines when the agent can propose changes versus commit-ready patches",
                "Aligns agent steps with GitHub checks and branch workflows",
            ],
        },
        {
            "title": "Impact Agent",
            "icon": "✦",
            "summary": "Estimates productivity gains and recommends what to measure before broad rollout across engineering teams.",
            "signals": [
                "Tracks cycle time, review burden, and revert rate",
                "Measures acceptance rate of agent-generated suggestions",
                "Prioritizes the narrowest workflow that can show value fast",
            ],
        },
    ]


def build_metrics(req: AnalyzeRequest) -> dict:
    text = " ".join([req.workflow, req.challenge, req.constraints, req.objective])
    score = score_text(text)
    trust = max(58, min(94, math.floor(score * 0.86)))
    fit = max(55, min(96, math.floor(score * 0.91)))
    rollout = max(42, min(90, math.floor((fit + trust) / 2) - 8))
    return {
        "ai_fit": fit,
        "trust_readiness": trust,
        "rollout_readiness": rollout,
        "estimated_time_saved": f"{max(12, fit // 4)}%",
        "suggested_pilot": "1 workflow / 2 weeks / 3 contributors",
    }


def build_recommendation(req: AnalyzeRequest, metrics: dict) -> str:
    workflow_type = pick_workflow_type(req.workflow + " " + req.challenge)
    base = (
        f"Start with a narrow {workflow_type} pilot for the {req.team_name or 'engineering'} team. "
        f"The strongest use of an agent here is assisting with context-heavy but reviewable tasks, while keeping final approval with developers. "
        f"Given the described challenge, the agent should operate inside a guarded workflow with repo context, explicit success criteria, and automated checks before any output is trusted."
    )
    if metrics["ai_fit"] > 82:
        base += " The use case is a strong candidate for AI assistance because the work appears repetitive, context-driven, and measurable."
    else:
        base += " A hybrid setup is more appropriate than full agent autonomy, because parts of the task likely benefit from deterministic rules or human validation."
    return base


def build_quality_harness(req: AnalyzeRequest) -> List[dict]:
    return [
        {
            "name": "Context Package",
            "status": "Ready",
            "detail": "Repository files, coding guidelines, task intent, and expected output format are bundled before an agent acts.",
        },
        {
            "name": "Verification Layer",
            "status": "Ready",
            "detail": "Linting, tests, and acceptance checks validate whether an agent contribution is correct and safe to review.",
        },
        {
            "name": "Escalation Path",
            "status": "Ready",
            "detail": "Ambiguous tasks, confidence drops, or failed checks are escalated back to the developer instead of silently proceeding.",
        },
        {
            "name": "Observability",
            "status": "Pilot",
            "detail": "Measure acceptance rate, review time, rollback frequency, and time-to-merge for agent-generated work.",
        },
    ]


def build_backlog(req: AnalyzeRequest) -> List[str]:
    items = [
        "Create a repo-aware prompt contract for the target workflow",
        "Attach test harnesses and quality gates before enabling write actions",
        "Add a GitHub Actions pipeline that validates agent-generated changes",
        "Track reviewer acceptance rate and average edit distance after agent suggestions",
    ]
    if req.constraints:
        items.append("Encode environment constraints and security boundaries into agent instructions")
    if req.objective:
        items.append("Define a success metric tied directly to the stated objective")
    return items[:5]


@app.get("/")
def root() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "app": "Flower DevEx Agent Studio"}


@app.post("/api/analyze")
def analyze(req: AnalyzeRequest) -> dict:
    metrics = build_metrics(req)
    return {
        "title": pick_workflow_type(req.workflow + " " + req.challenge),
        "recommendation": build_recommendation(req, metrics),
        "metrics": metrics,
        "agent_cards": build_context_cards(req),
        "quality_harness": build_quality_harness(req),
        "backlog": build_backlog(req),
    }


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)
