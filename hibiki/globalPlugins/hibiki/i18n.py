from __future__ import annotations

from collections.abc import Callable
import builtins
import gettext
import os

import addonHandler
import languageHandler


def _normalize_lang(lang: str) -> str:
    return lang.replace("-", "_")


def init_translation() -> Callable[[str], str]:
    """
    Initialize translations for the add-on and return the gettext function.

    NVDA may provide language codes in BCP47 form (e.g., "es-ES").
    Python's gettext expects underscores (e.g., "es_ES"), so normalize.
    """
    addon = addonHandler.getCodeAddon(__file__)
    if addon is None:
        addonHandler.initTranslation()
        translator = builtins.__dict__.get("_")
        if callable(translator):
            return translator
        return lambda s: s

    lang = languageHandler.getLanguage() or ""
    lang = _normalize_lang(lang)

    languages = [lang] if lang else []
    if "_" in lang:
        base_lang = lang.split("_", 1)[0]
        if base_lang and base_lang not in languages:
            languages.append(base_lang)

    localedir = os.path.join(addon.path, "locale")
    translator = gettext.translation(
        addon.name,
        localedir=localedir,
        languages=languages or None,
        fallback=True,
    ).gettext

    builtins.__dict__["_"] = translator
    return translator
