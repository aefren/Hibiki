# Translation Guide for Hibiki

This guide explains how to translate Hibiki into other languages and how to maintain existing translations.

## For Translators

### Creating a New Translation

1. **Install Babel** (if not already installed):
   ```bash
   pip install Babel
   ```

2. **Initialize a new language catalog**:
   ```bash
   cd Hibiki
   pybabel init --input-file=Hibiki.pot --output-dir=locale --locale=<language_code> --domain=Hibiki
   ```

   Replace `<language_code>` with your language code (e.g., `fr` for French, `de` for German, `ja` for Japanese).

   Example for French:
   ```bash
   pybabel init --input-file=Hibiki.pot --output-dir=locale --locale=fr --domain=Hibiki
   ```

3. **Edit the .po file**:

   The command above creates a file at `locale/<language_code>/LC_MESSAGES/Hibiki.po`.

   Open this file with a translation editor:
   - **Poedit** (recommended): https://poedit.net/
   - **GTranslator**: For GNOME/Linux users
   - **Lokalize**: For KDE/Linux users
   - Or any text editor

   Translate the `msgstr` fields (leave `msgid` in English):
   ```po
   #: globalPlugins/Hibiki/settingsPanel.py:76
   msgid "&Enable Sound Navigation"
   msgstr "&Activer la Navigation Sonore"
   ```

4. **Test your translation**:
   ```bash
   # Compile the translation
   pybabel compile --directory=locale --domain=Hibiki

   # Build the add-on
   cd ..
   python build_addon.py
   ```

   Install the built `.nvda-addon` file in NVDA, change NVDA's language to your language, and test that the translations appear correctly.

5. **Submit your translation**:

   Create a pull request with your new `.po` file. The compiled `.mo` file will be generated automatically during the build process, so you don't need to include it.

### Updating an Existing Translation

If new strings have been added to the code, update your translation:

```bash
cd Hibiki

# Update the .po file with new strings
pybabel update --input-file=Hibiki.pot --output-dir=locale --domain=Hibiki

# Edit the updated .po file to translate new strings
# Look for entries with empty msgstr or marked as "fuzzy"

# Compile and test
pybabel compile --directory=locale --domain=Hibiki
```

## For Developers

### Marking Strings for Translation

In Python code, wrap translatable strings with `_()`:

```python
# Import at the top of the file (already done in Hibiki files)
import addonHandler
addonHandler.initTranslation()

# Then use _() to mark strings
message = _("Sound Navigation enabled")
label = _("&Enable Sound Navigation")
```

For strings with formatting:

```python
# Python brace format (preferred)
message = _("The file must be mono (1 channel). This file has {} channels.").format(num_channels)

# Or use python-brace-format marker in the .po file
```

### Extracting New Strings

After adding or modifying translatable strings in the code:

```bash
cd Hibiki

# Extract all translatable strings to the .pot template
pybabel extract --keywords=_ --output=Hibiki.pot --project=Hibiki --version=1.3.4 --msgid-bugs-address="https://github.com/Hibiki/Hibiki/issues" globalPlugins/Hibiki
```

Update the version number to match the current version in `manifest.ini`.

### Updating All Language Catalogs

After updating the `.pot` file:

```bash
# Update all existing .po files with new strings
pybabel update --input-file=Hibiki.pot --output-dir=locale --domain=Hibiki
```

This will:
- Add new untranslated strings to all `.po` files
- Mark outdated translations as "fuzzy" for review
- Preserve existing translations
- Update source code references

### Compiling Translation Catalogs

To manually compile `.po` files to `.mo` files:

```bash
# Compile all languages
pybabel compile --directory=locale --domain=Hibiki --statistics

# Compile a specific language
pybabel compile --input-file=locale/es/LC_MESSAGES/Hibiki.po --output-file=locale/es/LC_MESSAGES/Hibiki.mo
```

**Note**: The `build_addon.py` script automatically compiles all translations, so manual compilation is optional.

### Translation File Structure

```
Hibiki/
├── Hibiki.pot                          # Master translation template
└── locale/
    ├── es/                               # Spanish
    │   ├── manifest.ini                  # NVDA add-on metadata (translated)
    │   └── LC_MESSAGES/
    │       ├── Hibiki.po               # Spanish translations (source)
    │       └── Hibiki.mo               # Compiled binary (auto-generated)
    ├── fr/                               # French
    │   └── LC_MESSAGES/
    │       ├── Hibiki.po
    │       └── Hibiki.mo
    └── [other languages]/
```

## Common Language Codes

| Language | Code |
|---|---|
| Spanish | es |
| French | fr |
| German | de |
| Italian | it |
| Portuguese (Brazil) | pt_BR |
| Portuguese (Portugal) | pt_PT |
| Japanese | ja |
| Chinese (Simplified) | zh_CN |
| Chinese (Traditional) | zh_TW |
| Russian | ru |
| Polish | pl |
| Dutch | nl |
| Arabic | ar |
| Turkish | tr |

## Tools and Resources

### Required Tools

- **Babel**: Python internationalization library
  ```bash
  pip install Babel
  ```

### Recommended Translation Editors

- **Poedit**: https://poedit.net/ (Windows, macOS, Linux)
- **Lokalize**: https://apps.kde.org/lokalize/ (Linux)
- **GTranslator**: https://wiki.gnome.org/Apps/Gtranslator (Linux)

### Testing Translations in NVDA

1. Build the add-on: `python build_addon.py`
2. Install the `.nvda-addon` file in NVDA
3. Go to NVDA menu > Preferences > Settings > General
4. Change "Language" to your target language
5. Restart NVDA (NVDA+Q, then restart)
6. Open Sound Navigation settings (NVDA+N > Preferences > Settings > Sound Navigation)
7. Verify your translations appear correctly

**Fallback behavior**: If a string is not translated, NVDA will automatically display the English version.

## Translation Statistics

To see translation progress:

```bash
pybabel compile --directory=locale --domain=Hibiki --statistics
```

Output example:
```
9 of 80 messages (11%) translated in locale\es\LC_MESSAGES\Hibiki.po
```

## Translation Tips

1. **Keep keyboard shortcuts**: If a string contains `&` (keyboard shortcut marker), preserve it in the translation:
   - English: `"&Enable Sound Navigation"`
   - Spanish: `"&Habilitar Navegación con Sonidos"`

2. **Preserve placeholders**: If a string contains `{}`, `{0}`, etc., keep them in the same position:
   - English: `"This file has {} channels."`
   - Spanish: `"Este archivo tiene {} canales."`

3. **Context matters**: Read the translator comments (lines starting with `#:`) to understand where the string is used

4. **Test thoroughly**: Always test your translations in NVDA to ensure they fit in the UI and make sense in context

5. **NVDA terminology**: Follow NVDA's existing terminology in your language. Check NVDA's own translations for consistency.

## Questions or Issues?

If you have questions about translation or encounter issues:

1. Check existing translations: Look at `locale/es/LC_MESSAGES/Hibiki.po` as an example
2. Report issues: https://github.com/Hibiki/Hibiki/issues
3. Discuss on pull requests: Open a PR and ask questions there

Thank you for helping make Hibiki accessible to more users!
