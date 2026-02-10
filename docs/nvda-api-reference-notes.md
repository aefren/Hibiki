# Notas de referencia de la API de NVDA para SoundNav

Hallazgos utiles extraidos de la documentacion oficial de NVDA 2025.3.2 y del changelog.
Este documento evita tener que volver a buscar en los docs extensos de NVDA.

---

## Speech module - Estructura

### Jerarquia de funciones de speech

```
speech.speak()                    <- re-export (modulo speech)
speech.speech.speak()             <- funcion real (modulo speech.speech)
  └── speakTextInfo()             <- usado por browse mode
        └── getTextInfoSpeech()   <- genera speech sequence (NVDA 2024.2+)
              ├── getPropertiesSpeech()
              ├── getControlFieldSpeech()
              ├── getFormatFieldSpeech()
              └── getTableInfoSpeech()
```

**Regla critica:** Siempre hookear `speech.speech.speak` (interno), NO `speech.speak` (re-export). El re-export no intercepta el speech real. Despues de hookear, actualizar tambien el re-export para compatibilidad:
```python
speech.speech.speak = mi_hook
speech.speak = speech.speech.speak
```

### Firma de getPropertiesSpeech

```python
def getPropertiesSpeech(reason=controlTypes.OutputReason.QUERY, **propertyValues):
```

- `reason` tiene valor por defecto `OutputReason.QUERY`
- Los demas argumentos son **keyword-only** via `**propertyValues`
- NO tiene `*args` (no acepta posicionales extra)
- Retorna `SpeechSequence` (lista de comandos de speech)
- Renombrada desde `getSpeechTextForProperties` en NVDA 2019.3 (issue #10098)

### Firma de speak

```python
def speak(speechSequence, ...)
```

- `speechSequence` es una lista que puede contener:
  - `str` - texto a hablar
  - `FieldCommand` - con atributos `.command` ("controlStart", "controlEnd") y `.field` (dict con "role", "states", etc.)
  - Otros comandos de speech (pausas, cambios de pitch, etc.)

---

## Extension points de speech

Disponibles en `speech.extensions` (NVDA 2025.3.2):

| Tipo | Nombre | Descripcion |
|------|--------|-------------|
| Action | `speechCanceled` | Triggered when speech is canceled |
| Action | `pre_speechCanceled` | Triggered before speech is canceled |
| Action | `pre_speech` | Triggered before NVDA handles prepared speech |
| Action | `post_speechPaused` | Triggered when speech is paused or resumed |
| Action | `pre_speechQueued` | Triggered after speech is processed and directly before it is enqueued |
| Filter | `filter_speechSequence` | Allows filtering speech sequence before it passes to synth driver |

**Limitacion encontrada:** `pre_speech` no se dispara de forma confiable para el speech generado por `speakTextInfo()` en modo exploracion. El monkey-patch de `speech.speech.speak` es mas confiable para interceptar TODO el speech.

---

## Browse mode (modo exploracion)

### Como funciona la navegacion

- El foco real queda en el documento (treeInterceptor)
- Las flechas y letras rapidas mueven el **cursor virtual** (caret), NO el foco real
- `event_gainFocus` NO se dispara al mover el cursor virtual
- `event_gainFocus` SI se dispara con Tab/Shift+Tab (mueven foco real)

### Flujo de navegacion con flechas

1. `treeInterceptor` script handler recibe el gesto (ej: flecha abajo)
2. Prepara el movimiento del caret
3. Genera speech via `speakTextInfo()` -> `getTextInfoSpeech()` -> `getPropertiesSpeech()`
4. Si el paso 3 lanza una excepcion no capturada, **el caret puede no moverse**
5. Llama a `speak()` con el speech sequence generado

### Speech sequence en browse mode

Cuando NVDA navega en browse mode, el `speechSequence` pasado a `speak()` contiene `FieldCommand` objects:

```python
[
    FieldCommand("controlStart", {"role": controlTypes.Role.LINK, "states": {...}, ...}),
    "texto del link",
    FieldCommand("controlEnd", None),
]
```

Para extraer el rol del elemento actual, buscar el `FieldCommand` mas interno con `command == "controlStart"` antes del primer texto.

### Letras rapidas de navegacion

- K: siguiente link
- B: siguiente boton
- H: siguiente heading
- T: siguiente tabla
- Shift+letra: anterior

Estas usan la misma pipeline de speech que las flechas.

---

## Cambio critico en NVDA 2024.2

Issue #12150: `speakTextInfo` ya no envia speech a traves de `speakWithoutPauses` si la razon es `SAYALL`. Las funciones de speech se dividieron en patron `speakX` + `getXSpeech`:

- `speakTextInfo` -> depende de `getTextInfoSpeech`
- Las funciones getter (`getPropertiesSpeech`, `getControlFieldSpeech`, etc.) son las que generan el speech sequence

---

## controlTypes - Compatibilidad de versiones

### Roles (NVDA 2019.3 - 2025+)

```python
# NVDA 2019.3-2020.4 (constantes)
controlTypes.ROLE_BUTTON
controlTypes.ROLE_LINK

# NVDA 2021.1+ (enums)
controlTypes.Role.BUTTON
controlTypes.Role.LINK
```

### States

```python
# NVDA 2019.3-2020.4
controlTypes.STATE_CHECKED

# NVDA 2021.1+
controlTypes.State.CHECKED
```

### OutputReason (NVDA 2019.3+)

```python
# Deprecado
controlTypes.REASON_FOCUS

# Actual
controlTypes.OutputReason.FOCUS
controlTypes.OutputReason.QUERY  # default para getPropertiesSpeech
```

---

## Roles de tabla disponibles

Los siguientes roles existen en NVDA para elementos de tabla:

- `controlTypes.Role.TABLE`
- `controlTypes.Role.TABLEROW`
- `controlTypes.Role.TABLECELL`
- `controlTypes.Role.TABLECOLUMNHEADER`
- `controlTypes.Role.TABLEROWHEADER`
- `controlTypes.Role.TABLEBODY`

Constantes legacy equivalentes: `ROLE_TABLE`, `ROLE_TABLEROW`, `ROLE_TABLECELL`, `ROLE_TABLECOLUMNHEADER`, `ROLE_TABLEROWHEADER`.

---

## Reglas criticas para hooks en NVDA

1. **Siempre llamar `nextHandler()`** en event handlers - si no, se rompe la cadena de eventos
2. **Nunca dejar escapar excepciones** de hooks o event handlers - envolver en try/except
3. **Restaurar funciones hookeadas** en `terminate()` - si no, NVDA queda en estado roto
4. **Hookear `speech.speech.*`** (modulo interno), no `speech.*` (re-export)
5. **Mantener la firma compatible** con la funcion original al hookear - especialmente valores por defecto de parametros
