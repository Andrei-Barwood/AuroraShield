# AuroraShield

Repositorio de trabajo `defensive-by-design` orientado al ecosistema Apple.

## Estado actual

- Nombre del proyecto: `AuroraShield`
- Proyecto activo: `P01 - No-click network attack (mensajería) hasta user space y kernel`
- Estado de fase: `Fase A cerrada` / `Fase B en ejecución`
- Sección activa de Fase B: `Sección 1 (D19-D34) con D19 a D26 completados`
- Baseline de referencia: `baseline-20260327T135640Z`

## Objetivo del repositorio

Construir mitigaciones y modelos de prevención reproducibles sin publicar material explotable.

## Estructura

- `docs/p01/fase_a/bloque_1_scope.md`: alcance técnico y legal de laboratorio.
- `docs/p01/fase_a/bloque_1_checklist.md`: checklist de cierre de Bloque 1.
- `docs/p01/fase_a/bloque_2_kpis.md`: definición de KPIs de seguridad, reproducibilidad y mitigación.
- `docs/p01/fase_a/bloque_2_checklist.md`: checklist de cierre de Bloque 2.
- `docs/p01/fase_a/tramo_a_d3_d7.md`: desarrollo integrado de Día 3 al Día 7.
- `docs/p01/fase_a/tramo_a_d3_d7_checklist.md`: checklist de cierre del Tramo A.
- `docs/p01/fase_a/tramo_b_d8_d10.md`: desarrollo integrado de Día 8 al Día 10.
- `docs/p01/fase_a/tramo_b_d8_d10_checklist.md`: checklist de cierre del Tramo B.
- `docs/p01/fase_a/tramo_c_d11_d13.md`: desarrollo integrado de Día 11 al Día 13.
- `docs/p01/fase_a/tramo_c_d11_d13_checklist.md`: checklist de cierre del Tramo C.
- `docs/p01/fase_a/tramo_d_d14_d16.md`: desarrollo integrado de Día 14 al Día 16.
- `docs/p01/fase_a/tramo_d_d14_d16_checklist.md`: checklist de cierre del Tramo D.
- `docs/p01/fase_a/tramo_e_d17_d18.md`: cierre operativo de Fase A (baseline y gate review).
- `docs/p01/fase_a/tramo_e_d17_d18_checklist.md`: checklist de cierre del Tramo E.
- `docs/p01/fase_a/revision_puerta_fase_a.md`: revisión de puerta para inicio de Fase B.
- `docs/p01/fase_b/backlog_tecnico_inicial.md`: backlog técnico inicial de Fase B.
- `docs/p01/fase_b/seccion_1_d19_d34.md`: guía operativa de Sección 1 de Fase B.
- `docs/p01/fase_b/seccion_1_d19_d34_checklist.md`: checklist de ejecución de Sección 1.
- `docs/p01/fase_b/d19_d20_reporte.md`: resultados ejecutados de D19 y D20.
- `docs/p01/fase_b/d21_d22_reporte.md`: resultados ejecutados de D21 y D22.
- `docs/p01/fase_b/d23_d24_reporte.md`: resultados ejecutados de D23 y D24.
- `docs/p01/fase_b/d25_d26_reporte.md`: resultados ejecutados de D25 y D26.
- `infra/p01/matriz_multiversion.csv`: baseline multi-versión.
- `infra/p01/matriz_compatibilidad.csv`: baseline de compatibilidad de fixtures.
- `infra/p01/formato_log_unificado.json`: contrato de telemetría/log unificado.
- `infra/p01/fase_b/presupuesto_campanas.json`: presupuesto base para campañas largas.
- `infra/p01/fase_b/objetivos_metricas_d20.json`: objetivos cuantitativos definidos en D20.
- `infra/p01/fase_b/metricas_d21_d22.json`: métricas consolidadas de D21-D22.
- `infra/p01/fase_b/metricas_d23_d24.json`: métricas consolidadas de D23-D24.
- `infra/p01/fase_b/metricas_d25_d26.json`: métricas consolidadas de D25-D26.
- `fixtures/p01/`: fixtures sintéticos base y por escenario.
- `scripts/bootstrap_p01_entorno.sh`: bootstrap idempotente del entorno aislado.
- `scripts/p01_replay_deterministico.py`: replay determinístico de fixtures.
- `scripts/validar_logs_unificados_p01.py`: validador de formato de logs JSONL.
- `scripts/verificar_aislamiento_min_priv_p01.sh`: verificador de aislamiento y mínimo privilegio.
- `scripts/ejecutar_baseline_p01.sh`: ejecución baseline D17 sin mutaciones.
- `scripts/fase_b/p01_seccion1.py`: CLI unificada para D19-D34 (harness, corpus, mutaciones, campañas, dedup y triage).
- `scripts/fase_b/ejecutar_batch_harness_d19.sh`: ejecución batch de harness para D19.
- `scripts/fase_b/medir_cobertura_d20.py`: análisis de cobertura base y objetivos D20.
- `scripts/fase_b/ejecutar_d21_d22.sh`: ejecución integrada de D21-D22 (seed + normalización).
- `scripts/fase_b/ejecutar_d23_d24.sh`: ejecución integrada de D23-D24 (mutación + validación).
- `scripts/fase_b/validar_mutaciones_d23_d24.py`: verificación de calidad/utilidad de mutaciones D23-D24.
- `scripts/fase_b/ejecutar_d25_d26.sh`: ejecución integrada de D25-D26 (scheduler + captura automática de fallas).
- `scripts/fase_b/validar_d25_d26.py`: validación de cierre para D25-D26.
- `docs/p01/fase_a/scorecard_semanal_template.md`: plantilla semanal para semáforos y decisiones.
- `metrics/p01/runs_template.csv`: plantilla CSV para registrar corridas y cálculo de KPIs.
- `metrics/p01/runs.csv`: registro real de corridas baseline.
- `scripts/p01_kpi_summary.py`: resumen rápido de KPIs sobre el último registro del CSV.
