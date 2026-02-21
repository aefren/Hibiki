# Hibiki Add-on - Developer Notes

## Quick Start for Developers

### Project Structure
```
hibiki/
├── hibiki/                          # Add-on source
│   ├── manifest.ini                   # Add-on metadata
│   ├── readme.html                    # User documentation
│   ├── globalPlugins/hibiki/        # Main plugin code
│   │   ├── __init__.py               # Global plugin entry point
│   │   ├── roleMapper.py             # Role→sound mappings
│   │   ├── soundPlayer.py            # 3D audio playback
│   │   ├── settingsPanel.py          # GUI configuration
│   │   ├── camlorn_audio/            # 3D audio library
│   │   └── sounds/                   # WAV sound files
│   ├── doc/en/                       # Documentation
│   └── locale/es/LC_MESSAGES/        # Translations
├── hibiki-1.0.0.nvda-addon         # Distribution package
├── TESTING_GUIDE.md                  # Testing procedures
├── IMPLEMENTATION_SUMMARY.md         # Implementation details
└── DEVELOPER_NOTES.md                # This file
```

## Making Changes

### Modifying Role Mappings

**File**: `hibiki/globalPlugins/hibiki/roleMapper.py`

Role and state mappings are defined in `_ROLE_DEFINITIONS` and `_STATE_DEFINITIONS` dicts. Each entry is `'ROLE_NAME': ('sound_file.wav', 'control_key')`. The `ROLE_SOUND_MAP` and `ROLE_TO_CONTROL_KEY` dicts are auto-generated from these.

To add a new role mapping:
```python
_ROLE_DEFINITIONS = {
    # ... existing mappings ...
    'NEW_ROLE': ('new_sound.wav', 'newrole'),
}
```

1. Add the sound file to `sounds/` directory
2. Add the entry to `_ROLE_DEFINITIONS` in `roleMapper.py`
3. Add display name in `soundCustomizationDialog.py` `CONTROL_DISPLAY_NAMES` and default in `DEFAULT_SOUNDS`
4. Repackage the add-on
5. Test in NVDA

#### Heading Level Sounds

Heading levels use a two-layer mapping:
- **Old NVDA**: `HEADING1`–`HEADING6` roles map directly to `h1.wav`–`h6.wav` via `_ROLE_DEFINITIONS` with control keys `'heading1'`–`'heading6'`.
- **Modern NVDA**: A generic `HEADING` role with a `level` attribute. `get_sounds_for_object()` detects the level (int or string) and dynamically resolves the control key (`'heading1'`–`'heading6'`) and sound file (`h1.wav`–`h6.wav`).

### Adding Configuration Options

**File**: `hibiki/globalPlugins/hibiki/settingsPanel.py`

1. Update `init_configuration()` with new config spec:
```python
confspec = {
    "enabled": "boolean(default=True)",
    "suppressRoleLabels": "boolean(default=True)",
    "newOption": "boolean(default=False)",  # New option
}
```

2. Add GUI control in `makeSettings()`:
```python
self.newOptionCheckbox = sHelper.addItem(
    wx.CheckBox(self, label=_("&New Option"))
)
self.newOptionCheckbox.SetValue(get_config("newOption"))
```

3. Update `onSave()`:
```python
set_config("newOption", self.newOptionCheckbox.GetValue())
```

### Modifying Sound Playback

**File**: `hibiki/globalPlugins/hibiki/soundPlayer.py`

To change audio positioning:
```python
# Current values
AUDIO_WIDTH = 25.0  # Left-right spread
AUDIO_DEPTH = 5.0   # Distance from listener

# Modify these constants to change spatial characteristics
```

To add reverb or effects:
```python
# Reference: Unspoken __init__.py lines 85-90
# The camlorn_audio library supports reverb effects
```

### Adding Event Handlers

**File**: `hibiki/globalPlugins/hibiki/__init__.py`

To handle additional events:
```python
def event_newEvent(self, obj, nextHandler):
    """Handle new event type."""
    if self.is_enabled():
        self.play_for_object(obj)
    nextHandler()  # ALWAYS call this!
```

## Debugging

### Enable NVDA Logging

1. NVDA menu (NVDA+N)
2. Tools > View log
3. Add debug statements in code:
```python
import log
log.debug(f"Hibiki: Playing sound for {obj.role}")
```

### Common Issues

**Import Errors**:
- Check that camlorn_audio DLLs are in the correct location
- Verify Python 3.7+ compatibility (NVDA 2021.1+ uses Python 3.7)

**Sound Not Playing**:
- Add logging in `SoundPlayer.play_for_object()`
- Check if sound files are loading in `__init__()`
- Verify `init_camlorn_audio()` succeeds

**Speech Hook Not Working**:
- Verify hook is registered in `__init__()`
- Check that original function is saved
- Add logging in hook function

**Configuration Not Saving**:
- Check config spec is registered
- Verify `onSave()` is called
- Check NVDA config file permissions

## Repackaging After Changes

