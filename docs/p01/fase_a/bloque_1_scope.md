# P01 - Fase A - Bloque 1

## 1. Propósito del bloque

Definir de forma verificable el alcance técnico y legal del laboratorio para ejecutar investigación `defensive-by-design` sobre superficie no-click de mensajería.

## 2. Alcance técnico (IN-SCOPE)

1. Modelado de entrada no-click en pipeline de mensajería dentro de laboratorio aislado.
2. Análisis de parser/protocolo usando fixtures sintéticos.
3. Instrumentación local de observabilidad (logs, traces, crash collection) en entorno controlado.
4. Diseño de mitigaciones preventivas y controles universales (validación, aislamiento, fail-safe, rate limiting).
5. Construcción de pruebas de regresión y reproducibilidad multi-versión en entornos autorizados.

## 3. Alcance técnico (OUT-OF-SCOPE)

1. Explotación en infraestructura productiva o cuentas de terceros.
2. Publicación de PoC weaponizable o cadenas de ataque operativas.
3. Exfiltración de datos reales o manipulación de activos fuera del laboratorio.
4. Actividades que degraden disponibilidad de servicios en producción.

## 4. Alcance legal y ético

1. Trabajo exclusivamente en entornos propios/autorizados.
2. Cumplimiento de políticas aplicables de divulgación responsable.
3. No uso de credenciales de terceros ni acceso no autorizado.
4. Redacción de evidencia sensible antes de cualquier publicación.
5. Separación estricta entre evidencia privada para vendor y contenido público safe.

## 5. Fronteras de confianza (Trust Boundaries)

1. Límite A: entrada de datos externos -> parser de mensajería.
2. Límite B: parser -> procesos privilegiados del sistema.
3. Límite C: proceso de usuario -> interfaces de mayor privilegio.
4. Límite D: telemetría y artefactos -> repositorio público (solo datos sanitizados).

## 6. Supuestos operativos

1. Todas las pruebas se ejecutan con reset de entorno y trazabilidad completa.
2. Cada hallazgo debe terminar en una mitigación, test y evidencia reproducible.
3. Se prioriza impacto defensivo medible por encima de demostraciones ofensivas.

## 7. Criterios de cierre de Bloque 1

1. Documento de alcance aprobado.
2. Lista IN-SCOPE/OUT-OF-SCOPE congelada para Fase A.
3. Reglas legales/éticas explícitas y verificables.
4. Trust boundaries documentadas.
5. Backlog inicial para Bloque 2 creado.

## 8. Backlog inicial para Bloque 2 (adelanto)

1. Definir métricas cuantitativas de seguridad por variante (cadena corta y cadena completa).
2. Definir KPI de reproducibilidad (tasa de repro, tiempo medio de repro, variación multi-versión).
3. Definir KPI de mitigación (reducción de superficie, reducción de crashes críticos, overhead máximo).
