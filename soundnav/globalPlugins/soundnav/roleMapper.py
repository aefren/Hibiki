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
    get_role_constant('LIST'): 'list.wav',
    get_role_constant('LISTITEM'): 'listitem.wav',
    get_role_constant('GRAPHIC'): 'graphic.wav',
    get_role_constant('LINK'): 'link.wav',
    get_role_constant('TREEVIEWITEM'): 'treeviewitem.wav',
    get_role_constant('TAB'): 'tab.wav',
    get_role_constant('TABCONTROL'): 'tab.wav',
    get_role_constant('PROPERTYPAGE'): 'propertypage.wav',
    get_role_constant('SLIDER'): 'slider.wav',
    get_role_constant('PROGRESSBAR'): 'progressbar.wav',
    get_role_constant('DROPDOWNBUTTON'): 'combobox.wav',
    get_role_constant('CLOCK'): 'clock.wav',
    get_role_constant('ANIMATION'): 'icon.wav',
    get_role_constant('ICON'): 'icon.wav',
    get_role_constant('IMAGEMAP'): 'icon.wav',
    get_role_constant('RADIOMENUITEM'): 'radiobutton.wav',
    get_role_constant('RICHEDIT'): 'editabletext.wav',
    get_role_constant('SHAPE'): 'icon.wav',
    get_role_constant('TEAROFFMENU'): 'menuitem.wav',
    get_role_constant('POPUPMENU'): 'popupmenu.wav',
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
    get_role_constant('TOOLBAR'): 'toolbar.wav',
    get_role_constant('HEADING'): 'heading.wav',
    get_role_constant('HEADING1'): 'heading.wav',
    get_role_constant('HEADING2'): 'heading.wav',
    get_role_constant('HEADING3'): 'heading.wav',
    get_role_constant('HEADING4'): 'heading.wav',
    get_role_constant('HEADING5'): 'heading.wav',
    get_role_constant('HEADING6'): 'heading.wav',
    get_role_constant('DOCUMENT'): 'document.wav',
    get_role_constant('APPLICATION'): 'application.wav',
    get_role_constant('LANDMARK'): 'landmark.wav',
    get_role_constant('ARTICLE'): 'article.wav',
    get_role_constant('REGION'): 'region.wav',
    get_role_constant('SWITCH'): 'switch.wav',
    get_role_constant('TABLE'): 'table.wav',
    get_role_constant('TABLEROW'): 'tablerow.wav',
    get_role_constant('TABLECELL'): 'tablecell.wav',
    get_role_constant('TABLECOLUMNHEADER'): 'tableheader.wav',
    get_role_constant('TABLEROWHEADER'): 'tableheader.wav',
}

# State to sound file mapping
STATE_SOUND_MAP = {
    get_state_constant('CHECKED'): 'checked.wav',
    get_state_constant('EXPANDED'): 'expanded.wav',
    get_state_constant('COLLAPSED'): 'collapsed.wav',
    get_state_constant('VISITED'): 'visited.wav',
    get_state_constant('PRESSED'): 'pressed.wav',
    get_state_constant('SELECTED'): 'selected.wav',
    get_state_constant('BUSY'): 'busy.wav',
    get_state_constant('CLICKABLE'): 'clickable.wav',
    get_state_constant('HASLONGDESC'): 'haslongdesc.wav',
}

