# Hibiki v0.8.1 - First Official Release

🎉 We're thrilled to announce the first official release of **Hibiki**. This release marks a significant milestone with major improvements to audio feedback and stability.

## What's New

### Highlights
- 🎉 **First official release of Hibiki** - A spatial 3D audio feedback system for UI navigation
- 🐛 **Fixed phantom sound bug** - Refactored speech hook architecture to prevent sounds playing on unrelated speech events
- ⌨️ **Added browse mode support** - Arrow key navigation now includes 3D positional audio feedback
- 🎯 **Improved audio-speech synchronization** - Better alignment between spatial sounds and spoken labels

### Bug Fixes
- Fixed phantom sounds playing on unrelated speech events (#getPropertiesSpeech hook refactoring)
- Fixed browse mode sound delays during arrow key navigation
- Fixed getPropertiesSpeech hook implementation to use internal functions correctly
- Improved speech hook architecture for better event isolation

### Technical Changes
- Refactored speech hook system for improved reliability
- Enhanced internal function hooking mechanism
- Improved event handler isolation to prevent audio interference

## Installation
1. Download `Hibiki-0.8.1.nvda-addon` from this release
2. Open the file with NVDA
3. Accept the installation prompt
4. NVDA will restart automatically

## Usage
- **Toggle Hibiki**: NVDA+Shift+S
- **Navigation**: Arrow keys, Tab, or NVDA+Numpad keys provide spatial audio feedback
- **Browse Mode**: Use arrow keys in browse mode for directional audio cues
- **Customization**: Access settings through NVDA → Preferences → Settings → Hibiki

## Known Issues
None reported. Please file issues on GitHub if you encounter any problems.
