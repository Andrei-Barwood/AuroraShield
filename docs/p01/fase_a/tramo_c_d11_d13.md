# P01 - Fase A - Tramo C (Día 11 al Día 13)

## Objetivo del tramo

Completar en un solo ciclo las tareas de:

- Día 11: `Definir matriz multi-versión` + `Definir matriz de compatibilidad`.
- Día 12: `Provisionar entorno aislado` + `Automatizar bootstrap del entorno`.
- Día 13: `Diseñar fixtures sintéticos base` + `Versionar fixtures por escenario`.

Enfoque: `defensive-by-design`, sin PoC explotable, sin datos sensibles y sin pruebas en producción.

---

## Día 11 - Bloque 1: Definir matriz multi-versión

### Variables de control por versión

1. Sistema operativo y build.
2. Ruta de parser activa (legacy/moderna).
3. Política de rechazo temprano habilitada.
4. Señales de observabilidad disponibles.
5. Resultado esperado para casos negativos clave.

### Resultado del bloque

1. Matriz multi-versión creada en `infra/p01/matriz_multiversion.csv`.
2. Criterio uniforme para comparar resultados entre versiones.

---

## Día 11 - Bloque 2: Definir matriz de compatibilidad

### Ejes de compatibilidad

1. Versión de entrada de mensaje vs versión del parser.
2. Tipo de payload vs política de validación.
3. Ruta legacy vs ruta moderna.
4. Comportamiento esperado: aceptar, degradar, rechazar.

### Resultado del bloque

1. Matriz de compatibilidad creada en `infra/p01/matriz_compatibilidad.csv`.
2. Criterios explícitos para detectar divergencias funcionales y de seguridad.

---

## Día 12 - Bloque 1: Provisionar entorno aislado

### Requisitos del entorno

1. Separación de datos de trabajo (`artifacts`, `logs`, `tmp`).
2. Ejecución local reproducible sin dependencias productivas.
3. Configuración de umask segura y permisos mínimos.
4. Carpeta de fixtures de solo lectura para corridas estándar.

### Resultado del bloque

1. Estructura base de laboratorio lista para corridas repetibles.
2. Convención de rutas y artefactos establecida.

---

## Día 12 - Bloque 2: Automatizar bootstrap del entorno

### Alcance del bootstrap

1. Crear estructura de carpetas estándar de P01.
2. Validar dependencias mínimas (`bash`, `python3`, `git`).
3. Generar archivo `.env.example` no sensible.
4. Crear script idempotente para inicialización local.

### Resultado del bloque

1. Script `scripts/bootstrap_p01_entorno.sh` creado.
2. Bootstrap repetible y seguro para iniciar laboratorio en minutos.

---

## Día 13 - Bloque 1: Diseñar fixtures sintéticos base

### Principios de diseño de fixtures

1. Datos sintéticos sin información real.
2. Cobertura de entradas mínimas válidas.
3. Cobertura de casos estructuralmente límite.
4. Formato estable para reproducibilidad.

### Resultado del bloque

1. Fixtures base creados en `fixtures/p01/base/`.
2. Nomenclatura consistente para evolución posterior.

---

## Día 13 - Bloque 2: Versionar fixtures por escenario

### Estrategia de versionado

1. Separar por escenario (`legacy_v1`, `actual_v2`, etc.).
2. Mantener equivalencia semántica entre escenarios cuando aplique.
3. Registrar diferencias intencionales en metadatos del fixture.
4. Preparar base para pruebas diferenciales multi-versión.

### Resultado del bloque

1. Fixtures versionados por escenario en `fixtures/p01/escenarios/`.
2. Base lista para validación de compatibilidad y regresión.

---

## Criterio de cierre del Tramo C

1. Matriz multi-versión definida.
2. Matriz de compatibilidad definida.
3. Entorno aislado provisionado.
4. Bootstrap automatizado e idempotente.
5. Fixtures base diseñados.
6. Fixtures versionados por escenario.

## Salida para el siguiente tramo

1. Base lista para Día 14-16 (replay, telemetría y aislamiento reforzado).
2. Insumos listos para ejecutar baseline con y sin mutaciones en fases posteriores.