# Mapping from role constants to control keys (for custom sound lookup)
ROLE_TO_CONTROL_KEY = {
    get_role_constant('CHECKBOX'): 'checkbox',
    get_role_constant('RADIOBUTTON'): 'radiobutton',
    get_role_constant('STATICTEXT'): 'editabletext',
    get_role_constant('EDITABLETEXT'): 'editabletext',
    get_role_constant('BUTTON'): 'button',
    get_role_constant('MENUBAR'): 'menuitem',
    get_role_constant('MENUITEM'): 'menuitem',
    get_role_constant('MENU'): 'menuitem',
    get_role_constant('COMBOBOX'): 'combobox',
    get_role_constant('LISTITEM'): 'listitem',
    get_role_constant('GRAPHIC'): 'graphic',
    get_role_constant('LINK'): 'link',
    get_role_constant('TREEVIEWITEM'): 'treeviewitem',
    get_role_constant('TAB'): 'tab',
    get_role_constant('TABCONTROL'): 'tab',
    get_role_constant('SLIDER'): 'slider',
    get_role_constant('DROPDOWNBUTTON'): 'combobox',
    get_role_constant('CLOCK'): 'clock',
    get_role_constant('ANIMATION'): 'icon',
    get_role_constant('ICON'): 'icon',
    get_role_constant('IMAGEMAP'): 'icon',
    get_role_constant('RADIOMENUITEM'): 'radiobutton',
    get_role_constant('RICHEDIT'): 'editabletext',
    get_role_constant('SHAPE'): 'icon',
    get_role_constant('TEAROFFMENU'): 'menuitem',
    get_role_constant('TOGGLEBUTTON'): 'togglebutton',
    get_role_constant('CHART'): 'icon',
    get_role_constant('DIAGRAM'): 'icon',
    get_role_constant('DIAL'): 'slider',
    get_role_constant('DROPLIST'): 'combobox',
    get_role_constant('MENUBUTTON'): 'menubutton',
    get_role_constant('DROPDOWNBUTTONGRID'): 'button',
    get_role_constant('HOTKEYFIELD'): 'editabletext',
    get_role_constant('INDICATOR'): 'icon',
    get_role_constant('SPINBUTTON'): 'slider',
    get_role_constant('TREEVIEWBUTTON'): 'button',
    get_role_constant('DESKTOPICON'): 'icon',
    get_role_constant('PASSWORDEDIT'): 'passwordedit',
    get_role_constant('CHECKMENUITEM'): 'checkbox',
    get_role_constant('SPLITBUTTON'): 'splitbutton',
    get_role_constant('LIST'): 'list',
    get_role_constant('PROGRESSBAR'): 'progressbar',
    get_role_constant('PROPERTYPAGE'): 'propertypage',
    get_role_constant('POPUPMENU'): 'popupmenu',
    get_role_constant('TOOLBAR'): 'toolbar',
    get_role_constant('HEADING'): 'heading',
    get_role_constant('HEADING1'): 'heading',
    get_role_constant('HEADING2'): 'heading',
    get_role_constant('HEADING3'): 'heading',
    get_role_constant('HEADING4'): 'heading',
    get_role_constant('HEADING5'): 'heading',
    get_role_constant('HEADING6'): 'heading',
    get_role_constant('DOCUMENT'): 'document',
    get_role_constant('APPLICATION'): 'application',
    get_role_constant('LANDMARK'): 'landmark',
    get_role_constant('ARTICLE'): 'article',
    get_role_constant('REGION'): 'region',
    get_role_constant('SWITCH'): 'switch',
    get_role_constant('TABLE'): 'table',
    get_role_constant('TABLEROW'): 'tablerow',
    get_role_constant('TABLECELL'): 'tablecell',
    get_role_constant('TABLECOLUMNHEADER'): 'tableheader',
    get_role_constant('TABLEROWHEADER'): 'tableheader',
}

# Mapping from state constants to control keys (for custom sound lookup)
STATE_TO_CONTROL_KEY = {
    get_state_constant('CHECKED'): 'checked',
    get_state_constant('EXPANDED'): 'expanded',
    get_state_constant('COLLAPSED'): 'collapsed',
    get_state_constant('VISITED'): 'visited',
    get_state_constant('PRESSED'): 'pressed',
    get_state_constant('SELECTED'): 'selected',
    get_state_constant('BUSY'): 'busy',
    get_state_constant('CLICKABLE'): 'clickable',
    get_state_constant('HASLONGDESC'): 'haslongdesc',
}


def get_sounds_for_object(obj):
    """
    Get list of sound filenames or paths to play for a given NVDA object.

    Args:
        obj: NVDA object to get sounds for

    Returns:
        List of sound filenames/paths (strings) to play
    """
    sounds = []
    from .soundCustomizationDialog import get_custom_sounds
    custom_sounds = get_custom_sounds()

    # Get sound for the object's role
    if hasattr(obj, 'role') and obj.role in ROLE_SOUND_MAP:
        # Check for custom sound first
        control_key = ROLE_TO_CONTROL_KEY.get(obj.role)
        if control_key and control_key in custom_sounds:
            sounds.append(custom_sounds[control_key])
        else:
            sounds.append(ROLE_SOUND_MAP[obj.role])

    # Get sounds for the object's states
    if hasattr(obj, 'states'):
        for state in obj.states:
            if state in STATE_SOUND_MAP:
                # Check for custom sound first
                control_key = STATE_TO_CONTROL_KEY.get(state)
                if control_key and control_key in custom_sounds:
                    sounds.append(custom_sounds[control_key])
                else:
                    sounds.append(STATE_SOUND_MAP[state])

    return sounds

