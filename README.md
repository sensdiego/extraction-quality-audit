# Extraction Quality Audit

![Paper](https://img.shields.io/badge/paper-legal%20extraction%20audit-1f6feb)
![Sample](https://img.shields.io/badge/sample-100%20decisions-0a7ea4)
![Audit](https://img.shields.io/badge/audit-1%2C042%20items-6f42c1)
![Courts](https://img.shields.io/badge/courts-STJ%20%7C%20TJPR%20%7C%20TJSP%20%7C%20TRF4-2e8b57)
![License](https://img.shields.io/badge/license-CC--BY--4.0-8b0000)

The public data and analysis repository for the paper:

> **Not Hallucination but Granularity: Error Taxonomy and Quality Audit of
> LLM-Based Legal Information Extraction**
>
> Diego Sens (sens.legal, OAB/PR)

Language: [pt-BR](README.pt-BR.md) | `English`

## Repository Snapshot

| Field | Value |
|-------|-------|
| Scope | End-to-end expert audit of a production legal extraction pipeline |
| Audit sample | 100 Brazilian court decisions |
| Audited items | 1,042 |
| Courts | STJ, TJPR, TJSP, TRF4 |
| Core result | 96.0% precision with zero hallucinations in production models |
| Dominant error class | Granularity mismatch |

## Key Findings

- production extraction reached **96.0% precision**
- **zero hallucinations** were observed in the audited production sample
- granularity mismatch accounted for **31 of 42 errors** (3.0% of all items)
- LLM-as-judge agreement varied sharply by model, with Cohen's kappa ranging
  from **0.23 to 0.74**

## Repository Contents

| Asset | Description |
|-------|-------------|
| [`data/sample_ids.json`](data/sample_ids.json) | Identifiers for the 100 audited decisions |
| [`data/error_taxonomy.json`](data/error_taxonomy.json) | Seven-type error taxonomy |
| [`data/audit/`](data/audit/) | Expert audit files currently included in the repository |
| [`scripts/paper_stats.py`](scripts/paper_stats.py) | Statistics recomputation script |
| [`scripts/phase0_results.md`](scripts/phase0_results.md) | Supporting notes from the study workflow |
| [`LICENSE`](LICENSE) | Repository license (CC BY 4.0) |

## Data Availability

| Asset | Status | Notes |
|-------|--------|-------|
| Sample IDs (100 decisions) | Available | Tribunal + case number |
| Error taxonomy | Available | Seven-type classification |
| Expert audit files in `data/audit/` | Available | Current published audit material |
| Analysis script | Available | See note below on supplementary experiment inputs |
| Decision texts | Not included | Public judicial records |
| Extraction prompts | Not included | Proprietary |

## Recomputing Statistics

The main recomputation script is:

```bash
python scripts/paper_stats.py
```

Important note: the script expects supplementary experiment files under
`scripts/exp3_results/` and `scripts/controlled_extraction/`. If those assets
are not present in the local checkout, full recomputation will not run end to
end.

## Error Taxonomy

| Code | Error type | Definition |
|------|------------|------------|
| HAL | Hallucination | Extracted concept does not exist in the decision text |
| OMI | Omission | Concept exists but extraction is incomplete |
| GRA | Granularity mismatch | Concept at the wrong level of specificity |
| MIS | Misattribution | Attributed to the wrong party or court |
| ANC | Anchoring failure | Linked to the wrong legal provision |
| DUP | Duplication | Same concept extracted multiple times |
| TYP | Type error | Content placed in the wrong field |

## Citation

```bibtex
@article{sens2026granularity,
  author  = {Diego Sens},
  title   = {Not Hallucination but Granularity: Error Taxonomy and Quality Audit of {LLM}-Based Legal Information Extraction},
  year    = {2026},
  note    = {Preprint}
}
```

## License

This repository is released under [CC BY 4.0](LICENSE).
