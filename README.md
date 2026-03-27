# Extraction Quality Audit

Data and analysis scripts for the paper:

> **Not Hallucination but Granularity: Error Taxonomy and Quality Audit of LLM-Based Legal Information Extraction**
>
> Diego Sens (sens.legal, OAB/PR)

## Overview

End-to-end expert audit of a production multi-stage legal extraction pipeline, evaluating 1,042 items across 100 Brazilian court decisions from four tribunals (STJ, TJPR, TJSP, TRF4).

Key findings:
- 96.0% precision with zero hallucinations (production models)
- Dominant error: granularity mismatch (3.0%, 31/42 errors) — undetected by all verification methods tested
- LLM-as-judge performance varies dramatically by model (Cohen's κ from 0.23 to 0.74)

## Repository Structure

```
extraction-quality-audit/
├── README.md
├── data/
│   ├── sample_ids.json          # 100 decision identifiers (tribunal, case number)
│   ├── error_taxonomy.json      # 7-type error classification
│   └── audit/                   # Expert audit classifications (pending review)
├── scripts/
│   └── paper_stats.py           # Recomputation of all paper statistics (κ, Fisher, CIs)
└── LICENSE
```

## Data Availability

| Asset | Status | Notes |
|-------|--------|-------|
| Sample IDs (100 decisions) | Available | Tribunal + case number |
| Error taxonomy | Available | 7-type classification |
| Audit classifications | **Pending review** | To be included after final review |
| Analysis scripts | Available | Reproduces all paper statistics |
| Decision texts | Not included | Public judicial records (Lei 11.419/2006) |
| Extraction prompts | Not included | Proprietary |

## Error Taxonomy

| Code | Error Type | Definition |
|------|-----------|------------|
| HAL | Hallucination | Extracted concept does not exist in the decision text |
| OMI | Omission | Concept exists but extraction is incomplete |
| GRA | Granularity mismatch | Concept at wrong level of specificity |
| MIS | Misattribution | Attributed to wrong party or court |
| ANC | Anchoring failure | Linked to wrong legal provision |
| DUP | Duplication | Same concept extracted multiple times |
| TYP | Type error | Content placed in wrong field |

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

This dataset is released under CC-BY-4.0. See [LICENSE](LICENSE) for details.
