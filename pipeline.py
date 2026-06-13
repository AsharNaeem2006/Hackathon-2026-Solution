"""
TaxGraph AI - Pipeline Proof of Concept
=========================================
Implements:
  1. Entity Resolution (fuzzy string matching across NADRA/Excise/WAPDA/FBR)
  2. Knowledge Graph construction (NetworkX) - Person/Vehicle/Property/Meter nodes
  3. Tax Compliance Deviation Score + Explainable AI audit trail
"""

import pandas as pd
import networkx as nx
from difflib import SequenceMatcher
import json

# ---------------------------------------------------------------
# 1. LOAD DATA
# ---------------------------------------------------------------
nadra = pd.read_csv("nadra.csv")
excise = pd.read_csv("excise.csv")
wapda = pd.read_csv("wapda.csv")
fbr = pd.read_csv("fbr.csv")

print(f"Loaded: NADRA={len(nadra)}, Excise={len(excise)}, WAPDA={len(wapda)}, FBR={len(fbr)}")

# ---------------------------------------------------------------
# 2. ENTITY RESOLUTION
#    Fuzzy match names + CNIC-prefix + address similarity to
#    cluster records from different sources into one entity ID.
# ---------------------------------------------------------------

def name_similarity(a, b):
    return SequenceMatcher(None, str(a).lower(), str(b).lower()).ratio()

def cnic_prefix_match(c1, c2):
    """Match on CNIC without the trailing check digit."""
    c1 = str(c1).rsplit("-", 1)[0]
    c2 = str(c2).rsplit("-", 1)[0]
    return c1 == c2

def address_similarity(a, b):
    return SequenceMatcher(None, str(a).lower(), str(b).lower()).ratio()

entities = []  # resolved master entity records

for _, person in nadra.iterrows():
    entity = {
        "entity_id": f"ENT-{person['cnic'][-4:]}",
        "cnic": person["cnic"],
        "name": person["full_name"],
        "name_urdu": person["full_name_urdu"],
        "address": person["address"],
        "city": person["city"],
        "vehicles": [],
        "utility": None,
        "tax_filing": None,
        "match_scores": {},
    }

    # --- Match Excise records ---
    for _, v in excise.iterrows():
        cnic_match = cnic_prefix_match(person["cnic"], v["owner_cnic_partial"] + "-0")
        nm_score = name_similarity(person["full_name"], v["owner_name"])
        addr_score = address_similarity(person["address"], v["address"])
        combined = 0.5 * (1 if cnic_match else 0) + 0.3 * nm_score + 0.2 * addr_score
        if combined > 0.55:
            entity["vehicles"].append({
                "reg_no": v["reg_no"],
                "make": v["vehicle_make"],
                "model": v["vehicle_model"],
                "engine_cc": int(v["engine_cc"]),
                "value_pkr": int(v["value_pkr"]),
            })
            entity["match_scores"][f"excise_{v['reg_no']}"] = round(combined, 3)

    # --- Match WAPDA records ---
    best_w, best_score = None, 0
    for _, w in wapda.iterrows():
        nm_score = name_similarity(person["full_name"], w["consumer_name"])
        addr_score = address_similarity(person["address"], w["address"])
        combined = 0.6 * nm_score + 0.4 * addr_score
        if combined > best_score:
            best_score, best_w = combined, w
    if best_w is not None and best_score > 0.5:
        entity["utility"] = {
            "consumer_id": best_w["consumer_id"],
            "avg_monthly_bill_pkr": int(best_w["avg_monthly_bill_pkr"]),
            "avg_monthly_units_kwh": int(best_w["avg_monthly_units_kwh"]),
        }
        entity["match_scores"]["wapda"] = round(best_score, 3)

    # --- Match FBR records ---
    fbr_row = fbr[fbr["filer_cnic"] == person["cnic"]]
    if not fbr_row.empty:
        r = fbr_row.iloc[0]
        entity["tax_filing"] = {
            "status": r["filing_status"],
            "declared_income_pkr": int(r["declared_income_pkr"]),
            "tax_paid_pkr": int(r["tax_paid_pkr"]),
        }
    else:
        entity["tax_filing"] = {"status": "Non-Filer", "declared_income_pkr": 0, "tax_paid_pkr": 0}

    entities.append(entity)

print(f"\nEntity Resolution complete: {len(entities)} unified entities")

# ---------------------------------------------------------------
# 3. KNOWLEDGE GRAPH CONSTRUCTION (NetworkX)
# ---------------------------------------------------------------
G = nx.DiGraph()

