"""Paper revision statistics — Tasks 1-5.

Computes:
  Task 1: Llama κ on 308-item common subset
  Task 2: Bootstrap 95% CIs for both κ values
  Task 3: Fisher exact tests for controlled experiment
  Task 4: CI method audit (reported inline)
  Task 5: Kimi 409 vs 308 analysis
"""

import json
import numpy as np
from pathlib import Path
from collections import defaultdict
from scipy.stats import fisher_exact

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
EXP3 = Path(__file__).parent / "exp3_results"
KIMI_AGR = EXP3 / "agreement_kimi-k2.json"
LLAMA_AGR = EXP3 / "agreement_llama70b.json"
KIMI_JUDGE = EXP3 / "judge_kimi-k2.json"
LLAMA_JUDGE = EXP3 / "judge_llama70b.json"
CONTROLLED = Path(__file__).parent / "controlled_extraction" / "diego_audit_v2_all.json"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def cohens_kappa_full(pairs):
    """Cohen's κ with full taxonomy."""
    n = len(pairs)
    if n == 0:
        return float('nan')
    agree = sum(1 for j, h in pairs if j == h)
    codes = sorted(set(j for j, _ in pairs) | set(h for _, h in pairs))
    p_o = agree / n
    p_e = sum(
        (sum(1 for j, _ in pairs if j == c) / n) *
        (sum(1 for _, h in pairs if h == c) / n)
        for c in codes
    )
    if p_e >= 1:
        return 1.0
    return (p_o - p_e) / (1 - p_e)


def cohens_kappa_binary(pairs):
    """Cohen's κ binary (OK vs error)."""
    n = len(pairs)
    if n == 0:
        return float('nan')
    agree = sum(1 for j, h in pairs if (j == "OK") == (h == "OK"))
    j_ok = sum(1 for j, _ in pairs if j == "OK")
    h_ok = sum(1 for _, h in pairs if h == "OK")
    p_o = agree / n
    p_e = (j_ok / n) * (h_ok / n) + ((n - j_ok) / n) * ((n - h_ok) / n)
    if p_e >= 1:
        return 1.0
    return (p_o - p_e) / (1 - p_e)


def extract_pairs(agreement_json):
    """Extract (judge, human) pairs from agreement details."""
    return [(d["judge"], d["human"]) for d in agreement_json["details"]]


# ---------------------------------------------------------------------------
# Task 1: Llama κ on 308-item common subset
# ---------------------------------------------------------------------------
print("=" * 70)
print("TASK 1: Llama κ on 308-item common subset")
print("=" * 70)

kimi_agr = json.loads(KIMI_AGR.read_text())
llama_agr = json.loads(LLAMA_AGR.read_text())

# Build key sets from details
kimi_keys = {(d["decision"], d["field"], d["idx"]) for d in kimi_agr["details"]}
llama_keys = {(d["decision"], d["field"], d["idx"]) for d in llama_agr["details"]}

common_keys = kimi_keys & llama_keys
print(f"Kimi items:  {len(kimi_keys)}")
print(f"Llama items: {len(llama_keys)}")
print(f"Common keys: {len(common_keys)}")

# Build lookup for Llama on common subset
llama_lookup = {(d["decision"], d["field"], d["idx"]): (d["judge"], d["human"])
                for d in llama_agr["details"]}

llama_common_pairs = [llama_lookup[k] for k in common_keys if k in llama_lookup]
kimi_lookup = {(d["decision"], d["field"], d["idx"]): (d["judge"], d["human"])
               for d in kimi_agr["details"]}
kimi_common_pairs = [kimi_lookup[k] for k in common_keys if k in kimi_lookup]

llama_kappa_common = cohens_kappa_full(llama_common_pairs)
llama_kappa_common_bin = cohens_kappa_binary(llama_common_pairs)
kimi_kappa_common = cohens_kappa_full(kimi_common_pairs)

llama_agree_common = sum(1 for j, h in llama_common_pairs if j == h) / len(llama_common_pairs)

