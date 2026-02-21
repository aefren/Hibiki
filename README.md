# Hibiki - NVDA Add-on for Spatial Audio Navigation

**Version**: 0.9.1
**Minimum NVDA Version**: 2025.3.2

## What is Hibiki?

Hibiki is an NVDA add-on that provides spatial 3D audio feedback for screen reader navigation. Instead of relying solely on spoken announcements like "button", "link", or "checkbox", Hibiki plays distinctive spatial sounds that help you identify controls quickly and intuitively.

## Key Features

- 🔊 **Spatial 3D Audio** - Sounds positioned left/right based on screen location
- 🎵 **40+ Control Types** - Unique sounds for buttons, links, checkboxes, menus, and more
- 🎶 **Heading Level Sounds** - Distinct sounds for each heading level (H1–H6)
- 🔇 **Configurable Speech Suppression** - Optional suppression of role labels
- ⌨️ **Quick Toggle** - Enable/disable with NVDA+Shift+S
- 🎨 **Sound Customization** - Assign custom WAV files per control type, including per heading level
- 🌍 **Multi-language** - Spanish translations included
- 🎯 **NVDA 2025.3.2+** - Compatible with current NVDA

## Quick Start

### Installation

1. Download `Hibiki-0.9.1.nvda-addon`
2. Double-click to install
3. Restart NVDA
4. Navigate with Tab to hear sounds!

### Configuration

**NVDA menu (NVDA+N) → Preferences → Settings → Hibiki**

Options:
- Enable Hibiki
- Suppress spoken role labels

### Keyboard Shortcut

- **NVDA+Shift+S** - Toggle Hibiki on/off

## Project Structure

```
hibiki/
├── hibiki/                          # Add-on source code
│   ├── manifest.ini                   # Add-on metadata
│   ├── readme.html                    # User documentation
│   ├── globalPlugins/hibiki/        # Main plugin
│   │   ├── __init__.py               # Global plugin entry point
│   │   ├── roleMapper.py             # Role/state → sound mappings
│   │   ├── soundPlayer.py            # 3D audio playback engine
│   │   ├── settingsPanel.py          # Configuration GUI
│   │   ├── soundCustomizationDialog.py # Custom sound picker dialog
│   │   ├── camlorn_audio/            # 3D audio library
│   │   └── sounds/                   # WAV sound files
│   ├── doc/en/                       # English documentation
│   └── locale/es/LC_MESSAGES/        # Spanish translations
├── Hibiki-0.9.1.nvda-addon          # Installation package
├── CHANGELOG.md                      # Changelog
├── release_notes.md                  # Release notes
├── DEVELOPER_NOTES.md                # Developer reference
├── TRANSLATING.md                    # Translation guide
└── README.md                         # This file
```

## Documentation

### For Developers
- **DEVELOPER_NOTES.md** - Development guide and API reference
- **CHANGELOG.md** - Detailed changelog
- **release_notes.md** - Release notes and updates
- **TRANSLATING.md** - Translation guide for contributors

## Supported Control Types

### Common Controls
- Buttons, Links, Checkboxes, Radio Buttons
- Edit Fields, Password Fields, Combo Boxes
- List Items, Menu Items, Tabs

### Headings
- Heading Level 1 through Heading Level 6 (distinct sound per level)

### Specialized Controls
- Tree View Items, Sliders, Graphics
- Toggle Buttons, Split Buttons, Menu Buttons
- Clocks, Icons, Charts, Diagrams

### States
- Checked (checkboxes)
- Expanded/Collapsed (tree items)

## Technical Details

### Architecture

**Components**:
1. **GlobalPlugin** - Main event handler and coordinator
2. **RoleMapper** - Maps NVDA roles to sound files
3. **SoundPlayer** - 3D audio playback engine
4. **SettingsPanel** - Configuration GUI

**Audio Engine**: camlorn_audio with OpenAL Soft

**3D Positioning**:
- X-axis: -25.0 to +25.0 (left to right)
- Y-axis: Aspect-ratio adjusted (top to bottom)
- Z-axis: Constant -5.0 (depth)

### Compatibility

**Minimum NVDA Version**: 2025.3.2

**Windows**: 10 or later

## Testing Status

- ✅ Implementation: Complete
- ✅ User Testing: In Progress
- ✅ Compatibility Testing: NVDA 2025.3.2
- ✅ Performance Testing: Optimized

## Known Limitations

1. **Mouse Events**: Not implemented (keyboard navigation only)
2. **Volume Control**: Uses system volume only

## Credits

**Inspired by**: [Unspoken](https://github.com/your-link-here) by Austin Hicks

**Audio Library**: camlorn_audio (OpenAL Soft)

**Sound Files**: From Unspoken add-on

## License

Distributed under the same terms as NVDA (GPL v2).

## Contributing

Contributions welcome! Please:

1. Read **DEVELOPER_NOTES.md**
2. Test thoroughly using all supported NVDA versions
3. Submit pull requests with clear descriptions

## Support

For issues, suggestions, or questions:

- **GitHub Issues**: https://github.com/hibiki/hibiki/issues
- **GitHub Repository**: https://github.com/hibiki/hibiki

## Changelog

### Version 0.9.1 (2026-02-22)
- Import safety: no crash if a role constant is missing in the installed NVDA version
- Table sounds: tables, rows, cells, and headers now play sounds
- Thread safety in sound cache
- Duplicate settings panel registration prevented
- Null desktop guard in 3D audio playback

### Version 0.9 (2026-02-22)
- Heading level-specific sounds (H1–H6 each play a unique sound)
- Per-heading-level sound customization in settings dialog
- Fixed phantom sound bug by refactoring speech hook architecture
- Added browse mode 3D sound support for arrow key navigation
- Improved audio-speech synchronization

## Files Summary

| File | Size | Description |
|------|------|-------------|
| Hibiki-0.9.1.nvda-addon | — | Installation package |
| CHANGELOG.md | 8 KB | Detailed changelog |
| release_notes.md | 5 KB | Release notes |
| DEVELOPER_NOTES.md | 12 KB | Developer guide |
| TRANSLATING.md | 4 KB | Translation guide |
| README.md | — | Project overview |

## Next Steps

1. **Test the add-on** with your NVDA installation
2. **Gather feedback** from NVDA users
3. **Report issues** on GitHub
4. **Contribute** improvements

---

**Status**: 🚀 Ready for Testing
**Last Updated**: 2026-02-22

Made with ❤️ for the NVDA community
