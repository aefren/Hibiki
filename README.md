# Hibiki — NVDA Add-on for Spatial Audio Navigation

![Version](https://img.shields.io/github/v/release/aefren/Hibiki?label=version)
![License](https://img.shields.io/github/license/aefren/Hibiki)

Hibiki is an NVDA add-on that provides spatial 3D audio feedback for screen reader
navigation. Instead of relying solely on spoken announcements like "button", "link",
or "checkbox", Hibiki plays distinctive spatial sounds — positioned in stereo space
where the control sits on screen — that help you identify controls quickly and
intuitively.

## Key Features

- 🔊 **Spatial 3D Audio** — Sounds positioned left/right based on screen location
- 🎵 **40+ Control Types** — Unique sounds for buttons, links, checkboxes, menus, and more
- 🎶 **Heading Level Sounds** — Distinct sounds for each heading level (H1–H6)
- 🔇 **Configurable Speech Suppression** — Optional suppression of role labels
- ⌨️ **Quick Toggle** — Enable/disable with NVDA+Shift+S
- 🎨 **Sound Customization** — Assign custom WAV files per control type, including per heading level
- 🌍 **Multi-language** — Spanish translations included

## Quick Start

### Installation

1. Download the latest `.nvda-addon` file from
   [Releases](https://github.com/aefren/Hibiki/releases).
2. Open it (Enter) to install, and restart NVDA.
3. Navigate with Tab to hear sounds!

Requires NVDA 2025.3.2+ on Windows 10 or later.

### Configuration

**NVDA menu (NVDA+N) → Preferences → Settings → Hibiki**

Options:
- Enable Hibiki
- Suppress spoken role labels
- Custom sounds per control type

### Keyboard Shortcut

- **NVDA+Shift+S** — Toggle Hibiki on/off

## Supported Control Types

- **Common controls** — buttons, links, checkboxes, radio buttons, edit fields,
  password fields, combo boxes, list items, menu items, tabs
- **Headings** — levels 1 through 6, each with its own sound
- **Specialized controls** — tree view items, sliders, graphics, toggle buttons,
  split buttons, menu buttons, clocks, icons, charts, diagrams
- **States** — checked (checkboxes), expanded/collapsed (tree items)
- **Tables** — tables, rows, cells and headers

## How it works

- **GlobalPlugin** (`hibiki/globalPlugins/hibiki/__init__.py`) hooks NVDA's speech
  and focus events.
- **RoleMapper** maps NVDA roles and states to sound files, entry by entry, so a role
  missing from the installed NVDA version never breaks the add-on.
- **SoundPlayer** positions each sound in 3D using camlorn_audio (OpenAL Soft):
  X follows the control's horizontal position, Y its vertical position
  (aspect-ratio adjusted), Z is fixed depth.
- **SettingsPanel** and the sound customization dialog provide the configuration GUI.

See [docs/DEVELOPER_NOTES.md](docs/DEVELOPER_NOTES.md) for the developer guide and
[CHANGELOG.md](CHANGELOG.md) for the detailed version history.

## Building from source

```
python build_addon.py
```

This produces the installable `.nvda-addon` package.

## Translating

See [TRANSLATING.md](TRANSLATING.md) to contribute a translation. Spanish is
already included.

## Known Limitations

1. **Mouse events**: not implemented (keyboard navigation only).
2. **Volume control**: uses system volume only.

## Credits

- **Inspired by** [Unspoken](https://github.com/camlorn/unspoken) by Austin Hicks,
  which also provided the audio library (camlorn_audio / OpenAL Soft) and the base
  sound set.

## License

[GPL-2.0](LICENSE), the same terms as NVDA.

## Support

Issues and suggestions: https://github.com/aefren/Hibiki/issues
