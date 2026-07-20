# Hibiki v0.9.2 - Quick Navigation & Label Suppression Fixes

This release fixes a navigation-accuracy bug that affected every quick-nav key (b, shift+b, h, k, and friends) in browse mode, plus two related label-suppression bugs. If you're upgrading from 0.8.1, the "Previously" section below also covers what changed in 0.9 and 0.9.1, which never got their own release notes.

## What's New in 0.9.2

### Highlights
- 🎯 **Fixed sound position lag during quick navigation** - Sounds triggered by b, shift+b, h, k, and other single-letter/quick-nav keys now play at the position of the control being announced, not the previously focused one
- 🔊 **Fixed shared-line controls sounding identical** - Multiple controls on the same line (e.g. several links in one sentence) now each play at their own position instead of all sharing the first control's spot
- 🗣️ **Smarter label suppression** - Role and state labels are only hidden when a sound actually replaces them

### Bug Fixes
- **Quick navigation sound lag**: NVDA's browse mode announces a quick-nav target (`item.report()`) before moving the virtual caret to it (`item.moveTo()`) — this is deliberate on NVDA's side (see NVDA issue #8831), but it meant Hibiki was reading the *old* caret position when positioning sounds, so every sound landed one control behind. Hibiki now resolves the actual control being announced through its virtual buffer identifier, falling back to the text range being spoken, and only to the caret as a last resort.
- **Shared-line controls**: because the fix above resolves each control field individually rather than from a shared caret position, controls that share a line (several links in a sentence, for example) now get distinct positions.
- **Over-eager label suppression**: "Suppress spoken role labels" and "Suppress spoken state labels" no longer hide labels for roles or states Hibiki has no sound for (dialogs, groupings, windows, "unavailable", "read only", "required", etc.). Those are spoken normally again instead of being silently dropped.
- **Label suppression vs. browse mode sounds**: with "Play sounds during browse mode navigation" turned off, role and state labels are now spoken in browse mode instead of being hidden with nothing to replace them. Focus-mode suppression (Tab navigation in applications) is unaffected by that switch.

## Previously

### 0.9.1
- Fixed a startup crash on NVDA versions missing a role constant Hibiki referenced
- Added distinct sounds for tables, table rows, cells, and column/row headers
- Made the sound cache thread-safe
- Fixed duplicate settings panel registration and a null-desktop crash guard

### 0.9
- Added a distinct sound per heading level (H1–H6) instead of one generic heading sound
- Added per-level customization for heading sounds in the sound settings dialog

## Installation
1. Download `Hibiki-0.9.2.nvda-addon` from this release
2. Open the file with NVDA
3. Accept the installation prompt (this will replace an existing Hibiki install)
4. NVDA will restart automatically

## Usage
- **Toggle Hibiki**: NVDA+Shift+S
- **Navigation**: Arrow keys, Tab, or NVDA+Numpad keys provide spatial audio feedback
- **Browse Mode**: Quick navigation keys (b, h, k, e, etc.) and arrow keys now report accurate 3D positions
- **Customization**: Access settings through NVDA → Preferences → Settings → Hibiki

## Known Issues
- Rapidly navigating between controls of the same type can cut off the previous sound before it finishes, since each sound file currently plays from a single shared audio source. Not something a screen reader user would misread as a bug in control identification — it's a playback/audio-engine limitation, tracked for a future release.
- Multi-monitor setups are not accounted for in the 3D position calculation; controls on a secondary monitor may be positioned outside the expected left/right range.

Please file issues on GitHub if you encounter any problems.
