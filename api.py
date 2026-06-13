"""
TaxGraph AI — FastAPI Serving Layer
=====================================
Wraps the pipeline outputs into a high-throughput REST API.
Pre-loads entity resolution + deviation scores at startup into memory
so every request is a simple dict lookup — no live fuzzy matching.

Targets: 10–50 RPS on a single worker, 100+ RPS with multiple workers.

Endpoints:
  GET  /                        Health check
  GET  /entities                List all entities (paginated)
  GET  /entity/{cnic}           Full profile by CNIC
  GET  /entity/{cnic}/score     Deviation score + audit reasons only
  GET  /search?name=...         Fuzzy name search (pre-indexed)
  GET  /stats                   Dashboard summary stats
  POST /score/batch             Score multiple CNICs in one call
"""

import json
import time
import asyncio
from pathlib import Path
from difflib import SequenceMatcher
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel


# ---------------------------------------------------------------
# IN-MEMORY STORE  (populated once at startup)
# ---------------------------------------------------------------
store: dict = {
    "by_cnic":      {},   # cnic  -> merged entity record
    "by_entity_id": {},   # ENT-* -> merged entity record
    "scores":       {},   # cnic  -> deviation score record
    "all_entities": [],   # ordered list for pagination
    "name_index":   [],   # [(normalised_name, cnic)] for fuzzy search
}


def load_data():
    """
    Load pipeline JSON outputs into memory.
    Falls back to bundled sample data if files aren't present
    so the API can demo without running the full pipeline first.
    """
    base = Path(__file__).parent

    entity_file = base / "entity_resolution_output.json"
    scores_file = base / "deviation_scores_output.json"

    if entity_file.exists() and scores_file.exists():
        entities = json.loads(entity_file.read_text(encoding="utf-8"))
        scores   = json.loads(scores_file.read_text(encoding="utf-8"))
    else:
        # ---- bundled sample (subset from the provided JSONs) ----
        entities = SAMPLE_ENTITIES
        scores   = SAMPLE_SCORES

    score_map = {r["cnic"]: r for r in scores}

    for e in entities:
        cnic = e["cnic"]
        merged = {**e, "deviation": score_map.get(cnic, {})}
        store["by_cnic"][cnic]              = merged
        store["by_entity_id"][e["entity_id"]] = merged
        store["all_entities"].append(merged)
        store["name_index"].append((e["name"].lower(), cnic))

    print(f"[TaxGraph] Loaded {len(entities)} entities into memory store")


# ---------------------------------------------------------------
# LIFESPAN  (replaces @app.on_event)
# ---------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    load_data()
    yield


