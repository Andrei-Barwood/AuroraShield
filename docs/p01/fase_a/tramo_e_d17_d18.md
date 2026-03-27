# P01 - Fase A - Tramo E (Día 17 y Día 18)

## Objetivo del tramo

Completar el cierre de Fase A:

- Día 17: `Ejecutar baseline sin mutaciones` + `Registrar baseline de estabilidad`.
- Día 18: `Revisión de puerta de fase A` + `Ajustar backlog técnico de fase B`.

Enfoque: `defensive-by-design`, sin PoC explotable, sin datos sensibles y sin pruebas en producción.

---

## Día 17 - Bloque 1: Ejecutar baseline sin mutaciones

### Implementación

1. Script operativo: `scripts/ejecutar_baseline_p01.sh`.
2. Genera manifiesto de replay determinístico.
3. Valida logs unificados en JSONL.
4. Verifica aislamiento y mínimo privilegio.

### Resultado del bloque

1. Baseline ejecutado de forma reproducible.
2. Evidencia técnica generada en `artifacts/p01/baseline/<run_id>/`.

---

## Día 17 - Bloque 2: Registrar baseline de estabilidad

### Implementación

1. Registro automático de la corrida en `metrics/p01/runs.csv`.
2. Captura de métricas mínimas de estabilidad y reproducibilidad.
3. Resumen consultable con `scripts/p01_kpi_summary.py`.

### Resultado del bloque

1. Baseline de estabilidad registrado y versionado.

---

## Día 18 - Bloque 1: Revisión de puerta de fase A

### Criterios de revisión

1. Entregables de D1-D18 completos.
2. Replay determinístico y validación de logs operativos.
3. Guardrails de aislamiento activos.
4. Baseline inicial ejecutado y trazable.

### Resultado del bloque

1. Documento de revisión de puerta: `docs/p01/fase_a/revision_puerta_fase_a.md`.

---

## Día 18 - Bloque 2: Ajustar backlog técnico de fase B

### Alcance

1. Priorizar trabajo de instrumentación y discovery de Fase B.
2. Definir paquetes de ejecución por prioridad (P0/P1/P2).
3. Declarar dependencias y riesgos operativos.

### Resultado del bloque

1. Backlog técnico inicial de Fase B: `docs/p01/fase_b/backlog_tecnico_inicial.md`.

---

## Criterio de cierre del Tramo E

1. Baseline sin mutaciones ejecutado.
2. Baseline de estabilidad registrado en `metrics/p01/runs.csv`.
3. Revisión de puerta de Fase A completada.
4. Backlog técnico de Fase B definido.

## Salida para la siguiente fase

1. Fase A cerrada.
2. Inicio de Fase B con prioridades operativas y métricas base.
