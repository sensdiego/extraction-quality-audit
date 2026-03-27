# Phase 0 — Recomputed Statistics for Paper Revision

Date: 2026-03-25

## HAL Reclassification

Original summary (diego_audit_v2_all.json): STJ=5, TRF4=2, total=7
Actual items found in audit JSONs: STJ=3, TJSP=1, TRF4=0, total=4
**Summary file had incorrect counts.**

After Diego's reclassification decision:
- D8 STJ resultado=None → **OMI** (text says "negar provimento")
- D18 STJ resultado=None → **OMI** (text says "negou provimento")
- D29 STJ resultado=None → **OMI** (text says "negar provimento")
- D96 TJSP interpretacao Lei 11.419 from signature → **HAL** (kept)

**Final: 1 HAL + 3 OMI** (paper said "7 hallucinations")

## Kappa on Common Subset

| Judge | Full set n | Full κ | Common 308 κ |
|-------|-----------|--------|--------------|
| Kimi K2 | 308 | 0.7376 | 0.7376 |
| Llama 70B | 532 | 0.2313 | 0.1974 |

Kimi's 308 is a strict subset of Llama's 532.

## Bootstrap 95% CIs (n=2000)

| Judge | κ | 95% CI |
|-------|---|--------|
| Kimi K2 | 0.74 | [0.65, 0.81] |
| Llama 70B | 0.23 | [0.15, 0.31] |

CIs do not overlap → statistically significant difference.

## Fisher Exact Tests (Production vs Controlled)

| Tribunal | Prod err | Ctrl err | OR | p-value |
|----------|----------|----------|-----|---------|
| STJ | 9.3% | 22.1% | 2.76 | 0.005 |
| TJPR | 3.6% | 17.1% | 5.53 | <0.001 |
| TJSP | 0.6% | 6.0% | 10.54 | 0.004 |
| TRF4 | 1.7% | 6.9% | 4.19 | 0.078 |

3/4 significant. TRF4 trends same direction but ns (low counts).

## Kimi Paired Items

Paper says 409. Data: 411 items judged, 308 matched pairs for κ.
409 was likely 411 minus parse-excluded items, NOT the κ sample.
**Paper should report n=308 for κ computation.**

## CI Method

Not documented in code. Was computed ad-hoc. We'll state Clopper-Pearson going forward.
