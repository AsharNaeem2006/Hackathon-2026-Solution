"""
TaxGraph AI — RPS Benchmark
==============================
Fires concurrent requests at the API and measures actual RPS.
Run AFTER starting the server:  python api.py

Usage:
    python benchmark_rps.py              # default: 200 requests, 20 concurrent
    python benchmark_rps.py 500 50       # 500 requests, 50 concurrent
"""

import asyncio
import time
import sys
import httpx

BASE_URL = "http://localhost:8000"

CNICS = [
    "35202-1111111-1",
    "35202-7777777-7",
    "35202-1010101-0",
    "35202-4444444-4",
    "35202-9999999-9",
    "35202-6666666-6",
]

ENDPOINTS = [
    "/",
    "/stats",
    "/entities?page=1&size=10",
    f"/entity/{CNICS[0]}/score",
    f"/entity/{CNICS[1]}/score",
    f"/entity/{CNICS[2]}",
    "/search?name=Ahmad",
    "/search?name=Tariq",
]


async def fire_request(client: httpx.AsyncClient, url: str, results: list):
    t0 = time.perf_counter()
    try:
        r = await client.get(url, timeout=5.0)
        elapsed = time.perf_counter() - t0
        results.append({"ok": r.status_code == 200, "ms": round(elapsed * 1000, 1)})
    except Exception as e:
        results.append({"ok": False, "ms": -1, "error": str(e)})


async def run_benchmark(total: int = 200, concurrency: int = 20):
    print(f"\n{'='*55}")
    print(f"  TaxGraph AI — RPS Benchmark")
    print(f"  Total requests : {total}")
    print(f"  Concurrency    : {concurrency}")
    print(f"  Target         : {BASE_URL}")
    print(f"{'='*55}\n")

    # Warm up
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        try:
            r = await client.get("/", timeout=3.0)
            entities = r.json().get("entities_loaded", "?")
            print(f"  Server OK — {entities} entities loaded\n")
        except Exception as e:
            print(f"  ERROR: Cannot reach server — {e}")
            print("  Start the server first:  python api.py\n")
            return

    results = []
    urls = [BASE_URL + ENDPOINTS[i % len(ENDPOINTS)] for i in range(total)]

    semaphore = asyncio.Semaphore(concurrency)

    async def bounded(client, url):
        async with semaphore:
            await fire_request(client, url, results)

    t_start = time.perf_counter()

    async with httpx.AsyncClient() as client:
        await asyncio.gather(*[bounded(client, url) for url in urls])

    elapsed = time.perf_counter() - t_start

    ok      = sum(1 for r in results if r["ok"])
    failed  = total - ok
    rps     = round(total / elapsed, 1)
    latencies = [r["ms"] for r in results if r["ms"] > 0]
    avg_ms  = round(sum(latencies) / len(latencies), 1) if latencies else 0
    p95_ms  = round(sorted(latencies)[int(len(latencies) * 0.95)], 1) if latencies else 0
    p99_ms  = round(sorted(latencies)[int(len(latencies) * 0.99)], 1) if latencies else 0

    print(f"  Results")
    print(f"  -------")
    print(f"  Total time      : {round(elapsed, 2)}s")
    print(f"  Successful      : {ok}/{total}")
    print(f"  Failed          : {failed}")
    print(f"  RPS (actual)    : {rps}")
    print(f"  Avg latency     : {avg_ms} ms")
    print(f"  p95 latency     : {p95_ms} ms")
    print(f"  p99 latency     : {p99_ms} ms")

    target_min, target_max = 10, 50
    if rps >= target_min:
        if rps >= target_max:
            print(f"\n  PASS — {rps} RPS exceeds the {target_max} RPS target")
        else:
            print(f"\n  PASS — {rps} RPS is within the {target_min}–{target_max} RPS target")
    else:
        print(f"\n  BELOW target — {rps} RPS (need {target_min}+). Check worker count.")

    print(f"{'='*55}\n")


if __name__ == "__main__":
    total       = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    concurrency = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    asyncio.run(run_benchmark(total, concurrency))
