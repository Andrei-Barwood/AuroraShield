# P01 - Fase A - Bloque 2

## Objetivo del bloque

Definir KPIs cuantitativos para guiar P01 en modo `defensive-by-design`, con métricas accionables de:

1. Seguridad por variante (`cadena corta -> user space privilegiado` y `cadena completa -> kernel`).
2. Reproducibilidad multi-versión.
3. Efectividad de mitigaciones.

## 1) KPIs de seguridad por variante

### 1.1 Variante A (cadena corta a user space privilegiado)

| KPI | Fórmula | Meta inicial | Fuente |
|---|---|---|---|
| `A1-EntryPointCoverage` | `entrypoints_probados / entrypoints_identificados * 100` | `>= 95%` | inventario + campañas |
| `A2-BoundaryRejectRate` | `malformed_rechazados_antes_limite_B / malformed_totales * 100` | `>= 98%` | logs de validación |
| `A3-PrivEscAttemptSuccess` | `intentos_esc_priv_exitosos / intentos_esc_priv_totales * 100` | `0%` | suite de abuso |
| `A4-CriticalCrashDensity` | `crashes_criticos / (casos_ejecutados / 1_000_000)` | `<= 1.0` | campañas fuzz |
| `A5-UnsafeTransitionCount` | `transiciones_no_controladas_a_proc_priv` | `0` | trazas de flujo |

### 1.2 Variante B (cadena completa a kernel)

| KPI | Fórmula | Meta inicial | Fuente |
|---|---|---|---|
| `B1-EntryPointCoverage` | `entrypoints_probados / entrypoints_identificados * 100` | `>= 95%` | inventario + campañas |
| `B2-KernelBoundaryBypassRate` | `bypass_limite_C_confirmados / intentos_bypass_limite_C * 100` | `0%` | trazas + pruebas controladas |
| `B3-CriticalCrashDensity` | `crashes_criticos / (casos_ejecutados / 1_000_000)` | `<= 0.5` | campañas fuzz |
| `B4-KernelPrimitiveSignals` | `senales_reg_rw_pc_kernel_confirmadas` | `0` en entorno mitigado | crash triage |
| `B5-UnsafeKernelPathCount` | `rutas_no_controladas_hacia_kernel` | `0` | modelado + tests |

## 2) KPIs de reproducibilidad

| KPI | Fórmula | Meta inicial | Fuente |
|---|---|---|---|
| `R1-ReproSuccessRate` | `repros_exitosos / repros_totales * 100` | `>= 95%` | reruns automatizados |
| `R2-MeanTimeToReproMin` | `sum(minutos_repro) / repros_exitosos` | `<= 20 min` | bitácora de corrida |
| `R3-CrossVersionConsistency` | `versiones_con_resultado_consistente / versiones_probadas * 100` | `>= 90%` | matriz multi-versión |
| `R4-DeterministicReplayRate` | `replays_deterministicos / replays_totales * 100` | `>= 95%` | replay harness |
| `R5-ArtifactCompleteness` | `corridas_con_artefactos_completos / corridas_totales * 100` | `100%` | checklist de artefactos |

## 3) KPIs de mitigación

| KPI | Fórmula | Meta inicial | Fuente |
|---|---|---|---|
| `M1-CriticalCrashReduction` | `(baseline_crash_crit - postmit_crash_crit) / baseline_crash_crit * 100` | `>= 90%` | comparación baseline/post |
| `M2-UnsafePathReduction` | `(baseline_rutas_no_controladas - postmit_rutas_no_controladas) / baseline_rutas_no_controladas * 100` | `100%` | modelado de flujo |
| `M3-RegressionPassRate` | `tests_regresion_ok / tests_regresion_totales * 100` | `100%` | CI local |
| `M4-SecurityTestGrowth` | `(tests_seg_actual - tests_seg_baseline) / tests_seg_baseline * 100` | `>= 30%` | inventario de tests |
| `M5-PerfOverheadP95` | `((latencia_p95_post - latencia_p95_base) / latencia_p95_base) * 100` | `<= 5%` | benchmark |

## 4) Criterios de aceptación de Bloque 2

1. Todas las métricas tienen fórmula inequívoca.
2. Todas tienen umbral meta inicial.
3. Todas tienen fuente de datos definida.
4. Existe plantilla de captura diaria para corridas.
5. Existe scorecard semanal para decisión de avance.

## 5) Cadencia de medición

1. Diaria: `A4`, `B3`, `R1`, `R4`, `R5`.
2. Semanal: `A1`, `B1`, `R3`, `M3`, `M4`.
3. Por hito (al cierre de fase): `M1`, `M2`, `M5`.

## 6) Modelo de score (priorización)

`ScoreGlobal = 0.45 * ScoreSeguridad + 0.30 * ScoreRepro + 0.25 * ScoreMitigacion`

Condiciones de avance a Bloque 3:

1. `ScoreSeguridad >= 80`.
2. `R1 >= 95%` y `R5 = 100%`.
3. Ningún KPI crítico en rojo 3 días consecutivos.

## 7) Semáforos

- Verde: cumple meta.
- Amarillo: desviación <= 10% de la meta.
- Rojo: desviación > 10% o incumplimiento de KPI crítico.

## 8) Notas defensive-by-design

1. Estas métricas miden reducción de riesgo y robustez, no capacidad de daño.
2. Se excluye cualquier indicador de explotación en producción.
3. Cualquier señal de primitive se usa sólo para confirmar cierre de superficie y convertirla en test de regresión.
