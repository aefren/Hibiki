# Changelog - hibiki

Todas las versiones notables de este proyecto serán documentadas en este archivo.

## [0.9.2] - 2026-07-20

### Fixed
- **Quick navigation sound lag (b/shift+b, h, k, etc.)**: 3D sounds during browse-mode quick navigation now play at the position of the control being announced instead of the previously focused control. NVDA's `_quickNavScript` calls `item.report()` before `item.moveTo()` (NVDA issue #8831), so the virtual caret was still on the old control when Hibiki read its position — every sound landed one step behind. Sounds are now positioned via the control field's own `controlIdentifier_docHandle`/`controlIdentifier_ID` (resolved through `getNVDAObjectFromIdentifier`), falling back to the text range currently being spoken, then to the caret only as a last resort.
- **Shared-line controls all sounding at the same spot**: Multiple controls on one line (e.g. several links in a sentence) previously all played at the position of the first object on that line. Resolving each control field by its own identifier fixes this too.
- **Over-eager role/state label suppression**: "Suppress spoken role labels" and "Suppress spoken state labels" now only hide labels that Hibiki actually has a sound for. Roles without a mapped sound (dialog, grouping, window, ...) and states without one (unavailable, read only, required, ...) are spoken normally again instead of being silently dropped.
- **Label suppression respects the browse mode sounds switch**: with "Play sounds during browse mode navigation" turned off, role and state labels are spoken again in browse mode instead of being hidden with no sound to replace them. Focus-mode suppression is unaffected by that switch.

## [0.9.1] - 2026-02-22

### Fixed
- **Import safety**: The add-on no longer crashes on load if the installed NVDA version does not define one of the listed role constants. Role mappings are now built entry by entry, skipping unknown roles.
- **Table sounds**: Tables, table rows, table cells, and table headers now play distinct sounds (`snd2.wav`, `snd11.wav`, `snd12.wav`, `snd13.wav`). These control types are also available for customization in the sound settings dialog.
- **Thread safety**: The sound cache is now protected with a `threading.Lock` to prevent race conditions when custom sounds are lazily loaded from concurrent speech hooks.
- **Settings panel deduplication**: The Hibiki panel is no longer registered twice in NVDA's settings dialog if the add-on reloads without a clean `terminate()`.
- **Null desktop guard**: `play_for_object()` now returns early if `api.getDesktopObject()` returns `None`, preventing an unhandled `AttributeError` during NVDA startup.
- **Dead code removed**: Removed unused `SetItemData` call in the sound customization dialog.
- **Typos**: Fixed three instances of `Hibikiadd-on` → `Hibiki add-on` in `__init__.py`.

## [0.9] - 2026-02-22

### Agregado
- **Sonidos por nivel de encabezado**: Cada nivel de encabezado (H1–H6) reproduce un sonido distinto (`h1.wav`–`h6.wav`) en lugar del sonido genérico `heading.wav`.
- **Personalización por nivel**: El diálogo de personalización de sonidos ahora lista "Heading Level 1" a "Heading Level 6" individualmente, permitiendo asignar sonidos personalizados a cada nivel.

### Técnico
- `_ROLE_DEFINITIONS` ahora asigna `HEADING1`–`HEADING6` a claves de control separadas (`heading1`–`heading6`) en vez de una sola clave `heading`.
- `get_sounds_for_object()` detecta el atributo `level` en el rol genérico `HEADING` (NVDA moderno) y lo convierte a int para resolver el sonido correcto. Esto cubre tanto modo foco (level como int) como modo browse (level como string en attrs del buffer virtual).
- Eliminada la entrada genérica `'heading'` del diálogo de personalización.

## [1.3.4] - 2026-02-10

### Corregido
- **Sonidos fantasmas eliminados**: Los sonidos ahora solo se reproducen cuando NVDA anuncia un control, no en eventos de voz no relacionados (como F12 para leer la hora).
- **Sincronización perfecta**: Los sonidos se reproducen exactamente al mismo tiempo que el anuncio del control, sin retraso.
- **Navegación con flechas**: Corregido el problema donde los sonidos se reproducían con retraso al navegar con flechas arriba/abajo o teclas rápidas (k, b, e) en modo browse.

### Técnico
- Reemplazado hook reactivo en `speech.speak()` con hooks proactivos en:
  - `speech.getObjectPropertiesSpeech` (navegación con Tab/foco)
  - `speech.getControlFieldSpeech` (navegación en modo browse)
- Eliminado parche a `SpeechWithoutPausesInstance`
- Eliminada lógica de deduplicación basada en ubicación (ya innecesaria)
- Reducido código de 381 a 304 líneas

## [1.3.2] - Versión anterior
- Implementación base con sonidos 3D
- Supresión de etiquetas de rol/estado
- Soporte para 40+ tipos de control

---

**Nota**: Este CHANGELOG documenta cambios desde la versión 1.3.2. Para historial completo, ver commits de Git.
