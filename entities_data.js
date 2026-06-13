const ENTITIES = [
  {
    "id": 1,
    "entity_id": "ENT-11-1",
    "name": "Ahmad Ali Khan",
    "name_urdu": "احمد علی خان",
    "cnic": "35202-1111111-1",
    "city": "Islamabad",
    "risk": "critical",
    "score": 100,
    "declared_income": 0,
    "lifestyle_income": 24405000,
    "assets": {
      "Vehicles": [
        "Toyota Land Cruiser (4500cc) — PKR 45,000,000",
        "Toyota Fortuner (2700cc) — PKR 18,500,000"
      ],
      "Utility (WAPDA)": "WAP-100234 — PKR 310,000/month (4200 kWh)"
    },
    "bills": {
      "electricity": 310000
    },
    "fbr_return": "Non-Filer (FY2024) — Declared PKR 0",
    "evidence": [
      {
        "source": "NADRA",
        "field": "Identity",
        "value": "Ahmad Ali Khan (احمد علی خان)",
        "flag": false,
        "note": "CNIC 35202-1111111-1, Islamabad"
      },
      {
        "source": "Excise",
        "field": "Vehicle ISB-2024-0011",
        "value": "Toyota Land Cruiser (4500cc) — PKR 45,000,000",
        "flag": true,
        "note": "Entity-resolution match confidence: 91.8%"
      },
      {
        "source": "Excise",
        "field": "Vehicle ISB-2023-7765",
        "value": "Toyota Fortuner (2700cc) — PKR 18,500,000",
        "flag": true,
        "note": "Entity-resolution match confidence: 84.9%"
      },
      {
        "source": "WAPDA",
        "field": "Electricity Bill",
        "value": "PKR 310,000/month",
        "flag": true,
        "note": "Match confidence: 100.0%"
      },
      {
        "source": "FBR",
        "field": "Tax Filing",
        "value": "Non-Filer — Declared PKR 0",
        "flag": true,
        "note": "Tax paid: PKR 0"
      }
    ],
    "audit": [
      {
        "c": "red",
        "icon": "🚨",
        "label": "Non-filer owns 2 registered vehicle(s) worth PKR 63,500,000",
        "detail": "Entity ENT-11-1 (Ahmad Ali Khan, CNIC 35202-1111111-1): declared income PKR 0 vs. estimated lifestyle income PKR 24,405,000 derived from linked vehicle and utility records. Deviation score: 100.0/100."
      },
      {
        "c": "red",
        "icon": "🚨",
        "label": "Electricity bill of PKR 310,000/month inconsistent with declared income of PKR 0",
        "detail": "Entity ENT-11-1 (Ahmad Ali Khan, CNIC 35202-1111111-1): declared income PKR 0 vs. estimated lifestyle income PKR 24,405,000 derived from linked vehicle and utility records. Deviation score: 100.0/100."
      },
      {
        "c": "red",
        "icon": "🚨",
        "label": "Owns high-engine-capacity vehicle(s) ['ISB-2024-0011', 'ISB-2023-7765'] (>=2000cc) despite low declared income",
        "detail": "Entity ENT-11-1 (Ahmad Ali Khan, CNIC 35202-1111111-1): declared income PKR 0 vs. estimated lifestyle income PKR 24,405,000 derived from linked vehicle and utility records. Deviation score: 100.0/100."
      },
      {
        "c": "purple",
        "icon": "🕸",
        "label": "Knowledge graph linkage — 4 cross-DB edges",
        "detail": "Entity resolved across NADRA, Excise, WAPDA and FBR via fuzzy name/CNIC/address matching (SequenceMatcher + CNIC-prefix anchoring). Match confidences: {\"excise_ISB-2024-0011\": 0.918, \"excise_ISB-2023-7765\": 0.849, \"wapda\": 1.0}"
      }
    ],
    "conf": {
      "EXCISE": 85,
      "WAPDA": 100,
      "FBR": 100
    }
  },
  {
    "id": 2,
    "entity_id": "ENT-22-2",
    "name": "Ahmed A. Khan",
    "name_urdu": "احمد اے خان",
    "cnic": "35202-2222222-2",
    "city": "Islamabad",
    "risk": "critical",
    "score": 100,
    "declared_income": 0,
    "lifestyle_income": 14880000,
    "assets": {
      "Utility (WAPDA)": "WAP-100234 — PKR 310,000/month (4200 kWh)"
    },
    "bills": {
      "electricity": 310000
    },
    "fbr_return": "Non-Filer (FY2024) — Declared PKR 0",
    "evidence": [
      {
        "source": "NADRA",
        "field": "Identity",
        "value": "Ahmed A. Khan (احمد اے خان)",
        "flag": false,
        "note": "CNIC 35202-2222222-2, Islamabad"
      },
      {
        "source": "WAPDA",
        "field": "Electricity Bill",
        "value": "PKR 310,000/month",
        "flag": true,
        "note": "Match confidence: 64.9%"
      },
      {
        "source": "FBR",
        "field": "Tax Filing",
        "value": "Non-Filer — Declared PKR 0",
        "flag": true,
        "note": "Tax paid: PKR 0"
      }
    ],
    "audit": [
      {
        "c": "red",
        "icon": "🚨",
        "label": "Electricity bill of PKR 310,000/month inconsistent with declared income of PKR 0",
        "detail": "Entity ENT-22-2 (Ahmed A. Khan, CNIC 35202-2222222-2): declared income PKR 0 vs. estimated lifestyle income PKR 14,880,000 derived from linked vehicle and utility records. Deviation score: 100.0/100."
      },
      {
        "c": "purple",
        "icon": "🕸",
        "label": "Knowledge graph linkage — 2 cross-DB edges",
        "detail": "Entity resolved across NADRA, Excise, WAPDA and FBR via fuzzy name/CNIC/address matching (SequenceMatcher + CNIC-prefix anchoring). Match confidences: {\"wapda\": 0.649}"
      }
    ],
    "conf": {
      "WAPDA": 65,
      "FBR": 100
    }
  },
  {
    "id": 3,
    "entity_id": "ENT-33-3",
    "name": "Sana Fatima",
    "name_urdu": "ثناء فاطمہ",
    "cnic": "35202-3333333-3",
    "city": "Lahore",
    "risk": "high",
    "score": 76,
    "declared_income": 1800000,
    "lifestyle_income": 7455000,
    "assets": {
      "Vehicles": [
        "Honda Civic (1800cc) — PKR 6,500,000"
      ],
      "Utility (WAPDA)": "WAP-100892 — PKR 135,000/month (1800 kWh)"
    },
    "bills": {
      "electricity": 135000
    },
    "fbr_return": "Filer (FY2024) — Declared PKR 1,800,000",
    "evidence": [
      {
        "source": "NADRA",
        "field": "Identity",
        "value": "Sana Fatima (ثناء فاطمہ)",
        "flag": false,
        "note": "CNIC 35202-3333333-3, Lahore"
      },
      {
        "source": "Excise",
        "field": "Vehicle LHR-2022-3344",
        "value": "Honda Civic (1800cc) — PKR 6,500,000",
        "flag": false,
        "note": "Entity-resolution match confidence: 97.6%"
      },
      {
        "source": "WAPDA",
        "field": "Electricity Bill",
        "value": "PKR 135,000/month",
        "flag": false,
        "note": "Match confidence: 100.0%"
      },
      {
        "source": "FBR",
        "field": "Tax Filing",
        "value": "Filer — Declared PKR 1,800,000",
        "flag": true,
        "note": "Tax paid: PKR 185,000"
      }
    ],
    "audit": [
      {
        "c": "green",
        "icon": "✓",
        "label": "No major deviation detected; declared income consistent with observed assets",
        "detail": "Entity ENT-33-3 (Sana Fatima, CNIC 35202-3333333-3): declared income PKR 1,800,000 vs. estimated lifestyle income PKR 7,455,000 derived from linked vehicle and utility records. Deviation score: 75.9/100."
      },
      {
        "c": "purple",
        "icon": "🕸",
        "label": "Knowledge graph linkage — 3 cross-DB edges",
        "detail": "Entity resolved across NADRA, Excise, WAPDA and FBR via fuzzy name/CNIC/address matching (SequenceMatcher + CNIC-prefix anchoring). Match confidences: {\"excise_LHR-2022-3344\": 0.976, \"wapda\": 1.0}"
      }
    ],
    "conf": {
      "EXCISE": 98,
      "WAPDA": 100,
      "FBR": 100
    }
  },
  {
    "id": 4,
    "entity_id": "ENT-44-4",
    "name": "Bilal Hussain",
    "name_urdu": "بلال حسین",
    "cnic": "35202-4444444-4",
    "city": "Rawalpindi",
    "risk": "high",
    "score": 83,
    "declared_income": 600000,
    "lifestyle_income": 3594000,
    "assets": {
      "Vehicles": [
        "Suzuki Alto (1000cc) — PKR 2,200,000"
      ],
      "Utility (WAPDA)": "WAP-101455 — PKR 68,000/month (950 kWh)"
    },
    "bills": {
      "electricity": 68000
    },
    "fbr_return": "Filer (FY2024) — Declared PKR 600,000",
    "evidence": [
      {
        "source": "NADRA",
        "field": "Identity",
        "value": "Bilal Hussain (بلال حسین)",
        "flag": false,
        "note": "CNIC 35202-4444444-4, Rawalpindi"
      },
      {
        "source": "Excise",
        "field": "Vehicle RWP-2021-9981",
        "value": "Suzuki Alto (1000cc) — PKR 2,200,000",
        "flag": false,
        "note": "Entity-resolution match confidence: 99.5%"
      },
      {
        "source": "WAPDA",
        "field": "Electricity Bill",
        "value": "PKR 68,000/month",
        "flag": false,
        "note": "Match confidence: 100.0%"
      },
      {
        "source": "FBR",
        "field": "Tax Filing",
        "value": "Filer — Declared PKR 600,000",
        "flag": true,
        "note": "Tax paid: PKR 5,000"
      }
    ],
    "audit": [
      {
        "c": "green",
        "icon": "✓",
        "label": "No major deviation detected; declared income consistent with observed assets",
        "detail": "Entity ENT-44-4 (Bilal Hussain, CNIC 35202-4444444-4): declared income PKR 600,000 vs. estimated lifestyle income PKR 3,594,000 derived from linked vehicle and utility records. Deviation score: 83.3/100."
      },
      {
        "c": "purple",
        "icon": "🕸",
        "label": "Knowledge graph linkage — 3 cross-DB edges",
        "detail": "Entity resolved across NADRA, Excise, WAPDA and FBR via fuzzy name/CNIC/address matching (SequenceMatcher + CNIC-prefix anchoring). Match confidences: {\"excise_RWP-2021-9981\": 0.995, \"wapda\": 1.0}"
      }
    ],
    "conf": {
      "EXCISE": 100,
      "WAPDA": 100,
      "FBR": 100
    }
  },
  {
    "id": 5,
    "entity_id": "ENT-55-5",
    "name": "Bilal Husain",
    "name_urdu": "بلال حسین",
    "cnic": "35202-5555555-5",
    "city": "Rawalpindi",
    "risk": "critical",
    "score": 100,
    "declared_income": 0,
    "lifestyle_income": 3264000,
    "assets": {
      "Utility (WAPDA)": "WAP-101455 — PKR 68,000/month (950 kWh)"
    },
    "bills": {
      "electricity": 68000
    },
    "fbr_return": "Non-Filer (FY2024) — Declared PKR 0",
    "evidence": [
      {
        "source": "NADRA",
        "field": "Identity",
        "value": "Bilal Husain (بلال حسین)",
        "flag": false,
        "note": "CNIC 35202-5555555-5, Rawalpindi"
      },
      {
        "source": "WAPDA",
        "field": "Electricity Bill",
        "value": "PKR 68,000/month",
        "flag": false,
        "note": "Match confidence: 81.0%"
      },
      {
        "source": "FBR",
        "field": "Tax Filing",
        "value": "Non-Filer — Declared PKR 0",
        "flag": true,
        "note": "Tax paid: PKR 0"
      }
    ],
    "audit": [
      {
        "c": "green",
        "icon": "✓",
        "label": "No major deviation detected; declared income consistent with observed assets",
        "detail": "Entity ENT-55-5 (Bilal Husain, CNIC 35202-5555555-5): declared income PKR 0 vs. estimated lifestyle income PKR 3,264,000 derived from linked vehicle and utility records. Deviation score: 100.0/100."
      },
      {
        "c": "purple",
        "icon": "🕸",
        "label": "Knowledge graph linkage — 2 cross-DB edges",
        "detail": "Entity resolved across NADRA, Excise, WAPDA and FBR via fuzzy name/CNIC/address matching (SequenceMatcher + CNIC-prefix anchoring). Match confidences: {\"wapda\": 0.81}"
      }
    ],
    "conf": {
      "WAPDA": 81,
      "FBR": 100
    }
  },
  {
    "id": 6,
    "entity_id": "ENT-66-6",
    "name": "Mariam Sheikh",
    "name_urdu": "مریم شیخ",
    "cnic": "35202-6666666-6",
    "city": "Karachi",
    "risk": "high",
    "score": 76,
    "declared_income": 2400000,
    "lifestyle_income": 10080000,
    "assets": {
      "Vehicles": [
        "Toyota Corolla (1600cc) — PKR 4,800,000"
      ],
      "Utility (WAPDA)": "WAP-102110 — PKR 195,000/month (2600 kWh)"
    },
    "bills": {
      "electricity": 195000
    },
    "fbr_return": "Filer (FY2024) — Declared PKR 2,400,000",
    "evidence": [
      {
        "source": "NADRA",
        "field": "Identity",
        "value": "Mariam Sheikh (مریم شیخ)",
        "flag": false,
        "note": "CNIC 35202-6666666-6, Karachi"
      },
      {
        "source": "Excise",
        "field": "Vehicle KHI-2020-1123",
        "value": "Toyota Corolla (1600cc) — PKR 4,800,000",
        "flag": false,
        "note": "Entity-resolution match confidence: 95.8%"
      },
      {
        "source": "WAPDA",
        "field": "Electricity Bill",
        "value": "PKR 195,000/month",
        "flag": false,
        "note": "Match confidence: 100.0%"
      },
      {
        "source": "FBR",
        "field": "Tax Filing",
        "value": "Filer — Declared PKR 2,400,000",
        "flag": true,
        "note": "Tax paid: PKR 310,000"
      }
    ],
    "audit": [
      {
        "c": "green",
        "icon": "✓",
        "label": "No major deviation detected; declared income consistent with observed assets",
        "detail": "Entity ENT-66-6 (Mariam Sheikh, CNIC 35202-6666666-6): declared income PKR 2,400,000 vs. estimated lifestyle income PKR 10,080,000 derived from linked vehicle and utility records. Deviation score: 76.2/100."
      },
      {
        "c": "purple",
        "icon": "🕸",
        "label": "Knowledge graph linkage — 3 cross-DB edges",
        "detail": "Entity resolved across NADRA, Excise, WAPDA and FBR via fuzzy name/CNIC/address matching (SequenceMatcher + CNIC-prefix anchoring). Match confidences: {\"excise_KHI-2020-1123\": 0.958, \"wapda\": 1.0}"
      }
    ],
    "conf": {
      "EXCISE": 96,
      "WAPDA": 100,
      "FBR": 100
    }
  },
  {
    "id": 7,
    "entity_id": "ENT-77-7",
    "name": "Tariq Mehmood",
    "name_urdu": "طارق محمود",
    "cnic": "35202-7777777-7",
    "city": "Lahore",
    "risk": "critical",
    "score": 100,
    "declared_income": 0,
    "lifestyle_income": 22200000,
    "assets": {
      "Vehicles": [
        "Toyota Prado (3000cc) — PKR 28,000,000"
      ],
      "Utility (WAPDA)": "WAP-102998 — PKR 375,000/month (5100 kWh)"
    },
    "bills": {
      "electricity": 375000
    },
    "fbr_return": "Non-Filer (FY2024) — Declared PKR 0",
    "evidence": [
      {
        "source": "NADRA",
        "field": "Identity",
        "value": "Tariq Mehmood (طارق محمود)",
        "flag": false,
        "note": "CNIC 35202-7777777-7, Lahore"
      },
      {
        "source": "Excise",
        "field": "Vehicle LHR-2023-5567",
        "value": "Toyota Prado (3000cc) — PKR 28,000,000",
        "flag": true,
        "note": "Entity-resolution match confidence: 100.0%"
      },
      {
        "source": "WAPDA",
        "field": "Electricity Bill",
        "value": "PKR 375,000/month",
        "flag": true,
        "note": "Match confidence: 100.0%"
      },
      {
        "source": "FBR",
        "field": "Tax Filing",
        "value": "Non-Filer — Declared PKR 0",
        "flag": true,
        "note": "Tax paid: PKR 0"
      }
    ],
    "audit": [
      {
        "c": "red",
        "icon": "🚨",
        "label": "Non-filer owns 1 registered vehicle(s) worth PKR 28,000,000",
        "detail": "Entity ENT-77-7 (Tariq Mehmood, CNIC 35202-7777777-7): declared income PKR 0 vs. estimated lifestyle income PKR 22,200,000 derived from linked vehicle and utility records. Deviation score: 100.0/100."
      },
      {
        "c": "red",
        "icon": "🚨",
        "label": "Electricity bill of PKR 375,000/month inconsistent with declared income of PKR 0",
        "detail": "Entity ENT-77-7 (Tariq Mehmood, CNIC 35202-7777777-7): declared income PKR 0 vs. estimated lifestyle income PKR 22,200,000 derived from linked vehicle and utility records. Deviation score: 100.0/100."
      },
      {
        "c": "red",
        "icon": "🚨",
        "label": "Owns high-engine-capacity vehicle(s) ['LHR-2023-5567'] (>=2000cc) despite low declared income",
        "detail": "Entity ENT-77-7 (Tariq Mehmood, CNIC 35202-7777777-7): declared income PKR 0 vs. estimated lifestyle income PKR 22,200,000 derived from linked vehicle and utility records. Deviation score: 100.0/100."
      },
      {
        "c": "purple",
        "icon": "🕸",
        "label": "Knowledge graph linkage — 3 cross-DB edges",
        "detail": "Entity resolved across NADRA, Excise, WAPDA and FBR via fuzzy name/CNIC/address matching (SequenceMatcher + CNIC-prefix anchoring). Match confidences: {\"excise_LHR-2023-5567\": 1.0, \"wapda\": 1.0}"
      }
    ],
    "conf": {
      "EXCISE": 100,
      "WAPDA": 100,
      "FBR": 100
    }
  },
  {
    "id": 8,
    "entity_id": "ENT-88-8",
    "name": "M. Tariq Mehmud",
    "name_urdu": "ایم طارق محمود",
    "cnic": "35202-8888888-8",
    "city": "Lahore",
    "risk": "critical",
    "score": 100,
    "declared_income": 0,
    "lifestyle_income": 18000000,
    "assets": {
      "Utility (WAPDA)": "WAP-102998 — PKR 375,000/month (5100 kWh)"
    },
    "bills": {
      "electricity": 375000
    },
    "fbr_return": "Non-Filer (FY2024) — Declared PKR 0",
    "evidence": [
      {
        "source": "NADRA",
        "field": "Identity",
        "value": "M. Tariq Mehmud (ایم طارق محمود)",
        "flag": false,
        "note": "CNIC 35202-8888888-8, Lahore"
      },
      {
        "source": "WAPDA",
        "field": "Electricity Bill",
        "value": "PKR 375,000/month",
        "flag": true,
        "note": "Match confidence: 71.1%"
      },
      {
        "source": "FBR",
        "field": "Tax Filing",
        "value": "Non-Filer — Declared PKR 0",
        "flag": true,
        "note": "Tax paid: PKR 0"
      }
    ],
    "audit": [
      {
        "c": "red",
        "icon": "🚨",
        "label": "Electricity bill of PKR 375,000/month inconsistent with declared income of PKR 0",
        "detail": "Entity ENT-88-8 (M. Tariq Mehmud, CNIC 35202-8888888-8): declared income PKR 0 vs. estimated lifestyle income PKR 18,000,000 derived from linked vehicle and utility records. Deviation score: 100.0/100."
      },
      {
        "c": "purple",
        "icon": "🕸",
        "label": "Knowledge graph linkage — 2 cross-DB edges",
        "detail": "Entity resolved across NADRA, Excise, WAPDA and FBR via fuzzy name/CNIC/address matching (SequenceMatcher + CNIC-prefix anchoring). Match confidences: {\"wapda\": 0.711}"
      }
    ],
    "conf": {
      "WAPDA": 71,
      "FBR": 100
    }
  },
  {
    "id": 9,
    "entity_id": "ENT-99-9",
    "name": "Nadia Chaudhry",
    "name_urdu": "ندیہ چودھری",
    "cnic": "35202-9999999-9",
    "city": "Islamabad",
    "risk": "high",
    "score": 78,
    "declared_income": 950000,
    "lifestyle_income": 4371000,
    "assets": {
      "Vehicles": [
        "Suzuki Cultus (1000cc) — PKR 2,900,000"
      ],
      "Utility (WAPDA)": "WAP-103321 — PKR 82,000/month (1100 kWh)"
    },
    "bills": {
      "electricity": 82000
    },
    "fbr_return": "Filer (FY2024) — Declared PKR 950,000",
    "evidence": [
      {
        "source": "NADRA",
        "field": "Identity",
        "value": "Nadia Chaudhry (ندیہ چودھری)",
        "flag": false,
        "note": "CNIC 35202-9999999-9, Islamabad"
      },
      {
        "source": "Excise",
        "field": "Vehicle ISB-2022-4432",
        "value": "Suzuki Cultus (1000cc) — PKR 2,900,000",
        "flag": false,
        "note": "Entity-resolution match confidence: 94.7%"
      },
      {
        "source": "WAPDA",
        "field": "Electricity Bill",
        "value": "PKR 82,000/month",
        "flag": false,
        "note": "Match confidence: 100.0%"
      },
      {
        "source": "FBR",
        "field": "Tax Filing",
        "value": "Filer — Declared PKR 950,000",
        "flag": true,
        "note": "Tax paid: PKR 45,000"
      }
    ],
    "audit": [
      {
        "c": "green",
        "icon": "✓",
        "label": "No major deviation detected; declared income consistent with observed assets",
        "detail": "Entity ENT-99-9 (Nadia Chaudhry, CNIC 35202-9999999-9): declared income PKR 950,000 vs. estimated lifestyle income PKR 4,371,000 derived from linked vehicle and utility records. Deviation score: 78.3/100."
      },
      {
        "c": "purple",
        "icon": "🕸",
        "label": "Knowledge graph linkage — 3 cross-DB edges",
        "detail": "Entity resolved across NADRA, Excise, WAPDA and FBR via fuzzy name/CNIC/address matching (SequenceMatcher + CNIC-prefix anchoring). Match confidences: {\"excise_ISB-2022-4432\": 0.947, \"wapda\": 1.0}"
      }
    ],
    "conf": {
      "EXCISE": 95,
      "WAPDA": 100,
      "FBR": 100
    }
  },
  {
    "id": 10,
    "entity_id": "ENT-01-0",
    "name": "Usman Farooq",
    "name_urdu": "عثمان فاروق",
    "cnic": "35202-1010101-0",
    "city": "Lahore",
    "risk": "critical",
    "score": 100,
    "declared_income": 0,
    "lifestyle_income": 5334000,
    "assets": {
      "Vehicles": [
        "Honda City (1300cc) — PKR 4,200,000"
      ],
      "Utility (WAPDA)": "WAP-104120 — PKR 98,000/month (1400 kWh)"
    },
    "bills": {
      "electricity": 98000
    },
    "fbr_return": "Non-Filer (FY2024) — Declared PKR 0",
    "evidence": [
      {
        "source": "NADRA",
        "field": "Identity",
        "value": "Usman Farooq (عثمان فاروق)",
        "flag": false,
        "note": "CNIC 35202-1010101-0, Lahore"
      },
      {
        "source": "Excise",
        "field": "Vehicle LHR-2024-8810",
        "value": "Honda City (1300cc) — PKR 4,200,000",
        "flag": false,
        "note": "Entity-resolution match confidence: 100.0%"
      },
      {
        "source": "WAPDA",
        "field": "Electricity Bill",
        "value": "PKR 98,000/month",
        "flag": false,
        "note": "Match confidence: 100.0%"
      },
      {
        "source": "FBR",
        "field": "Tax Filing",
        "value": "Non-Filer — Declared PKR 0",
        "flag": true,
        "note": "Tax paid: PKR 0"
      }
    ],
    "audit": [
      {
        "c": "red",
        "icon": "🚨",
        "label": "Non-filer owns 1 registered vehicle(s) worth PKR 4,200,000",
        "detail": "Entity ENT-01-0 (Usman Farooq, CNIC 35202-1010101-0): declared income PKR 0 vs. estimated lifestyle income PKR 5,334,000 derived from linked vehicle and utility records. Deviation score: 100.0/100."
      },
      {
        "c": "purple",
        "icon": "🕸",
        "label": "Knowledge graph linkage — 3 cross-DB edges",
        "detail": "Entity resolved across NADRA, Excise, WAPDA and FBR via fuzzy name/CNIC/address matching (SequenceMatcher + CNIC-prefix anchoring). Match confidences: {\"excise_LHR-2024-8810\": 1.0, \"wapda\": 1.0}"
      }
    ],
    "conf": {
      "EXCISE": 100,
      "WAPDA": 100,
      "FBR": 100
    }
  }
];