### Manual Repackaging
```bash
cd hibiki
python -c "
import zipfile
import os

addon_name = 'hibiki-1.0.0.nvda-addon'
source_dir = 'hibiki'

with zipfile.ZipFile(addon_name, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(source_dir):
        if '__pycache__' in root:
            continue
        for file in files:
            if file.endswith('.pyc') or file in ['run.py', 'test.py']:
                continue
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, source_dir)
            zf.write(file_path, arcname)
"
```

### Testing Changes
1. Uninstall previous version (NVDA menu > Tools > Manage add-ons)
2. Restart NVDA
3. Install new version
4. Restart NVDA
5. Test changes

## Code Style Guidelines

### Python Conventions
- Follow PEP 8
- Use UTF-8 encoding: `# -*- coding: utf-8 -*-`
- Add docstrings to all functions
- Use type hints where helpful (optional)

### NVDA Conventions
- Always call `nextHandler()` in event handlers
- Use `addonHandler.initTranslation()` for i18n
- Use `ui.message()` for user feedback
- Use `log.debug()` for debugging
- Prefer `config.conf` for persistent settings

### Translation Strings
- Mark all user-facing strings with `_()`:
```python
ui.message(_("Sound Navigation enabled"))
```
- Add comments for translators:
```python
# Translators: Message when add-on is enabled
ui.message(_("Sound Navigation enabled"))
```

## Performance Considerations

### Sound Preloading
All sounds are preloaded in `SoundPlayer.__init__()` for instant playback. This uses more memory but ensures no delay when navigating.

**Trade-off**: ~2MB memory vs. instant response

### Event Frequency
Focus events can fire very rapidly (10+ per second with fast navigation). The `play_for_object()` function must be fast.

**Current performance**: <1ms per call

### Memory Leaks
Watch for:
- Sounds not being garbage collected
- Event handlers holding references
- Growing collections in global variables

## Versioning

### Version Number Format
`MAJOR.MINOR.PATCH` (Semantic Versioning)

- **MAJOR**: Breaking changes (incompatible API)
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Updating Version
1. Update `manifest.ini`: `version = X.Y.Z`
2. Update package name: `hibiki-X.Y.Z.nvda-addon`
3. Update documentation dates
4. Add changelog entry

## Testing Checklist

Before releasing a new version:

- [ ] All Python files have proper encoding declarations
- [ ] No syntax errors (`python -m py_compile *.py`)
- [ ] All event handlers call `nextHandler()`
- [ ] Configuration options save and load correctly
- [ ] Speech hook is registered and restored properly
- [ ] Sound files are present and load successfully
- [ ] Package includes all necessary files
- [ ] Documentation is up to date
- [ ] Version numbers are consistent
- [ ] Tested with multiple NVDA versions (if possible)
- [ ] No memory leaks during extended use
- [ ] No crashes or freezes

## NVDA Add-on API Reference

### Essential Imports
```python
import globalPluginHandler
import addonHandler
import speech
import ui
import config
from scriptHandler import script
import controlTypes
import NVDAObjects.api
```

### Global Plugin Lifecycle
```python
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self):
        # Initialization
        pass

    def terminate(self):
        # Cleanup
        pass
```

### Event Handlers
```python
def event_gainFocus(self, obj, nextHandler):
    # Focus changed
    nextHandler()

def event_becomeNavigatorObject(self, obj, nextHandler, isFocus=False):
    # Object navigator moved
    nextHandler()
```

### Scripts (Keyboard Commands)
```python
@script(
    description=_("Description"),
    gesture="kb:NVDA+shift+s"
)
def script_myCommand(self, gesture):
    # Command implementation
    ui.message(_("Message"))
```

### Configuration
```python
# Define spec
config.conf.spec["myAddon"] = {
    "option": "boolean(default=True)"
}

# Get value
value = config.conf["myAddon"]["option"]

# Set value
config.conf["myAddon"]["option"] = True
```

## Useful Resources

### NVDA Development
- **NVDA Developer Guide**: https://www.nvaccess.org/files/nvda/documentation/developerGuide.html
- **NVDA Source Code**: https://github.com/nvaccess/nvda
- **NVDA Add-ons**: https://addons.nvda-project.org/
- **NVDA API**: Documented in source code docstrings

### Audio Libraries
- **OpenAL Soft**: https://openal-soft.org/
- **camlorn_audio**: Included with Unspoken

### Python Development
- **PEP 8**: https://www.python.org/dev/peps/pep-0008/
- **wxPython**: https://www.wxpython.org/ (for GUI)
- **configobj**: https://configobj.readthedocs.io/ (NVDA uses this)

## Contributing

### Bug Reports
Include:
1. NVDA version
2. Windows version
3. Steps to reproduce
4. Expected vs. actual behavior
5. NVDA log file

### Feature Requests
Include:
1. Use case description
2. Expected behavior
3. Why this would be useful
4. Suggested implementation (optional)

### Pull Requests
1. Fork the repository
2. Create a feature branch
3. Make changes with clear commit messages
4. Test thoroughly
5. Submit PR with description

## License

This add-on is distributed under the same license as NVDA itself (GPL v2).

## Contact

- **GitHub**: https://github.com/hibiki/hibiki
- **Issues**: https://github.com/hibiki/hibiki/issues

---

**Happy coding!**
