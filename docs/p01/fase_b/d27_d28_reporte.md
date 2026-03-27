# P01 - Reporte D27-D28 (Fase B / Sección 1)

## Alcance ejecutado

- D27 Bloque 1: Implementar deduplicación por firma.
- D27 Bloque 2: Validar clustering de crashes/fallas.
- D28 Bloque 1: Automatizar minimización de casos.
- D28 Bloque 2: Verificar reproducibilidad del mínimo.

## Artefactos generados

1. `scripts/fase_b/ejecutar_d27_d28.sh`
2. `scripts/fase_b/validar_d27_d28.py`
3. `artifacts/p01/fase_b/d27_d28/clusters/estructural.json`
4. `artifacts/p01/fase_b/d27_d28/clusters/semantico.json`
5. `artifacts/p01/fase_b/d27_d28/clusters/combinado.json`
6. `artifacts/p01/fase_b/d27_d28/minimize/*/reporte_minimizacion.json`
7. `artifacts/p01/fase_b/d27_d28/repro/*/run1/summary.json`
8. `artifacts/p01/fase_b/d27_d28/repro/*/run2/summary.json`
9. `infra/p01/fase_b/metricas_d27_d28.json`

## Resultado D27 (deduplicación)

- Contexto `estructural`: 48 fallas -> 4 clusters (reducción 91.67%).
- Contexto `semantico`: 24 fallas -> 2 clusters (reducción 91.67%).
- Contexto `combinado`: 72 fallas -> 6 clusters (reducción 91.67%).
- Top cluster combinado: 20 ocurrencias.

Estado D27: `deduplicacion_por_firma_validada=true`.

## Resultado D28 (minimización + reproducibilidad)

- Minimización por contexto: 12 casos mínimos (`estructural`, `semantico`, `combinado`).
- Total minimizados agregados: 36.
- Faltantes de fixture: 0 en todos los contextos.
- Reproducibilidad: 3/3 contextos deterministas (`repro_success_pct=100.0%`).

Resumen de repro (idéntico run1/run2 por contexto):

- `fixtures_total=12`, `accepts=5`, `degrades=4`, `rejects=3`, `coverage_base_pct=87.5`.

Estado D28:

- `minimizacion_automatica_activa=true`
- `reproducibilidad_verificada=true`

## Interpretación técnica

1. D27 consolidó la señal de fallas en un número pequeño y estable de firmas priorizables.
2. D28 dejó un flujo reproducible de minimización con fixtures mínimos separados de metadatos (`fixtures/`), evitando ruido operativo.
3. El tramo cumple criterios de calidad de ingeniería para continuar a D29 con base consistente.

## Próximo paso sugerido

- Ejecutar D29 (script de repro automático y estandarización de salida de repro).
