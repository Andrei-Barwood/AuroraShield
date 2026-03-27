# AuroraShield

Repositorio de trabajo `defensive-by-design` orientado al ecosistema Apple.

## Estado actual

- Nombre del proyecto: `AuroraShield`
- Proyecto activo: `P01 - No-click network attack (mensajería) hasta user space y kernel`
- Fase activa: `Fase A`
- Último hito completado: `Tramo D (Día 14 al Día 16)`
- Próximo hito sugerido: `Cierre de Fase A (Día 17 y Día 18)`

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
- `infra/p01/matriz_multiversion.csv`: baseline multi-versión.
- `infra/p01/matriz_compatibilidad.csv`: baseline de compatibilidad de fixtures.
- `infra/p01/formato_log_unificado.json`: contrato de telemetría/log unificado.
- `fixtures/p01/`: fixtures sintéticos base y por escenario.
- `scripts/bootstrap_p01_entorno.sh`: bootstrap idempotente del entorno aislado.
- `scripts/p01_replay_deterministico.py`: replay determinístico de fixtures.
- `scripts/validar_logs_unificados_p01.py`: validador de formato de logs JSONL.
- `scripts/verificar_aislamiento_min_priv_p01.sh`: verificador de aislamiento y mínimo privilegio.
- `docs/p01/fase_a/scorecard_semanal_template.md`: plantilla semanal para semáforos y decisiones.
- `metrics/p01/runs_template.csv`: plantilla CSV para registrar corridas y cálculo de KPIs.
- `scripts/p01_kpi_summary.py`: resumen rápido de KPIs sobre el último registro del CSV.