for e in entities:
    G.add_node(e["entity_id"], type="Person", name=e["name"], city=e["city"])

    for v in e["vehicles"]:
        vnode = v["reg_no"]
        G.add_node(vnode, type="Vehicle", make=v["make"], model=v["model"], value=v["value_pkr"])
        G.add_edge(e["entity_id"], vnode, relation="owns")

    if e["utility"]:
        unode = e["utility"]["consumer_id"]
        G.add_node(unode, type="Meter", bill=e["utility"]["avg_monthly_bill_pkr"])
        G.add_edge(e["entity_id"], unode, relation="registered_at")

    fnode = f"FBR-{e['entity_id']}"
    G.add_node(fnode, type="TaxFiling", status=e["tax_filing"]["status"])
    G.add_edge(e["entity_id"], fnode, relation="filed_in")

print(f"Knowledge Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

# ---------------------------------------------------------------
# 4. TAX COMPLIANCE DEVIATION SCORE + EXPLAINABLE AUDIT TRAIL
#    Heuristic scorinlg (stand-in for a trained GNN anomaly model):
#    compares declared income vs. "lifestyle signal" income proxy
#    derived from vehicle value + utility consumption.
# ---------------------------------------------------------------

def estimate_lifestyle_income(entity):
    """Proxy annual income implied by assets/utility usage."""
    vehicle_component = sum(v["value_pkr"] for v in entity["vehicles"]) * 0.15  # ~15% of asset value/yr
    utility_component = (entity["utility"]["avg_monthly_bill_pkr"] * 12 * 4) if entity["utility"] else 0
    return vehicle_component + utility_component

results = []
for e in entities:
    lifestyle_income = estimate_lifestyle_income(e)
    declared = e["tax_filing"]["declared_income_pkr"]

    if lifestyle_income == 0:
        deviation = 0
    else:
        deviation = max(0, (lifestyle_income - declared) / lifestyle_income)

    score = round(min(deviation * 100, 100), 1)

    reasons = []
    if e["tax_filing"]["status"] == "Non-Filer" and e["vehicles"]:
        reasons.append(f"Non-filer owns {len(e['vehicles'])} registered vehicle(s) "
                        f"worth PKR {sum(v['value_pkr'] for v in e['vehicles']):,}")
    if e["utility"] and e["utility"]["avg_monthly_bill_pkr"] > 200000 and declared < 1000000:
        reasons.append(f"Electricity bill of PKR {e['utility']['avg_monthly_bill_pkr']:,}/month "
                        f"inconsistent with declared income of PKR {declared:,}")
    if any(v["engine_cc"] >= 2000 for v in e["vehicles"]) and declared < 2000000:
        big_cars = [v["reg_no"] for v in e["vehicles"] if v["engine_cc"] >= 2000]
        reasons.append(f"Owns high-engine-capacity vehicle(s) {big_cars} (>=2000cc) "
                        f"despite low declared income")
    if not reasons:
        reasons.append("No major deviation detected; declared income consistent with observed assets")

    results.append({
        "entity_id": e["entity_id"],
        "name": e["name"],
        "cnic": e["cnic"],
        "filing_status": e["tax_filing"]["status"],
        "declared_income_pkr": declared,
        "estimated_lifestyle_income_pkr": round(lifestyle_income),
        "deviation_score": score,
        "audit_reasons": reasons,
        "linked_records": {
            "vehicles": [v["reg_no"] for v in e["vehicles"]],
            "utility": e["utility"]["consumer_id"] if e["utility"] else None,
        },
        "match_confidence": e["match_scores"],
    })

results_sorted = sorted(results, key=lambda r: r["deviation_score"], reverse=True)

# ---------------------------------------------------------------
# 5. OUTPUT
# ---------------------------------------------------------------
print("\n=== TAX COMPLIANCE DEVIATION REPORT (sorted by risk) ===\n")
for r in results_sorted:
    print(f"{r['entity_id']} | {r['name']} | Score: {r['deviation_score']}/100 | "
          f"Status: {r['filing_status']}")
    print(f"   Declared: PKR {r['declared_income_pkr']:,}  |  "
          f"Lifestyle estimate: PKR {r['estimated_lifestyle_income_pkr']:,}")
    for reason in r["audit_reasons"]:
        print(f"   -> {reason}")
    print()

# Save outputs
with open("entity_resolution_output.json", "w", encoding="utf-8") as f:
    json.dump(entities, f, indent=2, ensure_ascii=False)

with open("deviation_scores_output.json", "w", encoding="utf-8") as f:
    json.dump(results_sorted, f, indent=2, ensure_ascii=False)

nx.write_gexf(G, "knowledge_graph.gexf")

pd.DataFrame(results_sorted)[[
    "entity_id", "name", "cnic", "filing_status", "declared_income_pkr",
    "estimated_lifestyle_income_pkr", "deviation_score"
]].to_csv("deviation_scores.csv", index=False)

print("Saved: entity_resolution_output.json, deviation_scores_output.json, "
      "deviation_scores.csv, knowledge_graph.gexf")
