# P01 - Fase A - Tramo A (Día 3 al Día 7)

## Objetivo del tramo

Completar en un solo ciclo las tareas de:

- Día 3: `Mapear flujo no-click extremo a extremo` + `Identificar puntos de entrada de datos`.
- Día 4: `Mapear parser/protocolo por etapas` + `Documentar supuestos de formato`.
- Día 5: `Delimitar trust boundaries` + `Marcar cruces de privilegio`.
- Día 6: `Definir modelo de amenaza base` + `Definir supuestos operativos`.
- Día 7: `Crear catálogo de abuse cases` + `Crear catálogo de misuse cases`.

Enfoque: `defensive-by-design`, sin PoC explotable, sin datos sensibles, sin pruebas en producción.

---

## Día 3 - Bloque 1: Mapear flujo no-click extremo a extremo

### Flujo E2E (alto nivel)

```mermaid
flowchart LR
  A["Fuente Externa No-Confiable"] --> B["Edge Ingress"]
  B --> C["Normalización de Transporte"]
  C --> D["Cola de Ingesta"]
  D --> E["Parser de Mensajería"]
  E --> F["Validador de Esquema"]
  F --> G["Motor de Políticas"]
  G --> H["Procesamiento de Contenido Enriquecido"]
  H --> I["Renderer de Notificación"]
  I --> J["Proceso Privilegiado de Sistema"]
  J --> K["Telemetría y Auditoría"]
```

### Resultado esperado del bloque

1. Flujo no-click identificado de extremo a extremo.
2. Nodos críticos marcados para controles preventivos.
3. Trayectoria principal y trayectorias alternas documentadas.

---

## Día 3 - Bloque 2: Identificar puntos de entrada de datos

### Inventario de entradas (versión inicial)

| ID | Punto de entrada | Tipo | Riesgo defensivo | Control recomendado |
|---|---|---|---|---|
| EP-01 | Cabeceras de transporte | Metadatos | Alto | canonicalización + límites de tamaño |
| EP-02 | Cuerpo textual | Payload | Medio | validación de encoding + longitud |
| EP-03 | Descriptor de adjunto | Metadatos | Alto | validación estricta de tipo/estructura |
| EP-04 | Contenedor comprimido | Binario | Alto | descompresión segura y límites de recursión |
| EP-05 | Preview de URL | Contenido remoto | Alto | aislamiento de fetch y allowlist |
| EP-06 | Campos de internacionalización | Texto estructurado | Medio | normalización unicode y reglas de parsing |
| EP-07 | Campos multimedia embebidos | Binario | Alto | sandbox de decodificación |
| EP-08 | Parámetros de compatibilidad legado | Estructurado | Medio | parser estricto por versión |

### Resultado esperado del bloque

1. Entradas clasificadas y priorizadas.
2. Riesgo defensivo asociado por entrada.
3. Control mínimo definido por entrada.

---

## Día 4 - Bloque 1: Mapear parser/protocolo por etapas

### Pipeline del parser (modelo funcional)

1. `Stage-0 Ingreso`: recibe bytes del canal de transporte.
2. `Stage-1 Decoding`: transforma a representación canónica.
3. `Stage-2 Framing`: delimita unidades lógicas del mensaje.
4. `Stage-3 Parsing`: interpreta campos y subestructuras.
5. `Stage-4 Schema Validation`: valida presencia/tipo/rango.
6. `Stage-5 Semantic Validation`: valida reglas de negocio y contexto.
7. `Stage-6 Policy Gate`: decide permitir, degradar o rechazar.
8. `Stage-7 Safe Rendering`: genera salida segura para UI/notificación.

### Controles por etapa

- Rechazo temprano en Stage-1/2 para reducir superficie.
- Aislamiento de contenido complejo en Stage-6/7.
- Logging estructurado de errores con IDs no sensibles.

---

## Día 4 - Bloque 2: Documentar supuestos de formato

### Supuestos explícitos (baseline)

1. Todo payload se interpreta en UTF-8 o se rechaza.
2. Todo campo tiene límite máximo de longitud por perfil.
3. Estructuras anidadas tienen profundidad máxima fija.
4. No se permite ambigüedad de tipo para campos críticos.
5. Contenedores comprimidos tienen cota de expansión.
6. Versiones legacy se parsean en ruta separada y controlada.
7. Campos desconocidos se manejan bajo política `deny-by-default`.

### Resultado esperado del bloque

1. Supuestos de formato convertidos en reglas verificables.
2. Base lista para casos negativos de Día 8.

---

## Día 5 - Bloque 1: Delimitar trust boundaries

### Boundaries del sistema

| Boundary | Desde | Hacia | Naturaleza |
|---|---|---|---|
| TB-A | Red externa | Edge ingress | No confiable -> controlado |
| TB-B | Edge ingress | Cola interna | Zona de borde -> zona de procesamiento |
| TB-C | Cola interna | Parser | Datos no confiables -> lógica de interpretación |
| TB-D | Parser | Proceso privilegiado | Usuario/servicio -> privilegio elevado |
| TB-E | Proceso privilegiado | Persistencia/sistema | Privilegio alto -> activos críticos |
| TB-F | Sistema | Telemetría/repositorio | Entorno sensible -> material compartible |

