# P01 - Fase B - Sección 1 (Día 19 al Día 34)

## Alcance de la sección

Esta sección cubre los bloques:

- D19-D24: instrumentación base (harness, corpus, mutación).
- D25-D29: orquestación de campañas, fallas, deduplicación y repro.
- D30-D34: campañas largas y triage comparativo para hipótesis iniciales.

Enfoque: `defensive-by-design`.

## Mapeo día por día

| Día | Bloque 1 | Bloque 2 | Entregable operativo |
|---|---|---|---|
| 19 | Crear harness inicial de parser | Integrar ejecución batch | `p01_seccion1.py harness` |
| 20 | Medir cobertura base | Definir métricas objetivo | `p01_seccion1.py coverage` + KPIs |
| 21 | Construir corpus semilla inicial | Clasificar semillas por tipo | `p01_seccion1.py seed-corpus` |
| 22 | Normalizar corpus semilla | Eliminar duplicados de bajo valor | `p01_seccion1.py normalize-corpus` |
| 23 | Implementar mutadores estructurales | Validar mutaciones válidas | `p01_seccion1.py mutate-struct` |
| 24 | Implementar mutadores semánticos | Validar mutaciones inválidas útiles | `p01_seccion1.py mutate-semantic` |
| 25 | Definir scheduler de campañas | Configurar presupuesto por campaña | `p01_seccion1.py plan-campaign` |
| 26 | Integrar captura automática de fallas | Guardar artefactos por corrida | `p01_seccion1.py capture-failures` |
| 27 | Implementar deduplicación por firma | Validar clustering de crashes | `p01_seccion1.py dedup-signatures` |
| 28 | Automatizar minimización de casos | Verificar reproducibilidad del mínimo | `p01_seccion1.py minimize` |
| 29 | Generar script de repro automático | Estandarizar salida de repro | `p01_seccion1.py repro` |
| 30 | Ejecutar campaña larga #1 | Triage inicial de resultados | harness + capture + dedup + triage |
| 31 | Profundizar triage de clústeres críticos | Etiquetar severidad preliminar | `p01_seccion1.py triage` |
| 32 | Hipótesis de causa raíz preliminar | Priorizar top hallazgos | informe de hallazgos top |
| 33 | Ejecutar campaña larga #2 | Validar nuevos clústeres | corrida comparativa |
| 34 | Triage comparativo #1 vs #2 | Afinar reglas de deduplicación | informe comparativo |

## Comandos de referencia

```bash
# 1) Harness + cobertura
python3 scripts/fase_b/p01_seccion1.py harness --fixtures fixtures/p01 --out artifacts/p01/fase_b/seccion1/harness --run-id b1-d19
python3 scripts/fase_b/p01_seccion1.py coverage --summary artifacts/p01/fase_b/seccion1/harness/summary.json

# 2) Corpus y mutaciones
python3 scripts/fase_b/p01_seccion1.py seed-corpus --fixtures fixtures/p01 --out artifacts/p01/fase_b/seccion1/corpus --template-pack mensajeria
python3 scripts/fase_b/p01_seccion1.py normalize-corpus --corpus artifacts/p01/fase_b/seccion1/corpus --out artifacts/p01/fase_b/seccion1/corpus
./scripts/fase_b/ejecutar_d21_d22.sh
python3 scripts/fase_b/p01_seccion1.py mutate-struct --normalized artifacts/p01/fase_b/seccion1/corpus --out artifacts/p01/fase_b/seccion1/mutations
python3 scripts/fase_b/p01_seccion1.py mutate-semantic --normalized artifacts/p01/fase_b/seccion1/corpus --out artifacts/p01/fase_b/seccion1/mutations
./scripts/fase_b/ejecutar_d23_d24.sh

# 3) Campañas, fallas y triage
python3 scripts/fase_b/p01_seccion1.py plan-campaign --budget infra/p01/fase_b/presupuesto_campanas.json --out artifacts/p01/fase_b/seccion1/plan_campanas.json
python3 scripts/fase_b/p01_seccion1.py capture-failures --events artifacts/p01/fase_b/seccion1/harness/events.jsonl --out artifacts/p01/fase_b/seccion1/fallas
python3 scripts/fase_b/p01_seccion1.py dedup-signatures --failures artifacts/p01/fase_b/seccion1/fallas/fallas.jsonl --out artifacts/p01/fase_b/seccion1/clusters.json
python3 scripts/fase_b/p01_seccion1.py triage --clusters artifacts/p01/fase_b/seccion1/clusters.json --out artifacts/p01/fase_b/seccion1/triage_top.json
```

## Criterio de cierre de sección 1

1. Pipeline ejecutable extremo a extremo para D19-D34.
2. Dos campañas largas comparables (D30 y D33).
3. Clusters deduplicados y triage preliminar priorizado.
4. Hipótesis de causa raíz base listas para sección 2.
