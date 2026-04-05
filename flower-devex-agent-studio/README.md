# Flower DevEx Agent Studio

I built this project to demonstrate how I think about AI agents inside real software engineering workflows.

Instead of focusing only on model output, I wanted to prototype the broader developer experience around AI-assisted development: how an agent gets context, where it should be trusted, how its output can be verified, and how these workflows can plug into engineering systems like GitHub and CI pipelines.

## Why I built this

The Flower AI Developer Experience Internship stood out to me because it sits at the intersection of AI, platform engineering, and developer productivity. That is exactly the kind of space I want to keep building in.

This project explores a practical workflow where agents are treated as contributors rather than isolated tools. The goal is to help engineers reason about:

- when AI is the right fit for a workflow
- what guardrails are required before trusting agent output
- how to structure a pilot that improves developer productivity without compromising quality

## What the project includes

- A polished local web app with no external API dependency
- A multi-agent workflow made up of Discovery, Trust, Workflow, and Impact agents
- A recommendation engine for AI-assisted engineering workflows
- A trust harness that highlights correctness, validation, escalation, and observability layers
- A rollout backlog for piloting AI agents inside development teams

## Tech stack

- FastAPI
- Vanilla HTML, CSS, and JavaScript
- Local rule-based workflow analysis

## How to run

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Then open:

```text
http://127.0.0.1:8000
```

## What I would extend next

If I were to keep evolving this, I would add:

- GitHub Actions integration for validation flows
- richer repository context packaging for agents
- measurable productivity dashboards for pilot teams
- support for comparing multiple agent workflows side by side

## Notes

This project is intentionally local and lightweight so it can be run quickly and reviewed easily. I wanted it to be simple to demo while still showing how I think about trust, quality, and developer experience in agent-based systems.
