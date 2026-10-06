"""Generate the extract probe document and gold records (deterministic, seed 7)."""

import json
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
rng = random.Random(7)

CITIES = ["Lisbon", "Porto", "Madrid", "Seville", "Valencia", "Lyon", "Nantes", "Ghent",
          "Utrecht", "Bremen", "Leipzig", "Turin", "Bologna", "Krakow", "Brno", "Graz"]
CARRIERS = {"dhl": ["DHL", "DHL Express", "dhl"], "ups": ["UPS", "ups"],
            "fedex": ["FedEx", "FedEx Ground", "fedex"], "dpd": ["DPD", "dpd"]}
NOISE = [
    "{ts} DEBUG heartbeat worker=w{n} ok",
    "{ts} INFO  queue depth={n}",
    "{ts} WARN  label printer p{n} low on paper",
    "{ts} INFO  sync inventory batch={n} rows=0",
    "{ts} DEBUG gc pause {n}ms",
]


def ts(day, h, m, s):
    return f"2026-09-{day:02d}T{h:02d}:{m:02d}:{s:02d}Z"


gold = []
lines = [
    "Dispatch office log export -- week of 2026-09-14",
    "Prepared by night shift. Mixed sources: the dispatcher daemon log, the shift notes,",
    "and the manual table kept on the whiteboard. Only shipments that physically left the",
    "dock count as dispatched. Planned or voided shipments do not count.",
    "",
    "== daemon log ==",
]

rid = 1001
day = 14
records = []
for i in range(40):
    if i and i % 4 == 0:
        day += 1
    carrier = rng.choice(sorted(CARRIERS))
    raw_carrier = rng.choice(CARRIERS[carrier])
    w = round(rng.uniform(0.4, 48.0), rng.choice([1, 2]))
    city = rng.choice(CITIES)
    records.append({"id": f"SHP-{rid}", "date": f"2026-09-{day:02d}", "carrier": carrier,
                    "weight_kg": w, "dest": city, "_raw_carrier": raw_carrier, "_day": day})
    rid += 1

# Tricky: one large legacy weight.
records[37]["weight_kg"] = 1250.5
fmt_of = {}
for i, r in enumerate(records):
    fmt_of[i] = "log" if i < 18 else ("prose" if i < 30 else ("table" if i < 36 else "legacy"))

noise_i = 0


def noise(day):
    global noise_i
    noise_i += 1
    t = rng.choice(NOISE)
    return t.format(ts=ts(day, rng.randrange(0, 23), rng.randrange(60), rng.randrange(60)), n=rng.randrange(1, 99))


def log_line(r, retransmit=False):
    w = f"{r['weight_kg']}kg"
    tail = " (retransmit)" if retransmit else ""
    return (f"{ts(r['_day'], rng.randrange(6, 20), rng.randrange(60), rng.randrange(60))} INFO  dispatch "
            f"id={r['id']} carrier={r['_raw_carrier']} wt={w} dest=\"{r['dest']}\"{tail}")


retransmit_line = None
for i in range(18):
    r = records[i]
    for _ in range(rng.choice([1, 2, 3])):
        lines.append(noise(r["_day"]))
    if i == 9:
        # Tricky formatting: wrapped log line.
        full = log_line(r)
        cut = full.index(" carrier=")
        lines.append(full[:cut] + " \\")
        lines.append("      " + full[cut + 1:])
    else:
        line = log_line(r)
        lines.append(line)
        if i == 4:
            retransmit_line = line + " (retransmit)"
    if i == 12:
        lines.append(retransmit_line)  # Decoy 1: retransmitted duplicate.
    if i == 15:
        # Decoy 2: dispatched-looking line later voided.
        lines.append(f"{ts(r['_day'], 21, 4, 9)} INFO  dispatch id=SHP-1077 carrier=DPD wt=6.6kg dest=\"Ghent\"")
        lines.append(f"{ts(r['_day'], 21, 30, 0)} WARN  dispatch id=SHP-1077 VOIDED before pickup; parcel never left the dock")

lines += ["", "== shift notes =="]
for i in range(18, 30):
    r = records[i]
    style = i % 3
    if style == 0:
        lines.append(f"- {r['id']} went out with {r['_raw_carrier']} to {r['dest']} on {r['date']}, {r['weight_kg']} kg.")
    elif style == 1:
        lines.append(f"- {r['date']}: handed {r['id']} ({r['weight_kg']} kg, destination {r['dest']}) to the {r['_raw_carrier']} driver.")
    else:
        lines.append(f"- Dispatched {r['id']} on {r['date']} -> {r['dest']}. Carrier: {r['_raw_carrier']}. Weight {r['weight_kg']} kg.")
    if i == 22:
        lines.append("- Customer in Lyon called about late delivery; told them we would check tomorrow.")
    if i == 25:
        # Decoy 3: planned, not dispatched.
        lines.append(f"- Planned for next week: SHP-1098 via DHL to Lyon, about 9.5 kg. Not booked yet.")
    if i == 27:
        lines.append("- Reminder: re-tape pallets before the afternoon pickup.")

lines += ["", "== whiteboard table ==", "| id | date | carrier | weight | destination |", "|---|---|---|---|---|"]
for i in range(30, 36):
    r = records[i]
    lines.append(f"| {r['id']} | {r['date']} | {r['_raw_carrier']} | {r['weight_kg']} kg | {r['dest']} |")

lines += ["", "== legacy terminal (dates in this section are DD/MM/YYYY) =="]
for i in range(36, 40):
    r = records[i]
    d = r["date"]
    legacy_date = f"{d[8:10]}/{d[5:7]}/{d[0:4]}"
    w = f"{r['weight_kg']:,}" if r["weight_kg"] >= 1000 else f"{r['weight_kg']}"
    lines.append(f"DSP {legacy_date} {r['id']} {r['_raw_carrier'].upper():<12} {w:>9} KG  TO {r['dest'].upper()}")
    lines.append(noise(r["_day"]))

lines += ["", "end of export"]

# Pad with noise to ~150 lines, inserted only inside the daemon log section.
log_end = lines.index("== shift notes ==")
while len(lines) < 150:
    pos = rng.randrange(7, log_end - 1)
    lines.insert(pos, noise(14 + rng.randrange(0, 9)))
    log_end += 1

os.makedirs(os.path.join(HERE, "workspace"), exist_ok=True)
with open(os.path.join(HERE, "workspace", "dispatch_log.txt"), "w") as f:
    f.write("\n".join(lines) + "\n")
gold = [{k: v for k, v in r.items() if not k.startswith("_")} for r in records]
with open(os.path.join(HERE, "gold", "records.json"), "w") as f:
    json.dump(gold, f, indent=1)
print(len(lines), "lines;", len(gold), "gold records")
