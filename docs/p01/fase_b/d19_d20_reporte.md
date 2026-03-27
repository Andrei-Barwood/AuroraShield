# P01 - Reporte D19-D20 (Fase B / Sección 1)

## Alcance ejecutado

- D19 Bloque 1: Crear harness inicial de parser.
- D19 Bloque 2: Integrar ejecución batch.
- D20 Bloque 1: Medir cobertura base.
- D20 Bloque 2: Definir métricas objetivo.

## Artefactos generados

1. `artifacts/p01/fase_b/d19_d20/batch_harness/d19-base/summary.json`
2. `artifacts/p01/fase_b/d19_d20/batch_harness/d19-legacy/summary.json`
3. `artifacts/p01/fase_b/d19_d20/batch_harness/d19-actual/summary.json`
4. `artifacts/p01/fase_b/d19_d20/batch_harness/d19-all/summary.json`
5. `artifacts/p01/fase_b/d19_d20/batch_harness/batch_resumen.json`
6. `infra/p01/fase_b/objetivos_metricas_d20.json`

## Resultado D19 (batch harness)

- Corridas ejecutadas: 4
- Fixtures procesados (agregado): 10
- `coverage_base_pct` ponderada: 18.75%
- `reject_rate_pct` agregada: 40.00%

Desglose por corrida:

| run_id | fixtures | accepts | degrades | rejects | coverage_base_pct |
|---|---:|---:|---:|---:|---:|
| d19-base | 2 | 1 | 1 | 0 | 12.50 |
| d19-legacy | 2 | 1 | 0 | 1 | 12.50 |
| d19-actual | 1 | 0 | 0 | 1 | 12.50 |
| d19-all | 5 | 2 | 1 | 2 | 25.00 |

## Resultado D20 (métricas objetivo)

Objetivos establecidos en `infra/p01/fase_b/objetivos_metricas_d20.json`:

1. Objetivo D24: `entrypoint_coverage_base_pct_min >= 60.0`
2. Objetivo D24: `reject_rate_pct` dentro de `[20.0, 70.0]`
3. Objetivo D34: `entrypoint_coverage_base_pct_min >= 95.0`
4. Objetivo D34: `dedup_precision_pct_min >= 90.0`
5. Objetivo D34: `repro_success_rate_pct_min >= 95.0`

## Interpretación técnica

1. La cobertura base actual (18.75%) confirma necesidad de ampliar corpus y clases de entrada en D21-D24.
2. La tasa de rechazo (40%) está dentro del rango objetivo D24, útil para etapa inicial de hardening.
3. La prioridad inmediata es aumentar diversidad de semillas y mejorar clasificación por tipo para elevar cobertura.

## Próximo paso sugerido

- Ejecutar D21 y D22 (corpus semilla + normalización/deduplicación) para empujar cobertura hacia objetivo D24.