### Resultado esperado del bloque

1. Boundaries definidos y numerados.
2. Puntos de control asignados por boundary.

---

## Día 5 - Bloque 2: Marcar cruces de privilegio

### Matriz de cruces

| Cruce | Origen | Destino | Riesgo | Mitigación principal |
|---|---|---|---|---|
| CP-01 | Ingreso no confiable | Parser | Alto | validación estricta + fail-close |
| CP-02 | Parser | Proceso privilegiado | Crítico | broker intermedio + policy gate |
| CP-03 | Renderer | Contexto de sistema | Alto | rendering seguro y sandbox |
| CP-04 | Proceso privilegiado | Persistencia sensible | Crítico | least privilege + control transaccional |

### Resultado esperado del bloque

1. Cruces críticos etiquetados.
2. Mitigación por cruce definida.

---

## Día 6 - Bloque 1: Definir modelo de amenaza base

### Actores

1. `A1 Externo remoto sin interacción del usuario`.
2. `A2 Emisor con capacidad de variar formato del mensaje`.
3. `A3 Actor que explota rutas legacy de parsing`.

### Objetivos de atacante (modelado defensivo)

1. Romper validaciones de formato.
2. Forzar transición no segura entre boundaries.
3. Elevar impacto desde fallo de parsing a contexto privilegiado.

### Amenazas priorizadas (STRIDE simplificado)

| ID | Categoría | Riesgo | Control base |
|---|---|---|---|
| TH-01 | Tampering de payload | Alto | canonicalización + checks estructurales |
| TH-02 | DoS por payload complejo | Alto | límites de tamaño/profundidad/tiempo |
| TH-03 | Elevación de privilegio por chain interna | Crítico | separación de privilegios + broker |
| TH-04 | Bypass de validación legacy | Alto | parser por versión + deny-by-default |
| TH-05 | Exposición de datos en telemetría | Medio | redacción y mínimo dato necesario |

---

## Día 6 - Bloque 2: Definir supuestos operativos

1. Laboratorio aislado y autorizado únicamente.
2. Telemetría estructurada con redacción automática.
3. Reproducciones siempre desde estado limpio.
4. Hallazgo no válido si no es reproducible.
5. Todo hallazgo debe terminar en test de regresión.
6. Priorización por reducción de riesgo sistémico.
7. Ningún experimento en producción.

### Resultado esperado del bloque

1. Supuestos operativos convertidos en guardrails de ejecución.

---

## Día 7 - Bloque 1: Catálogo de abuse cases (defensivo)

| ID | Abuse case | Señal observable | Mitigación |
|---|---|---|---|
| AB-01 | Mensaje con framing inconsistente | error de framing recurrente | parser estricto + rechazo temprano |
| AB-02 | Encodings mixtos malformados | fallas en decoding | canonicalización y fallback seguro |
| AB-03 | Adjuntos con metadatos ambiguos | discrepancia tipo real/declarado | validación tipo + sandbox |
| AB-04 | Payload con nesting excesivo | aumento latencia y memoria | límite de profundidad |
| AB-05 | Compresión expandible anómala | ratio expansión alto | límite de descompresión |
| AB-06 | Uso malicioso de rutas legacy | disparidad de parseo por versión | rutas legacy aisladas |
| AB-07 | Campos opcionales conflictivos | estados inválidos del parser | validación semántica |
| AB-08 | Secuencias de mensajes encadenadas | errores de estado | machine state hardening |

---

## Día 7 - Bloque 2: Catálogo de misuse cases (defensivo)

| ID | Misuse case | Riesgo | Prevención |
|---|---|---|---|
| MU-01 | Reusar parser sin límites en nuevo módulo | Alto | policy de parser común con guardrails |
| MU-02 | Habilitar compatibilidad legacy sin pruebas | Alto | gate de release con regresión obligatoria |
| MU-03 | Loggear payload crudo en producción | Alto | redacción + logging mínimo |
| MU-04 | Saltar validación semántica por performance | Crítico | presupuesto de performance con mínimos obligatorios |
| MU-05 | Promover proceso a privilegio alto por conveniencia | Crítico | modelo least privilege y revisión formal |
| MU-06 | Aceptar campos desconocidos silenciosamente | Alto | deny-by-default |
| MU-07 | Desactivar límites temporalmente sin rollback | Alto | feature flag con expiración y auditoría |
| MU-08 | Compartir artefactos sin sanitizar | Medio | pipeline de sanitización pre-publicación |

---

## Criterio de cierre del Tramo A

1. Flujo E2E no-click documentado.
2. Entradas de datos inventariadas y priorizadas.
3. Parser por etapas y supuestos de formato definidos.
4. Trust boundaries y cruces de privilegio documentados.
5. Threat model base y supuestos operativos aprobados.
6. Catálogo mínimo de abuse/misuse cases disponible.

## Salida para el siguiente tramo

1. Base lista para Día 8-D10 (casos negativos, data flow detallado y failure modes).
2. Entradas y boundaries listos para traducirse en tests defensivos.
