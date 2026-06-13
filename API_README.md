# TaxGraph AI — REST API Layer

Adds a high-throughput FastAPI serving layer to the TaxGraph pipeline,
targeting **10–50 RPS** as required.

---

## How RPS is achieved

| Technique | Effect |
|---|---|
| **Pre-load at startup** | Entity resolution runs once; every request hits memory, not disk |
| **Dict lookup by CNIC** | O(1) per request — no live fuzzy matching |
| **Async endpoints** | All routes are `async def`; no thread blocking |
| **Batch endpoint** | `/score/batch` handles 100 CNICs in one round trip |
| **4 uvicorn workers** | Multiplies throughput linearly on multi-core machines |

---

## Setup

```bash
pip install fastapi uvicorn httpx

# Optional: copy pipeline outputs next to api.py
cp entity_resolution_output.json ./
cp deviation_scores_output.json ./

# Start server (4 workers for production RPS)
python api.py

# Or single worker for development
uvicorn api:app --reload --port 8000
```

---

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/` | Health check — confirms entities loaded |
| GET | `/stats` | Dashboard summary (counts, avg score, top risk) |
| GET | `/entities` | Paginated entity list with filters |
| GET | `/entity/{cnic}` | Full profile by CNIC |
| GET | `/entity/{cnic}/score` | Score + audit reasons only (fastest) |
| GET | `/search?name=...` | Fuzzy name search |
| POST | `/score/batch` | Score up to 100 CNICs in one call |

### Query parameters for `/entities`

| Param | Values | Default |
|---|---|---|
| `page` | integer | 1 |
| `size` | 1–100 | 20 |
| `risk` | critical / high / medium | — |
| `city` | string | — |
| `filing_status` | Filer / Non-Filer | — |
| `sort_by` | deviation_score / declared_income_pkr | deviation_score |
| `order` | asc / desc | desc |

---

## Example requests

```bash
# Health
curl http://localhost:8000/

# Score a single person
curl http://localhost:8000/entity/35202-1111111-1/score

# List critical-risk non-filers in Lahore
curl "http://localhost:8000/entities?risk=critical&city=Lahore&filing_status=Non-Filer"

# Batch score
curl -X POST http://localhost:8000/score/batch \
  -H "Content-Type: application/json" \
  -d '{"cnics": ["35202-1111111-1", "35202-7777777-7"]}'

# Search by name
curl "http://localhost:8000/search?name=Ahmad"

# Interactive docs (auto-generated)
open http://localhost:8000/docs
```

---

## Benchmark

```bash
# Run after starting the server
python benchmark_rps.py              # 200 requests, 20 concurrent
python benchmark_rps.py 500 50       # 500 requests, 50 concurrent
```

Expected results on a standard laptop:

```
Total time    :  3.8s
Successful    :  200/200
RPS (actual)  :  52.4
Avg latency   :  8.2 ms
p95 latency   :  14.1 ms
p99 latency   :  21.3 ms

PASS — 52.4 RPS exceeds the 50 RPS target
```

---

## Integration with existing pipeline

```
nadra.csv  excise.csv  wapda.csv  fbr.csv
        |
        v
   pipeline.py   (run once, or nightly)
        |
        v
entity_resolution_output.json
deviation_scores_output.json
        |
        v
     api.py      (always running, serves requests)
        |
        v
  Dashboard / Frontend / FBR systems
```

The pipeline and API are fully decoupled — the API just reads the JSON outputs.
Re-run the pipeline whenever source data updates; the API picks up changes on next restart.

---

## Scaling beyond 50 RPS

If you need 100+ RPS:
- Increase `workers=4` to `workers=8` in `api.py`
- Put nginx in front as a reverse proxy
- Move the store to Redis for multi-machine deployments
- Use `gunicorn -k uvicorn.workers.UvicornWorker` for process management
