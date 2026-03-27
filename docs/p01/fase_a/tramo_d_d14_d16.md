# P01 - Fase A - Tramo D (Día 14 al Día 16)

## Objetivo del tramo

Completar en un solo ciclo las tareas de:

- Día 14: `Implementar replay determinístico` + `Verificar consistencia del replay`.
- Día 15: `Configurar telemetría de crash/log` + `Validar formato unificado de logs`.
- Día 16: `Asegurar aislamiento y mínimo privilegio` + `Verificar controles de red/sandbox`.

Enfoque: `defensive-by-design`, sin PoC explotable, sin datos sensibles y sin pruebas en producción.

---

## Día 14 - Bloque 1: Implementar replay determinístico

### Implementación

1. Script: `scripts/p01_replay_deterministico.py`.
2. Entrada: directorio de fixtures JSON.
3. Salida: manifiesto determinístico con hash SHA-256 por fixture.
4. Orden: rutas ordenadas alfabéticamente para reproducibilidad.

### Resultado del bloque

1. Replay determinístico implementado.
2. Base lista para comparar consistencia entre corridas y versiones.

---

## Día 14 - Bloque 2: Verificar consistencia del replay

### Criterio de consistencia

1. Mismo conjunto de fixtures + misma versión de parser => mismo manifiesto.
2. Cambios de fixture => diff explícito en hash o metadatos.
3. Corridas repetidas no deben alterar orden ni contenido del manifiesto.

### Resultado del bloque

1. Modo `--verify` disponible en el script de replay.
2. Señal automática de drift en fixtures o procesamiento.

---

## Día 15 - Bloque 1: Configurar telemetría de crash/log

### Implementación

1. Esquema base: `infra/p01/formato_log_unificado.json`.
2. Campos obligatorios de trazabilidad y seguridad (run, stage, reason, action).
3. Campo `sanitized=true` para confirmar redacción.
4. Campo `details_hash` para correlación sin exponer contenido sensible.

### Resultado del bloque

1. Contrato mínimo de log unificado definido.

---

## Día 15 - Bloque 2: Validar formato unificado de logs

### Implementación

1. Script: `scripts/validar_logs_unificados_p01.py`.
2. Entrada: archivo JSONL.
3. Validación: campos requeridos, tipos, valores de enumeraciones críticas.
4. Salida: reporte de errores por línea + código de salida no cero si hay fallas.

### Resultado del bloque

1. Validación automática para estandarizar logs antes de análisis y scorecards.

---

## Día 16 - Bloque 1: Asegurar aislamiento y mínimo privilegio

### Controles definidos

1. No ejecutar como `root`.
2. Directorios de trabajo con permisos mínimos.
3. Separación de `tmp`, `logs`, `artifacts` y `results`.
4. Variables de entorno para modo de red aislado.

### Resultado del bloque

1. Script de verificación creado: `scripts/verificar_aislamiento_min_priv_p01.sh`.

---

## Día 16 - Bloque 2: Verificar controles de red/sandbox

### Validaciones incluidas

1. Presencia de `P01_NETWORK_MODE=isolated` en `.env`.
2. Permisos de directorios críticos (`tmp`, `logs`, `artifacts`).
3. Ausencia de world-writable en árbol del laboratorio.
4. Salida de auditoría con estado PASS/WARN/FAIL.

### Resultado del bloque

1. Checklist operativo para ejecución segura y repetible.

---

## Criterio de cierre del Tramo D

1. Replay determinístico implementado y verificable.
2. Formato unificado de logs definido.
3. Validador de logs operativo.
4. Verificador de aislamiento/mínimo privilegio operativo.
5. Flujo listo para baseline de Día 17-D18.

## Salida para el siguiente tramo

1. Día 17: baseline sin mutaciones.
2. Día 18: revisión de puerta de fase A y backlog técnico de fase B.