print(f"\nLlama κ (full) on common {len(llama_common_pairs)} items: {llama_kappa_common:.4f}")
print(f"Llama κ (binary) on common {len(llama_common_pairs)} items: {llama_kappa_common_bin:.4f}")
print(f"Llama agreement on common subset: {llama_agree_common:.4f}")
print(f"Kimi κ (full) on common {len(kimi_common_pairs)} items: {kimi_kappa_common:.4f}")
print(f"\nFor reference — full sets:")
print(f"  Kimi κ (full, n=308): {kimi_agr['kappa_full']}")
print(f"  Llama κ (full, n=532): {llama_agr['kappa_full']}")


# ---------------------------------------------------------------------------
# Task 2: Bootstrap 95% CIs for both κ values
# ---------------------------------------------------------------------------
print("\n" + "=" * 70)
print("TASK 2: Bootstrap 95% CIs for κ (n_boot=2000)")
print("=" * 70)

np.random.seed(42)
N_BOOT = 2000

# Kimi: use full 308 pairs
kimi_pairs = extract_pairs(kimi_agr)
llama_pairs = extract_pairs(llama_agr)

def bootstrap_kappa(pairs, n_boot=2000, kappa_fn=cohens_kappa_full):
    """Bootstrap κ values."""
    n = len(pairs)
    kappas = np.empty(n_boot)
    pairs_arr = list(pairs)
    for b in range(n_boot):
        idxs = np.random.randint(0, n, size=n)
        sample = [pairs_arr[i] for i in idxs]
        kappas[b] = kappa_fn(sample)
    return kappas

# Kimi (n=308)
kimi_boots = bootstrap_kappa(kimi_pairs, N_BOOT)
kimi_ci = (np.percentile(kimi_boots, 2.5), np.percentile(kimi_boots, 97.5))
print(f"\nKimi κ (full, n={len(kimi_pairs)}):")
print(f"  Point estimate: {cohens_kappa_full(kimi_pairs):.4f}")
print(f"  Bootstrap 95% CI: [{kimi_ci[0]:.4f}, {kimi_ci[1]:.4f}]")
print(f"  Bootstrap mean: {np.mean(kimi_boots):.4f}, std: {np.std(kimi_boots):.4f}")

# Llama (n=532)
llama_boots = bootstrap_kappa(llama_pairs, N_BOOT)
llama_ci = (np.percentile(llama_boots, 2.5), np.percentile(llama_boots, 97.5))
print(f"\nLlama κ (full, n={len(llama_pairs)}):")
print(f"  Point estimate: {cohens_kappa_full(llama_pairs):.4f}")
print(f"  Bootstrap 95% CI: [{llama_ci[0]:.4f}, {llama_ci[1]:.4f}]")
print(f"  Bootstrap mean: {np.mean(llama_boots):.4f}, std: {np.std(llama_boots):.4f}")

# Also do binary kappa CIs
kimi_boots_bin = bootstrap_kappa(kimi_pairs, N_BOOT, cohens_kappa_binary)
kimi_ci_bin = (np.percentile(kimi_boots_bin, 2.5), np.percentile(kimi_boots_bin, 97.5))
llama_boots_bin = bootstrap_kappa(llama_pairs, N_BOOT, cohens_kappa_binary)
llama_ci_bin = (np.percentile(llama_boots_bin, 2.5), np.percentile(llama_boots_bin, 97.5))
print(f"\nBinary κ CIs:")
print(f"  Kimi (binary):  [{kimi_ci_bin[0]:.4f}, {kimi_ci_bin[1]:.4f}]")
print(f"  Llama (binary): [{llama_ci_bin[0]:.4f}, {llama_ci_bin[1]:.4f}]")


# ---------------------------------------------------------------------------
# Task 3: Fisher exact tests — controlled vs production
# ---------------------------------------------------------------------------
print("\n" + "=" * 70)
print("TASK 3: Fisher exact tests — controlled vs production")
print("=" * 70)

controlled = json.loads(CONTROLLED.read_text())

# Production data from paper
production = {
    "STJ":  {"items": 290, "errors": 27},
    "TJPR": {"items": 306, "errors": 11},
    "TJSP": {"items": 331, "errors": 2},
    "TRF4": {"items": 115, "errors": 2},
}

