# TaxGraph AI

> Knowledge Graph–Based Tax Compliance Intelligence System for Identifying High-Risk Non-Filers Through Entity Resolution, Graph Analytics, and Explainable AI.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" />
  <img src="https://img.shields.io/badge/Knowledge%20Graphs-NetworkX-green.svg" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-teal.svg" />
  <img src="https://img.shields.io/badge/D3.js-Visualization-orange.svg" />
  <img src="https://img.shields.io/badge/Hackathon-CUST%202026-red.svg" />
</p>

---

## Overview

TaxGraph AI is an AI-powered tax intelligence platform designed to address one of Pakistan's most critical economic challenges: the identification of high-net-worth individuals whose declared income does not align with their observed lifestyle and asset ownership.

The system integrates multiple fragmented civic datasets, performs entity resolution across records, constructs a knowledge graph of relationships, and generates a **Tax Compliance Deviation Score (TCDS)** along with a fully explainable audit trail.

Built for the **CUST Hackathon 2026** challenge:

**Graph AI for Broadening the National Tax Net**

---

## Problem Statement

Pakistan's tax ecosystem is fragmented across multiple government departments. Valuable taxpayer signals are distributed among:

- Federal Board of Revenue (FBR)
- NADRA Identity Records
- Excise & Taxation Vehicle Registries
- WAPDA Utility Consumption Data
- Property Registries
- Immigration & Travel Logs

These datasets often operate independently, making it difficult to identify individuals whose:

- Assets significantly exceed declared income
- Utility consumption indicates undisclosed wealth
- Luxury ownership patterns conflict with tax filings
- Multiple records represent the same individual under different identities

---

## Solution Architecture

TaxGraph AI combines:

### 1. Entity Resolution Engine

Links records belonging to the same individual across multiple databases using:

- CNIC Matching
- Fuzzy Name Matching
- Address Similarity Scoring
- Urdu/Roman Name Normalization
- Confidence-Based Record Linking

### 2. Knowledge Graph Construction

Relationships are modeled as a graph:

```text
Person
├── owns ─────► Vehicle
├── owns ─────► Property
├── pays ─────► Utility Meter
├── filed ────► Tax Return
├── traveled ─► Travel Record
└── linked ───► Business Entity
```

### 3. Tax Compliance Deviation Scoring

The platform calculates a risk score between **0 and 100** indicating the likelihood of tax non-compliance.

### 4. Explainable AI Audit Trail

Every flagged entity receives a human-readable explanation detailing:

- Why the entity was linked
- Which assets triggered suspicion
- Which databases contributed evidence
- The factors affecting the final score

---

## Core Features

- Multi-source Entity Resolution
- Knowledge Graph Generation
- Tax Compliance Deviation Score (TCDS)
- Explainable AI Audit Reports
- Interactive Dashboard
- Graph Visualization
- Risk Analytics
- JSON & CSV Export
- API Integration Support
- Synthetic Dataset Simulation

---

## Repository Structure

```text
TaxGraph-AI/
│
├── api.py
├── pipeline.py
├── benchmark_rps.py
├── generate_entities_js.py
│
├── dashboard.html
├── entities_data.js
│
├── nadra.csv
├── excise.csv
├── wapda.csv
├── fbr.csv
│
├── entity_resolution_output.json
├── deviation_scores.csv
├── deviation_scores_output.json
│
├── knowledge_graph.gexf
│
├── TaxGraph_Pipeline.ipynb
│
├── API_README.md
└── README.md
```

---

## Data Sources

| Dataset | Purpose |
|----------|----------|
| NADRA | Citizen identity records |
| Excise | Vehicle ownership information |
| WAPDA | Utility consumption data |
| FBR | Tax return and filing records |

> All datasets included in this repository are synthetic and anonymized for demonstration purposes.

---

## Tax Compliance Deviation Score (TCDS)

The TCDS is a composite risk indicator designed to highlight discrepancies between reported income and observed financial behavior.

### Scoring Factors

| Factor | Weight |
|----------|----------|
| Asset–Income Gap | 40% |
| Utility Consumption Risk | 25% |
| Filing Inconsistency | 20% |
| Cross-Database Anomalies | 15% |

### Risk Levels

| Score | Classification |
|---------|---------------|
| 0 – 25 | Low Risk |
| 26 – 50 | Medium Risk |
| 51 – 75 | High Risk |
| 76 – 100 | Critical Risk |

---

## Example Audit Output

```text
Entity: Ahmad Ali Khan

TCDS Score: 100

Evidence:

• Owns Toyota Land Cruiser (4500cc)
• Owns Toyota Fortuner (2700cc)
• Monthly Electricity Bill: PKR 310,000
• Declared Income: PKR 0
• Non-Filer in FY2024

Conclusion:

Observed lifestyle indicators significantly exceed
declared income. Entity recommended for audit review.
```

---

## Knowledge Graph Workflow

```text
NADRA
   │
   ▼
Entity Resolution
   │
   ├──────── Excise
   ├──────── WAPDA
   └──────── FBR
          │
          ▼
Knowledge Graph
          │
          ▼
Risk Scoring Engine
          │
          ▼
Explainable Audit Trail
```

---

## Technology Stack

### Backend

- Python
- Pandas
- NumPy
- FastAPI
- NetworkX

### Frontend

- HTML5
- CSS3
- JavaScript
- D3.js
- Chart.js

### Analytics

- Entity Resolution
- Fuzzy Matching
- Knowledge Graphs
- Graph Analytics
- Explainable AI (XAI)

---

## Running the Project

### Clone Repository

```bash
git clone https://github.com/yourusername/TaxGraph-AI.git
cd TaxGraph-AI
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Pipeline

```bash
python pipeline.py
```

### Start API

```bash
python api.py
```

### Launch Dashboard

```bash
python -m http.server 8000
```

Open:

```text
http://localhost:8000/dashboard.html
```

---

## Project Outputs

The pipeline generates:

| File | Description |
|--------|------------|
| entity_resolution_output.json | Linked entity records |
| deviation_scores.csv | Risk scoring results |
| deviation_scores_output.json | Detailed scoring explanations |
| knowledge_graph.gexf | Exportable graph structure |
| entities_data.js | Dashboard data source |

---

## Challenge Alignment

This project directly addresses the challenge requirements by implementing:

- Knowledge Graph Construction
- Entity Resolution Pipeline
- Tax Compliance Risk Scoring
- Explainable AI Audit Trails
- Multi-Dataset Integration
- Fraud Detection Methodology
- GovTech & FinTech Applications

---

## Future Enhancements

- Neo4j Integration
- Graph Neural Networks (GraphSAGE / GAT)
- Real-Time Streaming Pipelines
- SHAP-Based Explainability
- AML / KYC Extensions
- Provincial Tax Authority Integration
- Large-Scale Government Deployment

---

## Disclaimer

This project uses synthetic and anonymized datasets exclusively. No real taxpayer data, personally identifiable information, or government records are included.

The system is intended for educational, research, and demonstration purposes only.

---

## Authors

**TaxGraph AI Team**

CUST Hackathon 2026  
Graph AI for Broadening the National Tax Net

---
⭐ If you find this project interesting, consider starring the repository.
