# P01 - Reporte D25-D26 (Fase B / Sección 1)

## Alcance ejecutado

- D25 Bloque 1: Definir scheduler de campañas.
- D25 Bloque 2: Configurar presupuesto por campaña.
- D26 Bloque 1: Integrar captura automática de fallas.
- D26 Bloque 2: Guardar artefactos por corrida.

## Artefactos generados

1. `scripts/fase_b/ejecutar_d25_d26.sh`
2. `scripts/fase_b/validar_d25_d26.py`
3. `artifacts/p01/fase_b/d25_d26/plan_campanas.json`
4. `artifacts/p01/fase_b/d25_d26/fallas/estructural/fallas_resumen.json`
5. `artifacts/p01/fase_b/d25_d26/fallas/semantico/fallas_resumen.json`
6. `artifacts/p01/fase_b/d25_d26/fallas/estructural/artefactos_corrida.json`
7. `artifacts/p01/fase_b/d25_d26/fallas/semantico/artefactos_corrida.json`
8. `infra/p01/fase_b/metricas_d25_d26.json`

## Resultado D25 (scheduler + presupuesto)

- Campañas planificadas: 2
- Presupuesto total configurado: `1300` casos y `150` minutos
- `budget_ok_pct`: 100.0%
- `scheduler_ok_pct`: 100.0%
- `scheduler_global`: zona `America/Santiago`, ventana `06:00-23:00`, paralelismo `2`

Estado D25:

- `scheduler_definido=true`
- `presupuesto_por_campana_definido=true`

## Resultado D26 (captura automática + artefactos)

- Contextos de captura procesados: 2 (`estructural`, `semantico`)
- Eventos procesados: 144
- Fallas capturadas: 72
- Corridas detectadas: 2
- Archivos de artefacto contabilizados por validador: 6

Desglose por contexto:

- `estructural`: 72 eventos, 48 fallas, 1 corrida con bundle.
- `semantico`: 72 eventos, 24 fallas, 1 corrida con bundle.

Estado D26:

- `captura_automatica_integrada=true`
- `artefactos_por_corrida_guardados=true`

## Interpretación técnica

1. D25 dejó un plan de campañas operativo con scheduler y presupuesto explícitos por campaña.
2. D26 dejó la captura de fallas automatizada y trazable por corrida (`runs/<run_id>`), con bundles reproducibles.
3. El pipeline sigue en enfoque `defensive-by-design`, sin publicar material explotable.

## Próximo paso sugerido

- Ejecutar D27 y D28 (deduplicación por firma + minimización automática con reproducibilidad).
