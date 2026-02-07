# SoundNav Add-on - Testing Guide

## Pre-Installation Checks

Before testing the add-on, ensure:

1. **NVDA is installed** - Version 2019.3 or later
2. **Backup your NVDA configuration** - Just in case
3. **Close any running NVDA instances**

## Installation

1. Locate the file: `soundnav-1.0.0.nvda-addon`
2. Double-click the file (or press Enter on it)
3. NVDA will prompt you to install the add-on
4. Accept the installation
5. Restart NVDA when prompted

## Phase 1: Basic Functionality Tests

### Test 1: Add-on Activation
1. After NVDA restarts, press **NVDA+N** to open the NVDA menu
2. Navigate to **Preferences > Settings**
3. Verify that "Sound Navigation" appears in the categories list
4. Press **NVDA+Shift+S** and verify you hear "Sound Navigation enabled"

### Test 2: Web Browser Navigation
1. Open Firefox or Chrome
2. Navigate to a complex webpage (e.g., google.com)
3. Press **Tab** repeatedly to navigate through controls
4. **Expected result**: You should hear different sounds for:
   - Buttons (soft click sound)
   - Links (bubbling water sound)
   - Text fields (typing sound)
   - Each sound should be positioned left/right based on screen location

### Test 3: File Explorer Navigation
1. Open Windows File Explorer (Win+E)
2. Navigate through folders using arrow keys
3. **Expected result**: You should hear sounds for:
   - Tree view items
   - List items
   - Icons

### Test 4: Object Navigation
1. While in any application, use **NVDA+Numpad 8/4/6/2** to navigate objects
2. **Expected result**: You should hear sounds as you move between objects

## Phase 2: Configuration Tests

### Test 5: Settings Panel
1. Press **NVDA+N** to open NVDA menu
2. Navigate to **Preferences > Settings**
3. Select "Sound Navigation" category
4. **Verify the following controls exist**:
   - "Enable Sound Navigation" checkbox
   - "Suppress spoken role labels" checkbox

### Test 6: Suppress Role Labels
1. Open the Sound Navigation settings
2. **Enable** "Suppress spoken role labels"
3. Click OK
4. Navigate through a webpage with Tab
5. **Expected result**: You should hear ONLY sounds, NOT "button", "link", etc.

6. **Disable** "Suppress spoken role labels"
7. Click OK
8. Navigate through the same webpage
9. **Expected result**: You should hear BOTH sounds AND "button", "link", etc.

### Test 7: Toggle with Keyboard
1. Press **NVDA+Shift+S** to disable Sound Navigation
2. **Expected result**: Message "Sound Navigation disabled"
3. Navigate with Tab - should hear NO sounds
4. Press **NVDA+Shift+S** again to enable
5. **Expected result**: Message "Sound Navigation enabled"
6. Navigate with Tab - sounds should be back

## Phase 3: Advanced Tests

### Test 8: Multiple Control Types
Navigate to a complex webpage (e.g., https://www.w3.org/WAI/demos/bad/) and verify sounds for:

- **Buttons** (button.wav) - Submit, Cancel buttons
- **Links** (link.wav) - Regular hyperlinks
- **Checkboxes** (checkbox.wav) - Selection boxes
- **Radio buttons** (radiobutton.wav) - Single selection controls
- **Combo boxes** (combobox.wav) - Dropdown menus
- **Text fields** (editabletext.wav) - Input fields
- **Tabs** (tab.wav) - Tab controls

### Test 9: State Sounds
1. Navigate to a checkbox control
2. If it's checked, you should hear TWO sounds:
   - checkbox.wav (for the control type)
   - checked.wav (for the checked state)
3. Navigate to a tree view with expandable items
4. You should hear:
   - expanded.wav for expanded items
   - collapsed.wav for collapsed items

### Test 10: 3D Positioning
1. Open a webpage with controls spread across the screen
2. Navigate to a button on the LEFT side of the screen
3. **Expected result**: Sound should come from the LEFT
4. Navigate to a button on the RIGHT side of the screen
5. **Expected result**: Sound should come from the RIGHT
6. **Note**: You may need headphones to clearly hear the stereo positioning

## Phase 4: Compatibility Tests

### Test 11: Different Applications
Test Sound Navigation in:
- [ ] Firefox
- [ ] Chrome
- [ ] Microsoft Edge
- [ ] Microsoft Word (if available)
- [ ] Notepad
- [ ] Windows Settings
- [ ] File Explorer
- [ ] Any other commonly used applications

### Test 12: Rapid Navigation
1. Open a webpage with many links
2. Hold down the **Tab** key to navigate rapidly
3. **Expected result**:
   - Sounds should play smoothly without lag
   - NVDA should not freeze or crash
   - Memory usage should remain stable

## Phase 5: Error Handling Tests

### Test 13: Missing Sound Files
This test verifies graceful degradation if sound files are missing (should not be necessary for normal testing).

### Test 14: Reinstallation
1. Uninstall the add-on: NVDA menu > Tools > Manage add-ons > SoundNav > Remove
2. Restart NVDA
3. Verify that NVDA works normally without SoundNav
4. Reinstall the add-on
5. Verify everything works again

## Expected Test Results Summary

| Test | Expected Result | Pass/Fail | Notes |
|------|----------------|-----------|-------|
| Test 1: Activation | Settings panel appears, toggle works | | |
| Test 2: Web Browser | Different sounds for different controls | | |
| Test 3: File Explorer | Sounds for tree/list items | | |
| Test 4: Object Navigation | Sounds with NVDA+numpad | | |
| Test 5: Settings Panel | Two checkboxes present | | |
| Test 6: Suppress Labels | Labels suppressed when enabled | | |
| Test 7: Toggle Keyboard | NVDA+Shift+S works | | |
| Test 8: Multiple Types | All control types have sounds | | |
| Test 9: State Sounds | Checked/expanded/collapsed sounds | | |
| Test 10: 3D Positioning | Left/right positioning works | | |
| Test 11: Applications | Works in multiple apps | | |
| Test 12: Rapid Navigation | No lag or crashes | | |
| Test 14: Reinstallation | Clean uninstall/reinstall | | |

## Troubleshooting

### No sounds playing
- Check that Sound Navigation is enabled (NVDA+Shift+S)
- Check the settings panel
- Verify system volume is not muted
- Check that you're navigating to supported control types

### NVDA crashes or freezes
- Disable the add-on immediately (NVDA+Shift+S)
- Report the issue with detailed steps to reproduce
- Consider uninstalling until the issue is fixed

### Sounds are not positioned correctly
- Verify you're using stereo audio (not mono)
- Try using headphones for clearer positioning
- Check that the control has a valid screen location

### Configuration not saving
- Check NVDA configuration directory permissions
- Try resetting NVDA configuration
- Report the issue

## Performance Metrics to Watch

While testing, monitor:
- **Memory usage**: Should not increase significantly over time
- **CPU usage**: Should remain low (< 5% when idle)
- **Responsiveness**: Navigation should feel instant, not delayed
- **Audio quality**: Sounds should be clear, not distorted

## Reporting Issues

When reporting issues, include:
1. NVDA version
2. Windows version
3. Steps to reproduce
4. Expected vs. actual behavior
5. Any error messages
6. NVDA log file (NVDA menu > Tools > View log)

## Success Criteria

The add-on is working correctly if:
- ✅ All 14 tests pass
- ✅ No crashes or freezes occur
- ✅ Sounds play for all supported control types
- ✅ 3D positioning is noticeable (with stereo audio)
- ✅ Configuration persists across NVDA restarts
- ✅ Toggle keyboard shortcut works
- ✅ No significant performance impact
