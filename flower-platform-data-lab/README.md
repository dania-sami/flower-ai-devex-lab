# Flower Platform Data Lab

I built this project to demonstrate how I think about platform and data engineering in a setting similar to Flower.

Instead of making a generic data project, I wanted to model the kind of platform work described in the role: a scalable data foundation that supports ingestion, transformation, quality checks, observability, and self-service delivery for fast-moving teams.

This project simulates an energy data platform with a lakehouse-style flow, pipeline monitoring, asset ingestion visibility, and embedded quality checks. I also included platform support agents that focus on ingestion, quality, and cost review because I find the intersection of platform engineering, automation, and developer productivity especially interesting.

## What this project demonstrates

- Python and SQL-oriented data engineering thinking
- Lakehouse-style platform design with bronze, silver, and gold flow concepts
- Pipeline orchestration and observability
- Data quality and reliability as first-class concerns
- Cost-aware platform decisions
- Declarative, self-service platform patterns
- Clear UI for platform visibility and operations

## Project structure

```text
flower-platform-data-lab/
├── backend/
│   ├── app.py
│   └── requirements.txt
├── frontend/
│   ├── app.js
│   ├── index.html
│   └── styles.css
├── .github/
│   └── workflows/
│       └── ci.yml
├── infra/
│   └── terraform/
│       └── main.tf
└── README.md
```

## Features

### 1. Platform overview dashboard
A polished dashboard showing operational platform metrics such as uptime, average market price, quality score, renewable coverage, and daily platform cost.

### 2. Pipeline execution view
A pipeline view that shows run freshness, execution duration, and ownership. This reflects how I think about data platform reliability and team visibility.

### 3. Embedded quality framework
Quality checks are shown as part of the workflow rather than an afterthought. This mirrors the role’s focus on correctness, edge cases, and bullet-proof systems.

### 4. Asset ingestion layer
The dashboard includes simulated energy asset ingestion with availability, latency, and capacity information.

### 5. Platform support agents
I added lightweight platform agents for ingestion, quality, and cost review. They are designed as supportive operational components rather than a separate AI demo.

## How to run locally

### Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Then open:

```text
http://127.0.0.1:8000
```

## Notes

I intentionally kept the project local and self-contained so it runs without external credentials, APIs, or cloud setup.

If I were extending this further, I would add:

- dbt models for transformations
- Spark-based workload simulation
- persistent storage for run history
- more detailed lineage visualization
- CI checks for data tests and schema validation
- Terraform modules for reproducible local and cloud deployment

## Why I built it

What stood out to me in the Flower role was that it is not just about moving data from one place to another. It is about building the platform that enables other teams to move faster with confidence.

That is exactly the kind of engineering work I want to grow in.