for tribunal in ["STJ", "TJPR", "TJSP", "TRF4"]:
    prod = production[tribunal]
    ctrl = controlled["by_tribunal"][tribunal]

    prod_correct = prod["items"] - prod["errors"]
    prod_err = prod["errors"]
    ctrl_correct = ctrl["items"] - ctrl["errors"]
    ctrl_err = ctrl["errors"]

    # 2x2 table: [[prod_correct, prod_errors], [ctrl_correct, ctrl_errors]]
    table = [[prod_correct, prod_err], [ctrl_correct, ctrl_err]]
    odds_ratio, p_value = fisher_exact(table)

    prod_rate = prod["errors"] / prod["items"] * 100
    ctrl_rate = ctrl["errors"] / ctrl["items"] * 100

    print(f"\n{tribunal}:")
    print(f"  Production: {prod['items']} items, {prod['errors']} errors ({prod_rate:.1f}%)")
    print(f"  Controlled: {ctrl['items']} items, {ctrl['errors']} errors ({ctrl_rate:.1f}%)")
    print(f"  Table: {table}")
    print(f"  OR = {odds_ratio:.4f}, p = {p_value:.6f}", end="")
    if p_value < 0.001:
        print(" ***")
    elif p_value < 0.01:
        print(" **")
    elif p_value < 0.05:
        print(" *")
    else:
        print(" (ns)")


# ---------------------------------------------------------------------------
# Task 5: Kimi 409 vs 308 analysis
# ---------------------------------------------------------------------------
print("\n" + "=" * 70)
print("TASK 5: Kimi 409 vs 308 analysis")
print("=" * 70)

kimi_judge = json.loads(KIMI_JUDGE.read_text())
llama_judge = json.loads(LLAMA_JUDGE.read_text())

# Count total items produced by each judge
kimi_total_judge_items = 0
kimi_total_expected_items = 0
kimi_decisions_with_items = 0
for r in kimi_judge["results"]:
    if not r.get("skipped") and not r.get("error"):
        n_judge = len(r.get("judge_items", []))
        n_expected = r.get("n_items", 0)
        kimi_total_judge_items += n_judge
        kimi_total_expected_items += n_expected
        if n_judge > 0:
            kimi_decisions_with_items += 1

llama_total_judge_items = 0
llama_total_expected_items = 0
for r in llama_judge["results"]:
    if not r.get("skipped") and not r.get("error"):
        llama_total_judge_items += len(r.get("judge_items", []))
        llama_total_expected_items += r.get("n_items", 0)

print(f"\nKimi judge file:")
print(f"  Total judge items produced (parsed):  {kimi_total_judge_items}")
print(f"  Total expected items (from sample):   {kimi_total_expected_items}")
print(f"  Decisions with items:                 {kimi_decisions_with_items}")
print(f"  Calibration decisions (D1-D5):        {kimi_judge['calibration_decisions']}")
print(f"  Eval decisions (D6-D100):             {kimi_judge['eval_decisions']}")
print(f"  Decisions skipped:                    {sum(1 for r in kimi_judge['results'] if r.get('skipped'))}")

print(f"\nLlama judge file:")
print(f"  Total judge items produced (parsed):  {llama_total_judge_items}")
print(f"  Total expected items (from sample):   {llama_total_expected_items}")

print(f"\nAgreement files:")
print(f"  Kimi n_matched (agreement JSON):  {kimi_agr['n_matched']}")
print(f"  Llama n_matched (agreement JSON): {llama_agr['n_matched']}")

# The matching requires same (decision, field, idx) key in BOTH judge output AND human audit
# Kimi parsed 411 items but only 308 matched the human audit keys
# Paper says 409 — investigate:
# Check how many unique items Kimi produced that have valid field assignments
kimi_items_with_field = 0
kimi_items_without_field = 0
for r in kimi_judge["results"]:
    if not r.get("skipped") and not r.get("error"):
        for ji in r.get("judge_items", []):
            if ji.get("field"):
                kimi_items_with_field += 1
            else:
                kimi_items_without_field += 1

print(f"\n  Kimi items with field assigned:    {kimi_items_with_field}")
print(f"  Kimi items without field:          {kimi_items_without_field}")

