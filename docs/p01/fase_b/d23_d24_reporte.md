# P01 - Reporte D23-D24 (Fase B / Sección 1)

## Alcance ejecutado

- D23 Bloque 1: Implementar mutadores estructurales.
- D23 Bloque 2: Validar mutaciones válidas.
- D24 Bloque 1: Implementar mutadores semánticos.
- D24 Bloque 2: Validar mutaciones inválidas útiles.

## Artefactos generados

1. `scripts/fase_b/ejecutar_d23_d24.sh`
2. `scripts/fase_b/validar_mutaciones_d23_d24.py`
3. `artifacts/p01/fase_b/d23_d24/mutations/manifest_estructural.json`
4. `artifacts/p01/fase_b/d23_d24/mutations/manifest_semantico.json`
5. `artifacts/p01/fase_b/d23_d24/harness/estructural/summary.json`
6. `artifacts/p01/fase_b/d23_d24/harness/semantico/summary.json`
7. `infra/p01/fase_b/metricas_d23_d24.json`

## Resultado D23 (estructural)

- Mutaciones estructurales generadas: 72
- Tipos de mutación estructural: 6
  - `remove_payload`, `payload_as_string`, `payload_null`, `remove_message_type`, `oversized_subject`, `payload_array_amplification`
- Parseabilidad de mutaciones: 100.0%
- Mutaciones con tag `_mutation`: 100.0%
- Resultado de harness: `reject_rate=66.67%`, `non_accept_rate=100.0%`
- Cobertura base en run estructural: 87.5%

Estado D23: `mutaciones_estructurales_validas=true`.

## Resultado D24 (semántico)

- Mutaciones semánticas generadas: 72
- Tipos de mutación semántica: 6
  - `unsupported_schema`, `invalid_expected_behavior`, `semantic_locale_out_of_profile`, `semantic_message_type_out_of_contract`, `semantic_timestamp_far_future`, `semantic_enum_out_of_profile`
- Parseabilidad de mutaciones: 100.0%
- Resultado de harness: `reject_rate=33.33%`, `non_accept_rate=100.0%`
- Cobertura base en run semántico: 100.0%

Estado D24: `mutaciones_semanticas_invalidas_utiles=true`.

## Gate D24 contra objetivo

- Objetivo D24 (`entrypoint_coverage_base_pct_min >= 60.0`): **cumplido**.
- Cobertura estructural: 87.5%
- Cobertura semántica: 100.0%

## Interpretación técnica

1. D23 quedó con mutadores estructurales robustos y verificables sin introducir material ofensivo.
2. D24 quedó con mutaciones semánticas útiles para rechazo/degradación controlada y para ampliar observabilidad.
3. Se cerró D19-D24 con artefactos reproducibles y métricas cuantitativas trazables.

## Próximo paso sugerido

- Ejecutar D25 y D26 (scheduler de campañas + captura automática de fallas por corrida).
