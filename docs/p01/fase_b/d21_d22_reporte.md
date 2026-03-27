# P01 - Reporte D21-D22 (Fase B / Sección 1)

## Alcance ejecutado

- D21 Bloque 1: Construir corpus semilla inicial.
- D21 Bloque 2: Clasificar semillas por tipo.
- D22 Bloque 1: Normalizar corpus semilla.
- D22 Bloque 2: Eliminar duplicados de bajo valor.

## Artefactos generados

1. `scripts/fase_b/ejecutar_d21_d22.sh`
2. `artifacts/p01/fase_b/d21_d22/corpus/index_semillas.csv`
3. `artifacts/p01/fase_b/d21_d22/corpus/clasificacion_semillas.json`
4. `artifacts/p01/fase_b/d21_d22/corpus/normalizacion_reporte.json`
5. `infra/p01/fase_b/metricas_d21_d22.json`

## Resultado D21 (corpus + clasificación)

- Semillas totales: 15
- Semillas generadas por plantilla `mensajeria`: 10
- Distribución por `schema_version`: `actual_v2=11`, `legacy_v1=4`
- Tipos de mensaje cubiertos: 6 (`texto`, `enlace`, `adjunto_medio`, `reaccion`, `grupo_evento`, `control`)

## Resultado D22 (normalización + deduplicación)

- Entradas evaluadas: 15
- Entradas únicas tras normalización: 12
- Duplicados exactos removidos: 0
- Duplicados de bajo valor removidos: 3
- Reducción total de corpus: 20.0%

Muestras removidas por bajo valor:

1. `FX-SEED-MEDIA-002` (se conserva `FX-SEED-MEDIA-001`)
2. `FX-SEED-REA-002` (se conserva `FX-SEED-REA-001`)
3. `FX-SEED-TXT-002` (se conserva `FX-SEED-TXT-001`)

## Interpretación técnica

1. El corpus base dejó de ser mono-tipo y ahora cubre seis clases de entrada, mejorando la base para mutación D23-D24.
2. La deduplicación de bajo valor está activa y elimina ruido temprano sin perder variedad funcional.
3. La reducción del 20% mejora la relación señal/ruido para campañas posteriores y acelera triage.

## Próximo paso sugerido

- Ejecutar D23 y D24 (mutadores estructurales + semánticos) sobre `artifacts/p01/fase_b/d21_d22/corpus/normalized`.