# ---------------------------------------------------------------
# APP
# ---------------------------------------------------------------
app = FastAPI(
    title="TaxGraph AI",
    description="Tax compliance deviation scoring API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------
# MODELS
# ---------------------------------------------------------------
class BatchRequest(BaseModel):
    cnics: list[str]


# ---------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------
def risk_band(score: float) -> str:
    if score >= 90: return "critical"
    if score >= 70: return "high"
    return "medium"


def slim(entity: dict) -> dict:
    """Return a lighter record for list views."""
    d = entity.get("deviation", {})
    return {
        "entity_id":    entity["entity_id"],
        "name":         entity["name"],
        "cnic":         entity["cnic"],
        "city":         entity["city"],
        "filing_status": entity["tax_filing"]["status"],
        "declared_income_pkr": entity["tax_filing"]["declared_income_pkr"],
        "estimated_lifestyle_income_pkr": d.get("estimated_lifestyle_income_pkr", 0),
        "deviation_score": d.get("deviation_score", 0),
        "risk": risk_band(d.get("deviation_score", 0)),
    }


# ---------------------------------------------------------------
# ROUTES
# ---------------------------------------------------------------
@app.get("/", tags=["health"])
async def health():
    return {
        "status": "ok",
        "entities_loaded": len(store["all_entities"]),
        "timestamp": time.time(),
    }


@app.get("/stats", tags=["dashboard"])
async def stats():
    scores = [e["deviation"].get("deviation_score", 0) for e in store["all_entities"]]
    statuses = [e["tax_filing"]["status"] for e in store["all_entities"]]
    risks = [risk_band(s) for s in scores]
    return {
        "total_entities": len(store["all_entities"]),
        "non_filers": statuses.count("Non-Filer"),
        "filers": statuses.count("Filer"),
        "risk_critical": risks.count("critical"),
        "risk_high": risks.count("high"),
        "risk_medium": risks.count("medium"),
        "avg_deviation_score": round(sum(scores) / len(scores), 1) if scores else 0,
        "top_risk_entity": max(store["all_entities"],
            key=lambda e: e["deviation"].get("deviation_score", 0),
            default={}
        ).get("name", "N/A"),
    }


@app.get("/entities", tags=["entities"])
async def list_entities(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    risk: Optional[str] = Query(None, description="Filter: critical | high | medium"),
    city: Optional[str] = None,
    filing_status: Optional[str] = Query(None, description="Filer | Non-Filer"),
    sort_by: str = Query("deviation_score", description="Field to sort by"),
    order: str = Query("desc", description="asc | desc"),
):
    results = [slim(e) for e in store["all_entities"]]

    if risk:
        results = [r for r in results if r["risk"] == risk.lower()]
    if city:
        results = [r for r in results if city.lower() in r["city"].lower()]
    if filing_status:
        results = [r for r in results if r["filing_status"] == filing_status]

    reverse = order == "desc"
    results.sort(key=lambda r: r.get(sort_by, 0), reverse=reverse)

    start = (page - 1) * size
    return {
        "total": len(results),
        "page": page,
        "size": size,
        "results": results[start: start + size],
    }


@app.get("/entity/{cnic}", tags=["entities"])
async def get_entity(cnic: str):
    entity = store["by_cnic"].get(cnic)
    if not entity:
        raise HTTPException(status_code=404, detail=f"No entity found for CNIC {cnic}")
    return entity


@app.get("/entity/{cnic}/score", tags=["scoring"])
async def get_score(cnic: str):
    entity = store["by_cnic"].get(cnic)
    if not entity:
        raise HTTPException(status_code=404, detail=f"No entity found for CNIC {cnic}")
    d = entity.get("deviation", {})
    return {
        "cnic":             cnic,
        "name":             entity["name"],
        "deviation_score":  d.get("deviation_score", 0),
        "risk":             risk_band(d.get("deviation_score", 0)),
        "filing_status":    entity["tax_filing"]["status"],
        "declared_income_pkr": entity["tax_filing"]["declared_income_pkr"],
        "estimated_lifestyle_income_pkr": d.get("estimated_lifestyle_income_pkr", 0),
        "audit_reasons":    d.get("audit_reasons", []),
        "match_confidence": entity.get("match_scores", {}),
    }


@app.get("/search", tags=["entities"])
async def search(name: str = Query(..., min_length=2)):
    q = name.lower()
    results = []
    for norm_name, cnic in store["name_index"]:
        score = SequenceMatcher(None, q, norm_name).ratio()
        if score > 0.45:
            results.append((score, cnic))
    results.sort(reverse=True)
    return {
        "query": name,
        "results": [slim(store["by_cnic"][cnic]) for _, cnic in results[:10]],
    }


@app.post("/score/batch", tags=["scoring"])
async def batch_score(req: BatchRequest):
    if len(req.cnics) > 100:
        raise HTTPException(status_code=400, detail="Max 100 CNICs per batch request")

    async def score_one(cnic: str):
        entity = store["by_cnic"].get(cnic)
        if not entity:
            return {"cnic": cnic, "error": "not found"}
        d = entity.get("deviation", {})
        return {
            "cnic":            cnic,
            "name":            entity["name"],
            "deviation_score": d.get("deviation_score", 0),
            "risk":            risk_band(d.get("deviation_score", 0)),
            "audit_reasons":   d.get("audit_reasons", []),
        }

    results = await asyncio.gather(*[score_one(c) for c in req.cnics])
    return {"count": len(results), "results": list(results)}


# ---------------------------------------------------------------
# BUNDLED SAMPLE DATA (so API works without pipeline CSVs)
# ---------------------------------------------------------------
SAMPLE_ENTITIES = [
  {"entity_id":"ENT-11-1","cnic":"35202-1111111-1","name":"Ahmad Ali Khan","name_urdu":"احمد علی خان","address":"House 12 Street 5 F-8 Markaz","city":"Islamabad","vehicles":[{"reg_no":"ISB-2024-0011","make":"Toyota","model":"Land Cruiser","engine_cc":4500,"value_pkr":45000000},{"reg_no":"ISB-2023-7765","make":"Toyota","model":"Fortuner","engine_cc":2700,"value_pkr":18500000}],"utility":{"consumer_id":"WAP-100234","avg_monthly_bill_pkr":310000,"avg_monthly_units_kwh":4200},"tax_filing":{"status":"Non-Filer","declared_income_pkr":0,"tax_paid_pkr":0},"match_scores":{"excise_ISB-2024-0011":0.918,"excise_ISB-2023-7765":0.849,"wapda":1.0}},
  {"entity_id":"ENT-77-7","cnic":"35202-7777777-7","name":"Tariq Mehmood","name_urdu":"طارق محمود","address":"House 77 Model Town","city":"Lahore","vehicles":[{"reg_no":"LHR-2023-5567","make":"Toyota","model":"Prado","engine_cc":3000,"value_pkr":28000000}],"utility":{"consumer_id":"WAP-102998","avg_monthly_bill_pkr":375000,"avg_monthly_units_kwh":5100},"tax_filing":{"status":"Non-Filer","declared_income_pkr":0,"tax_paid_pkr":0},"match_scores":{"excise_LHR-2023-5567":1.0,"wapda":1.0}},
  {"entity_id":"ENT-01-0","cnic":"35202-1010101-0","name":"Usman Farooq","name_urdu":"عثمان فاروق","address":"House 5 Gulberg III","city":"Lahore","vehicles":[{"reg_no":"LHR-2024-8810","make":"Honda","model":"City","engine_cc":1300,"value_pkr":4200000}],"utility":{"consumer_id":"WAP-104120","avg_monthly_bill_pkr":98000,"avg_monthly_units_kwh":1400},"tax_filing":{"status":"Non-Filer","declared_income_pkr":0,"tax_paid_pkr":0},"match_scores":{"excise_LHR-2024-8810":1.0,"wapda":1.0}},
  {"entity_id":"ENT-44-4","cnic":"35202-4444444-4","name":"Bilal Hussain","name_urdu":"بلال حسین","address":"House 9 Bahria Town","city":"Rawalpindi","vehicles":[{"reg_no":"RWP-2021-9981","make":"Suzuki","model":"Alto","engine_cc":1000,"value_pkr":2200000}],"utility":{"consumer_id":"WAP-101455","avg_monthly_bill_pkr":68000,"avg_monthly_units_kwh":950},"tax_filing":{"status":"Filer","declared_income_pkr":600000,"tax_paid_pkr":5000},"match_scores":{"excise_RWP-2021-9981":0.995,"wapda":1.0}},
  {"entity_id":"ENT-99-9","cnic":"35202-9999999-9","name":"Nadia Chaudhry","name_urdu":"ندیہ چودھری","address":"House 21 G-9/2 Islamabad","city":"Islamabad","vehicles":[{"reg_no":"ISB-2022-4432","make":"Suzuki","model":"Cultus","engine_cc":1000,"value_pkr":2900000}],"utility":{"consumer_id":"WAP-103321","avg_monthly_bill_pkr":82000,"avg_monthly_units_kwh":1100},"tax_filing":{"status":"Filer","declared_income_pkr":950000,"tax_paid_pkr":45000},"match_scores":{"excise_ISB-2022-4432":0.947,"wapda":1.0}},
  {"entity_id":"ENT-66-6","cnic":"35202-6666666-6","name":"Mariam Sheikh","name_urdu":"مریم شیخ","address":"Flat 3B Clifton Block 5","city":"Karachi","vehicles":[{"reg_no":"KHI-2020-1123","make":"Toyota","model":"Corolla","engine_cc":1600,"value_pkr":4800000}],"utility":{"consumer_id":"WAP-102110","avg_monthly_bill_pkr":195000,"avg_monthly_units_kwh":2600},"tax_filing":{"status":"Filer","declared_income_pkr":2400000,"tax_paid_pkr":310000},"match_scores":{"excise_KHI-2020-1123":0.958,"wapda":1.0}},
]

SAMPLE_SCORES = [
  {"entity_id":"ENT-11-1","name":"Ahmad Ali Khan","cnic":"35202-1111111-1","filing_status":"Non-Filer","declared_income_pkr":0,"estimated_lifestyle_income_pkr":24405000,"deviation_score":100.0,"audit_reasons":["Non-filer owns 2 registered vehicle(s) worth PKR 63,500,000","Electricity bill of PKR 310,000/month inconsistent with declared income of PKR 0","Owns high-engine-capacity vehicle(s) ['ISB-2024-0011', 'ISB-2023-7765'] (>=2000cc) despite low declared income"],"linked_records":{"vehicles":["ISB-2024-0011","ISB-2023-7765"],"utility":"WAP-100234"},"match_confidence":{"excise_ISB-2024-0011":0.918,"excise_ISB-2023-7765":0.849,"wapda":1.0}},
  {"entity_id":"ENT-77-7","name":"Tariq Mehmood","cnic":"35202-7777777-7","filing_status":"Non-Filer","declared_income_pkr":0,"estimated_lifestyle_income_pkr":22200000,"deviation_score":100.0,"audit_reasons":["Non-filer owns 1 registered vehicle(s) worth PKR 28,000,000","Electricity bill of PKR 375,000/month inconsistent with declared income of PKR 0","Owns high-engine-capacity vehicle(s) ['LHR-2023-5567'] (>=2000cc) despite low declared income"],"linked_records":{"vehicles":["LHR-2023-5567"],"utility":"WAP-102998"},"match_confidence":{"excise_LHR-2023-5567":1.0,"wapda":1.0}},
  {"entity_id":"ENT-01-0","name":"Usman Farooq","cnic":"35202-1010101-0","filing_status":"Non-Filer","declared_income_pkr":0,"estimated_lifestyle_income_pkr":5334000,"deviation_score":100.0,"audit_reasons":["Non-filer owns 1 registered vehicle(s) worth PKR 4,200,000"],"linked_records":{"vehicles":["LHR-2024-8810"],"utility":"WAP-104120"},"match_confidence":{"excise_LHR-2024-8810":1.0,"wapda":1.0}},
  {"entity_id":"ENT-44-4","name":"Bilal Hussain","cnic":"35202-4444444-4","filing_status":"Filer","declared_income_pkr":600000,"estimated_lifestyle_income_pkr":3594000,"deviation_score":83.3,"audit_reasons":["No major deviation detected; declared income consistent with observed assets"],"linked_records":{"vehicles":["RWP-2021-9981"],"utility":"WAP-101455"},"match_confidence":{"excise_RWP-2021-9981":0.995,"wapda":1.0}},
  {"entity_id":"ENT-99-9","name":"Nadia Chaudhry","cnic":"35202-9999999-9","filing_status":"Filer","declared_income_pkr":950000,"estimated_lifestyle_income_pkr":4371000,"deviation_score":78.3,"audit_reasons":["No major deviation detected; declared income consistent with observed assets"],"linked_records":{"vehicles":["ISB-2022-4432"],"utility":"WAP-103321"},"match_confidence":{"excise_ISB-2022-4432":0.947,"wapda":1.0}},
  {"entity_id":"ENT-66-6","name":"Mariam Sheikh","cnic":"35202-6666666-6","filing_status":"Filer","declared_income_pkr":2400000,"estimated_lifestyle_income_pkr":10080000,"deviation_score":76.2,"audit_reasons":["No major deviation detected; declared income consistent with observed assets"],"linked_records":{"vehicles":["KHI-2020-1123"],"utility":"WAP-102110"},"match_confidence":{"excise_KHI-2020-1123":0.958,"wapda":1.0}},
]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, workers=4, reload=False)
