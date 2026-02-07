# SoundNav - NVDA Add-on for Spatial Audio Navigation

**Version**: 1.0.0
**Status**: ✅ Implementation Complete - Ready for Testing

## What is SoundNav?

SoundNav is an NVDA add-on that provides spatial 3D audio feedback for screen reader navigation. Instead of relying solely on spoken announcements like "button", "link", or "checkbox", SoundNav plays distinctive spatial sounds that help you identify controls quickly and intuitively.

## Key Features

- 🔊 **Spatial 3D Audio** - Sounds positioned left/right based on screen location
- 🎵 **40+ Control Types** - Unique sounds for buttons, links, checkboxes, menus, and more
- 🔇 **Configurable Speech Suppression** - Optional suppression of role labels
- ⌨️ **Quick Toggle** - Enable/disable with NVDA+Shift+S
- 🌍 **Multi-language** - Spanish translations included
- 🎯 **NVDA 2019.3 to 2025.3** - Wide version compatibility

## Quick Start

### Installation

1. Download `soundnav-1.0.0.nvda-addon`
2. Double-click to install
3. Restart NVDA
4. Navigate with Tab to hear sounds!

### Configuration

**NVDA menu (NVDA+N) → Preferences → Settings → Sound Navigation**

Options:
- Enable Sound Navigation
- Suppress spoken role labels

### Keyboard Shortcut

- **NVDA+Shift+S** - Toggle Sound Navigation on/off

## Project Structure

```
soundnav/
├── soundnav/                          # Add-on source code
│   ├── manifest.ini                   # Add-on metadata
│   ├── readme.html                    # User documentation
│   ├── globalPlugins/soundnav/        # Main plugin
│   │   ├── __init__.py               # Global plugin (169 lines)
│   │   ├── roleMapper.py             # Role mappings (124 lines)
│   │   ├── soundPlayer.py            # 3D audio (115 lines)
│   │   ├── settingsPanel.py          # Configuration GUI (96 lines)
│   │   ├── camlorn_audio/            # 3D audio library
│   │   └── sounds/                   # 25 WAV files
│   ├── doc/en/                       # English documentation
│   └── locale/es/LC_MESSAGES/        # Spanish translations
├── soundnav-1.0.0.nvda-addon         # Installation package (2.43 MB)
├── TESTING_GUIDE.md                  # Comprehensive testing procedures
├── IMPLEMENTATION_SUMMARY.md         # Technical implementation details
├── DEVELOPER_NOTES.md                # Developer reference
└── README.md                         # This file
```

## Documentation

### For Users
- **readme.html** - Complete user guide in Spanish
- **TESTING_GUIDE.md** - How to test the add-on

### For Developers
- **IMPLEMENTATION_SUMMARY.md** - Architecture and design decisions
- **DEVELOPER_NOTES.md** - Development guide and API reference

## Supported Control Types

### Common Controls
- Buttons, Links, Checkboxes, Radio Buttons
- Edit Fields, Password Fields, Combo Boxes
- List Items, Menu Items, Tabs

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

**NVDA Versions**: 2019.3 to 2025.3+

**Version Detection**: Automatic detection and adaptation for old vs. new `controlTypes` API

**Windows**: 7 or later

## Testing Status

- ✅ Implementation: Complete
- ⏳ User Testing: Pending
- ⏳ Compatibility Testing: Pending multiple NVDA versions
- ⏳ Performance Testing: Pending profiling

**See TESTING_GUIDE.md for detailed testing procedures**

## Known Limitations

1. **Mouse Events**: Not implemented (keyboard navigation only)
2. **Custom Sounds**: Not configurable in current version
3. **Volume Control**: Uses system volume only

## Credits

**Inspired by**: [Unspoken](https://github.com/your-link-here) by Austin Hicks

**Audio Library**: camlorn_audio (OpenAL Soft)

**Sound Files**: From Unspoken add-on

## License

Distributed under the same terms as NVDA (GPL v2).

## Contributing

Contributions welcome! Please:

1. Read **DEVELOPER_NOTES.md**
2. Test thoroughly using **TESTING_GUIDE.md**
3. Submit pull requests with clear descriptions

## Roadmap

### Version 1.1 (Future)
- [ ] Additional language translations
- [ ] Custom sound configuration
- [ ] Volume control slider
- [ ] Sound theme selection
- [ ] Performance optimizations

### Version 2.0 (Future)
- [ ] Mouse support (optional)
- [ ] Custom role-to-sound mappings
- [ ] Sound recording tool
- [ ] Web-based configuration

## Support

For issues, suggestions, or questions:

- **GitHub Issues**: https://github.com/soundnav/soundnav/issues
- **GitHub Repository**: https://github.com/soundnav/soundnav

## Changelog

### Version 1.0.0 (2025-02-07)
- 🎉 Initial release
- ✅ 40+ control types supported
- ✅ 3D spatial audio
- ✅ Configurable role label suppression
- ✅ NVDA 2019.3 to 2025.3 compatibility
- ✅ Spanish translations
- ✅ Comprehensive documentation

## Files Summary

| File | Size | Description |
|------|------|-------------|
| soundnav-1.0.0.nvda-addon | 2.43 MB | Installation package |
| TESTING_GUIDE.md | 11 KB | Testing procedures |
| IMPLEMENTATION_SUMMARY.md | 14 KB | Technical details |
| DEVELOPER_NOTES.md | 12 KB | Developer guide |
| README.md | This file | Project overview |

## Next Steps

1. **Test the add-on** using TESTING_GUIDE.md
2. **Gather feedback** from NVDA users
3. **Report issues** on GitHub
4. **Contribute** improvements

---

**Status**: 🚀 Ready for Testing
**Last Updated**: 2025-02-07

Made with ❤️ for the NVDA community
