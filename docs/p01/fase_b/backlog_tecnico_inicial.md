# P01 - Backlog Técnico Inicial de Fase B

## Objetivo de Fase B

Incrementar cobertura, robustez de triage y capacidad de discovery continuo en modo `defensive-by-design`.

## Paquete P0 (arranque inmediato)

1. Construir harness extendido para parser por etapa (Stage-1 a Stage-7).
2. Integrar pipeline de deduplicación por firma de falla.
3. Implementar minimización automática de casos de entrada.
4. Automatizar generación diaria de `runs.csv` + scorecard semanal.
5. Expandir fixtures negativos desde 10 casos a mínimo 40 casos.

## Paquete P1 (siguiente iteración)

1. Mutadores estructurales por tipo de campo crítico.
2. Mutadores semánticos orientados a rutas legacy.
3. Pruebas diferenciales multi-versión con matriz `V1/V2/V3`.
4. Alertas automáticas sobre señales de observabilidad críticas.
5. Reporte comparativo semanal de drift en replay.

## Paquete P2 (optimización)

1. Mejorar rendimiento de campañas largas (batching y paralelización segura).
2. Normalizar taxonomía de causas raíz en triage.
3. Añadir métrica de costo computacional por campaña.
4. Plantilla de reporte técnico para transición a Fase C.

## Dependencias

1. Mantener actualizados fixtures por escenario.
2. Mantener contrato de log unificado compatible.
3. Mantener script de bootstrap como único entrypoint de laboratorio.

## Riesgos operativos

1. Sobreajuste a fixtures actuales y baja generalización.
2. Ruido de falsos positivos por mutaciones agresivas.
3. Degradación de reproducibilidad si no se congela entorno por corrida.

## Definición de listo para Fase C

1. Triage estable con deduplicación reproducible.
2. Cobertura de entradas críticas >= 95% sostenida.
3. Regresión automática activa para todos los hallazgos críticos.
4. Evidencia de reducción de riesgo en KPIs clave.