# Check: how many of the 411 Kimi items DON'T match human audit keys?
# Reconstruct the matching logic from compute_agreement
# We need the human audit items too — they're embedded in the agreement details indirectly
# Actually, the agreement was computed by the script. Let's just count mismatches.
kimi_all_keys = set()
from collections import Counter
field_counter = defaultdict(lambda: defaultdict(int))
for r in kimi_judge["results"]:
    if not r.get("skipped") and not r.get("error"):
        dec_num = r["decision_num"]
        field_counts = defaultdict(int)
        for ji in r.get("judge_items", []):
            field = ji.get("field", "unknown")
            field_counts[field] += 1
            idx = field_counts[field]
            kimi_all_keys.add((dec_num, field, idx))

print(f"\n  Kimi unique (dec, field, idx) keys: {len(kimi_all_keys)}")
print(f"  Kimi keys in agreement:             {len(kimi_keys)}")
print(f"  Kimi keys NOT in agreement:         {len(kimi_all_keys - kimi_keys)}")

# Explanation
print(f"""
EXPLANATION:
- Kimi parsed 411 items across 91 eval decisions (4 skipped for 0 items).
- The compute_agreement function matches items by (decision_num, field, idx) key.
- Only items where BOTH the judge AND the human audit have the SAME key get paired.
- Result: 308 matched pairs → n_matched = 308, κ = 0.7376.
- The paper's "409 paired items" appears to be the total Kimi judge output items
  (411, or ~409 if 2 were excluded/filtered). This is NOT the number of matched
  pairs for κ computation — it's the total items Kimi evaluated.
- The 411→409 difference of 2 items may be from items missing a field assignment
  or post-hoc filtering.
- Bottom line: κ = 0.7376 was computed on 308 actually-matched pairs, not 409.
  The paper should report n=308 for Kimi (or clarify "409" means total items judged
  vs 308 matched pairs for κ).
""")

# Summary
print("=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"""
TASK 1 — Llama κ on common subset:
  Llama κ_full on {len(llama_common_pairs)} common items: {llama_kappa_common:.4f}
  Llama κ_binary on {len(llama_common_pairs)} common items: {llama_kappa_common_bin:.4f}
  Llama agreement on common subset: {llama_agree_common:.4f}
  (vs Llama κ_full on full 532: {llama_agr['kappa_full']})
  Kimi κ_full on same {len(kimi_common_pairs)} items: {kimi_kappa_common:.4f} (same as full, since Kimi only has 308)

TASK 2 — Bootstrap 95% CIs:
  Kimi κ_full (n=308):   [{kimi_ci[0]:.4f}, {kimi_ci[1]:.4f}]
  Llama κ_full (n=532):  [{llama_ci[0]:.4f}, {llama_ci[1]:.4f}]
  Kimi κ_binary (n=308): [{kimi_ci_bin[0]:.4f}, {kimi_ci_bin[1]:.4f}]
  Llama κ_binary (n=532):[{llama_ci_bin[0]:.4f}, {llama_ci_bin[1]:.4f}]

TASK 3 — Fisher exact tests (production vs controlled):""")
for tribunal in ["STJ", "TJPR", "TJSP", "TRF4"]:
    prod = production[tribunal]
    ctrl = controlled["by_tribunal"][tribunal]
    table = [[prod["items"] - prod["errors"], prod["errors"]],
             [ctrl["items"] - ctrl["errors"], ctrl["errors"]]]
    _, p = fisher_exact(table)
    print(f"  {tribunal}: p = {p:.6f}")

print(f"""
TASK 4 — CI method:
  No Python scripts in the experiment directory use Clopper-Pearson, Wilson,
  or any explicit binomial CI function. The CIs mentioned in the paper drafts
  (e.g., "95% CI [54.8%, 83.3%]") appear in markdown text only — likely computed
  ad-hoc or in a prior session. No scipy.stats.proportion_confint or equivalent
  found in any .py file.

TASK 5 — Kimi 409 vs 308:
  - Kimi judge produced {kimi_total_judge_items} items total.
  - Agreement computation matched 308 items by (decision, field, idx) key.
  - Paper says "409 paired items" — this reflects total Kimi judge output
    (≈411), NOT the 308 actually matched for κ computation.
  - κ = 0.7376 is based on n=308 matched pairs.
""")
