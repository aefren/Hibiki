# -*- coding: utf-8 -*-
# roleMapper.py - Maps NVDA control types to sound files
# Part of SoundNav add-on for NVDA

import controlTypes

# Compatibility layer for NVDA version differences
# NVDA 2019.3-2020.4 uses controlTypes.ROLE_* constants
# NVDA 2021.1+ uses controlTypes.Role.* enumerations

def get_role_constant(role_name):
    """
    Get role constant compatible with both old and new NVDA versions.

    Args:
        role_name: The role name as a string (e.g., 'BUTTON', 'LINK')

    Returns:
        The appropriate role constant for the current NVDA version
    """
    # Try old-style constant first (NVDA 2019.3-2020.4)
    if hasattr(controlTypes, f'ROLE_{role_name}'):
        return getattr(controlTypes, f'ROLE_{role_name}')
    # Fall back to new-style enumeration (NVDA 2021.1+)
    else:
        return getattr(controlTypes.Role, role_name)

def get_state_constant(state_name):
    """
    Get state constant compatible with both old and new NVDA versions.

    Args:
        state_name: The state name as a string (e.g., 'CHECKED', 'EXPANDED')

    Returns:
        The appropriate state constant for the current NVDA version
    """
    # Try old-style constant first (NVDA 2019.3-2020.4)
    if hasattr(controlTypes, f'STATE_{state_name}'):
        return getattr(controlTypes, f'STATE_{state_name}')
    # Fall back to new-style enumeration (NVDA 2021.1+)
    else:
        return getattr(controlTypes.State, state_name)

# Role to sound file mapping
# Based on Unspoken add-on by Austin Hicks
ROLE_SOUND_MAP = {
    get_role_constant('CHECKBOX'): 'checkbox.wav',
    get_role_constant('RADIOBUTTON'): 'radiobutton.wav',
    get_role_constant('STATICTEXT'): 'editabletext.wav',
    get_role_constant('EDITABLETEXT'): 'editabletext.wav',
    get_role_constant('BUTTON'): 'button.wav',
    get_role_constant('MENUBAR'): 'menuitem.wav',
    get_role_constant('MENUITEM'): 'menuitem.wav',
    get_role_constant('MENU'): 'menuitem.wav',
    get_role_constant('COMBOBOX'): 'combobox.wav',
    get_role_constant('LISTITEM'): 'listitem.wav',
    get_role_constant('GRAPHIC'): 'graphic.wav',
    get_role_constant('LINK'): 'link.wav',
    get_role_constant('TREEVIEWITEM'): 'treeviewitem.wav',
    get_role_constant('TAB'): 'tab.wav',
    get_role_constant('TABCONTROL'): 'tabcontrol.wav',
    get_role_constant('SLIDER'): 'slider.wav',
    get_role_constant('DROPDOWNBUTTON'): 'combobox.wav',
    get_role_constant('CLOCK'): 'clock.wav',
    get_role_constant('ANIMATION'): 'icon.wav',
    get_role_constant('ICON'): 'icon.wav',
    get_role_constant('IMAGEMAP'): 'icon.wav',
    get_role_constant('RADIOMENUITEM'): 'radiobutton.wav',
    get_role_constant('RICHEDIT'): 'editabletext.wav',
    get_role_constant('SHAPE'): 'icon.wav',
    get_role_constant('TEAROFFMENU'): 'menuitem.wav',
    get_role_constant('TOGGLEBUTTON'): 'togglebutton.wav',
    get_role_constant('CHART'): 'icon.wav',
    get_role_constant('DIAGRAM'): 'icon.wav',
    get_role_constant('DIAL'): 'slider.wav',
    get_role_constant('DROPLIST'): 'combobox.wav',
    get_role_constant('MENUBUTTON'): 'menubutton.wav',
    get_role_constant('DROPDOWNBUTTONGRID'): 'button.wav',
    get_role_constant('HOTKEYFIELD'): 'editabletext.wav',
    get_role_constant('INDICATOR'): 'icon.wav',
    get_role_constant('SPINBUTTON'): 'slider.wav',
    get_role_constant('TREEVIEWBUTTON'): 'button.wav',
    get_role_constant('DESKTOPICON'): 'icon.wav',
    get_role_constant('PASSWORDEDIT'): 'passwordedit.wav',
    get_role_constant('CHECKMENUITEM'): 'checkbox.wav',
    get_role_constant('SPLITBUTTON'): 'splitbutton.wav',
}

# State to sound file mapping
STATE_SOUND_MAP = {
    get_state_constant('CHECKED'): 'checked.wav',
    get_state_constant('EXPANDED'): 'expanded.wav',
    get_state_constant('COLLAPSED'): 'collapsed.wav',
}

def get_sounds_for_object(obj):
    """
    Get list of sound filenames to play for a given NVDA object.

    Args:
        obj: NVDA object to get sounds for

    Returns:
        List of sound filenames (strings) to play
    """
    sounds = []

    # Get sound for the object's role
    if hasattr(obj, 'role') and obj.role in ROLE_SOUND_MAP:
        sounds.append(ROLE_SOUND_MAP[obj.role])

    # Get sounds for the object's states
    if hasattr(obj, 'states'):
        for state in obj.states:
            if state in STATE_SOUND_MAP:
                sounds.append(STATE_SOUND_MAP[state])

    return sounds
