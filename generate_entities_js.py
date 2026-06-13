"""
Generate ENTITIES JS array (entities_data.js) for the TaxGraph dashboard,
derived from the REAL pipeline outputs:
  - entity_resolution_output.json
  - deviation_scores_output.json
"""
import json

entities = json.load(open("entity_resolution_output.json", encoding="utf-8"))
scores = {r["entity_id"]: r for r in json.load(open("deviation_scores_output.json", encoding="utf-8"))}

CITY_MAP = {"Islamabad": "Islamabad", "Lahore": "Lahore", "Rawalpindi": "Rawalpindi", "Karachi": "Karachi"}

def risk_band(score):
    if score >= 90: return "critical"
    if score >= 70: return "high"
    return "medium"

out = []
for idx, e in enumerate(entities, start=1):
    s = scores[e["entity_id"]]
    score = s["deviation_score"]
    risk = risk_band(score)

    vehicles = [f"{v['make']} {v['model']} ({v['engine_cc']}cc) — PKR {v['value_pkr']:,}" for v in e["vehicles"]]
    utility = e["utility"]

    assets = {}
    if vehicles:
        assets["Vehicles"] = vehicles
    if utility:
        assets["Utility (WAPDA)"] = f"{utility['consumer_id']} — PKR {utility['avg_monthly_bill_pkr']:,}/month ({utility['avg_monthly_units_kwh']} kWh)"

    evidence = []
    evidence.append({
        "source": "NADRA", "field": "Identity",
        "value": f"{e['name']} ({e['name_urdu']})", "flag": False,
        "note": f"CNIC {e['cnic']}, {e['city']}"
    })
    for v in e["vehicles"]:
        conf = e["match_scores"].get(f"excise_{v['reg_no']}", 0)
        evidence.append({
            "source": "Excise", "field": f"Vehicle {v['reg_no']}",
            "value": f"{v['make']} {v['model']} ({v['engine_cc']}cc) — PKR {v['value_pkr']:,}",
            "flag": v["engine_cc"] >= 2000,
            "note": f"Entity-resolution match confidence: {conf*100:.1f}%"
        })
    if utility:
        conf = e["match_scores"].get("wapda", 0)
        evidence.append({
            "source": "WAPDA", "field": "Electricity Bill",
            "value": f"PKR {utility['avg_monthly_bill_pkr']:,}/month",
            "flag": utility["avg_monthly_bill_pkr"] > 200000 and s["declared_income_pkr"] < 1000000,
            "note": f"Match confidence: {conf*100:.1f}%"
        })
    evidence.append({
        "source": "FBR", "field": "Tax Filing",
        "value": f"{e['tax_filing']['status']} — Declared PKR {e['tax_filing']['declared_income_pkr']:,}",
        "flag": e["tax_filing"]["status"] == "Non-Filer" or s["deviation_score"] > 70,
        "note": f"Tax paid: PKR {e['tax_filing']['tax_paid_pkr']:,}"
    })

    audit = []
    for reason in s["audit_reasons"]:
        is_clean = reason.startswith("No major deviation")
        audit.append({
            "c": "green" if is_clean else ("red" if score >= 90 else "amber"),
            "icon": "✓" if is_clean else "🚨",
            "label": reason,
            "detail": (
                f"Entity {e['entity_id']} ({e['name']}, CNIC {e['cnic']}): "
                f"declared income PKR {s['declared_income_pkr']:,} vs. estimated lifestyle "
                f"income PKR {s['estimated_lifestyle_income_pkr']:,} derived from linked "
                f"vehicle and utility records. Deviation score: {score}/100."
            )
        })
    audit.append({
        "c": "purple", "icon": "🕸",
        "label": f"Knowledge graph linkage — {len(e['vehicles']) + (1 if utility else 0) + 1} cross-DB edges",
        "detail": (
            f"Entity resolved across NADRA, Excise, WAPDA and FBR via fuzzy name/CNIC/address "
            f"matching (SequenceMatcher + CNIC-prefix anchoring). "
            f"Match confidences: {json.dumps(e['match_scores'])}"
        )
    })

    conf = {k.split('_')[0].upper() if '_' in k else k.upper(): round(v*100) for k, v in e["match_scores"].items()}
    if not conf:
        conf = {"NADRA": 100}
    conf["FBR"] = 100

    out.append({
        "id": idx,
        "entity_id": e["entity_id"],
        "name": e["name"],
        "name_urdu": e["name_urdu"],
        "cnic": e["cnic"],
        "city": CITY_MAP.get(e["city"], e["city"]),
        "risk": risk,
        "score": round(score),
        "declared_income": s["declared_income_pkr"],
        "lifestyle_income": s["estimated_lifestyle_income_pkr"],
        "assets": assets,
        "bills": {"electricity": utility["avg_monthly_bill_pkr"] if utility else 0},
        "fbr_return": f"{e['tax_filing']['status']} (FY2024) — Declared PKR {e['tax_filing']['declared_income_pkr']:,}",
        "evidence": evidence,
        "audit": audit,
        "conf": conf
    })

js = "const ENTITIES = " + json.dumps(out, indent=2, ensure_ascii=False) + ";\n"
with open("entities_data.js", "w", encoding="utf-8") as f:
    f.write(js)

print(f"Generated entities_data.js with {len(out)} entities")
print(f"Risk distribution: critical={sum(1 for e in out if e['risk']=='critical')}, "
      f"high={sum(1 for e in out if e['risk']=='high')}, "
      f"medium={sum(1 for e in out if e['risk']=='medium')}")
