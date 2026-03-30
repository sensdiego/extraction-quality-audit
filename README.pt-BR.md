# Extraction Quality Audit

![Paper](https://img.shields.io/badge/paper-auditoria%20de%20extracao%20juridica-1f6feb)
![Sample](https://img.shields.io/badge/amostra-100%20decisoes-0a7ea4)
![Audit](https://img.shields.io/badge/auditoria-1%2C042%20itens-6f42c1)
![Courts](https://img.shields.io/badge/tribunais-STJ%20%7C%20TJPR%20%7C%20TJSP%20%7C%20TRF4-2e8b57)
![License](https://img.shields.io/badge/licenca-CC--BY--4.0-8b0000)

O repositorio publico de dados e analise do paper:

> **Not Hallucination but Granularity: Error Taxonomy and Quality Audit of
> LLM-Based Legal Information Extraction**
>
> Diego Sens (sens.legal, OAB/PR)

Idioma: `pt-BR` | [English](README.md)

## Snapshot do Repositorio

| Campo | Valor |
|-------|-------|
| Escopo | Auditoria especialista ponta a ponta de um pipeline juridico de extracao em producao |
| Amostra auditada | 100 decisoes brasileiras |
| Itens auditados | 1.042 |
| Tribunais | STJ, TJPR, TJSP, TRF4 |
| Resultado central | 96,0% de precision com zero hallucinations em modelos de producao |
| Classe dominante de erro | Granularity mismatch |

## Achados Principais

- a extracao em producao atingiu **96,0% de precision**
- houve **zero hallucinations** na amostra auditada de producao
- granularity mismatch respondeu por **31 dos 42 erros** (3,0% de todos os itens)
- o desempenho de LLM-as-judge variou muito por modelo, com Cohen's kappa de
  **0,23 a 0,74**

## Conteudo do Repositorio

| Ativo | Descricao |
|-------|-----------|
| [`data/sample_ids.json`](data/sample_ids.json) | Identificadores das 100 decisoes auditadas |
| [`data/error_taxonomy.json`](data/error_taxonomy.json) | Taxonomia de erros em sete tipos |
| [`data/audit/`](data/audit/) | Arquivos de auditoria especialista atualmente publicados |
| [`scripts/paper_stats.py`](scripts/paper_stats.py) | Script de recomputacao estatistica |
| [`scripts/phase0_results.md`](scripts/phase0_results.md) | Notas de apoio do workflow do estudo |
| [`LICENSE`](LICENSE) | Licenca do repositorio (CC BY 4.0) |

## Disponibilidade dos Dados

| Ativo | Status | Observacoes |
|-------|--------|-------------|
| Sample IDs (100 decisoes) | Disponivel | Tribunal + numero do processo |
| Taxonomia de erros | Disponivel | Classificacao em sete tipos |
| Arquivos de auditoria em `data/audit/` | Disponivel | Material de auditoria atualmente publicado |
| Script de analise | Disponivel | Ver nota abaixo sobre insumos suplementares |
| Textos das decisoes | Nao incluidos | Registros judiciais publicos |
| Prompts de extracao | Nao incluidos | Proprietarios |

## Recomputando as Estatisticas

O script principal de recomputacao e:

```bash
python scripts/paper_stats.py
```

Nota importante: o script espera arquivos experimentais suplementares em
`scripts/exp3_results/` e `scripts/controlled_extraction/`. Se esses ativos
nao estiverem presentes no checkout local, a recomputacao completa nao roda de
ponta a ponta.

## Taxonomia de Erros

| Codigo | Tipo de erro | Definicao |
|--------|--------------|-----------|
| HAL | Hallucination | Conceito extraido nao existe no texto da decisao |
| OMI | Omission | O conceito existe, mas a extracao esta incompleta |
| GRA | Granularity mismatch | Conceito no nivel errado de especificidade |
| MIS | Misattribution | Atribuido a parte ou tribunal errado |
| ANC | Anchoring failure | Vinculado ao dispositivo legal errado |
| DUP | Duplication | Mesmo conceito extraido multiplas vezes |
| TYP | Type error | Conteudo colocado no campo errado |

## Citacao

```bibtex
@article{sens2026granularity,
  author  = {Diego Sens},
  title   = {Not Hallucination but Granularity: Error Taxonomy and Quality Audit of {LLM}-Based Legal Information Extraction},
  year    = {2026},
  note    = {Preprint}
}
```

## Licenca

Este repositorio esta publicado sob [CC BY 4.0](LICENSE).
