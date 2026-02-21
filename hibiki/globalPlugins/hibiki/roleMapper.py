# roleMapper.py - Maps NVDA control types to sound files
# Part of Hibiki add-on for NVDA

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

# Unified role definitions: role_name -> (sound_file, control_key)
# Based on Unspoken add-on by Austin Hicks
# Each role is defined once, eliminating duplication between sound map and control key map
_ROLE_DEFINITIONS = {
    'CHECKBOX': ('checkbox.wav', 'checkbox'),
    'RADIOBUTTON': ('radiobutton.wav', 'radiobutton'),
    'STATICTEXT': ('editabletext.wav', 'editabletext'),
    'EDITABLETEXT': ('editabletext.wav', 'editabletext'),
    'BUTTON': ('button.wav', 'button'),
    'MENUBAR': ('menuitem.wav', 'menuitem'),
    'MENUITEM': ('menuitem.wav', 'menuitem'),
    'MENU': ('menuitem.wav', 'menuitem'),
    'COMBOBOX': ('combobox.wav', 'combobox'),
    'LIST': ('list.wav', 'list'),
    'LISTITEM': ('listitem.wav', 'listitem'),
    'GRAPHIC': ('graphic.wav', 'graphic'),
    'LINK': ('link.wav', 'link'),
    'TREEVIEWITEM': ('treeviewitem.wav', 'treeviewitem'),
    'TAB': ('tab.wav', 'tab'),
    'TABCONTROL': ('tab.wav', 'tab'),
    'PROPERTYPAGE': ('propertypage.wav', 'propertypage'),
    'SLIDER': ('slider.wav', 'slider'),
    'PROGRESSBAR': ('progressbar.wav', 'progressbar'),
    'DROPDOWNBUTTON': ('combobox.wav', 'combobox'),
    'CLOCK': ('clock.wav', 'clock'),
    'ANIMATION': ('icon.wav', 'icon'),
    'ICON': ('icon.wav', 'icon'),
    'IMAGEMAP': ('icon.wav', 'icon'),
    'RADIOMENUITEM': ('radiobutton.wav', 'radiobutton'),
    'RICHEDIT': ('editabletext.wav', 'editabletext'),
    'SHAPE': ('icon.wav', 'icon'),
    'TEAROFFMENU': ('menuitem.wav', 'menuitem'),
    'POPUPMENU': ('popupmenu.wav', 'popupmenu'),
    'TOGGLEBUTTON': ('togglebutton.wav', 'togglebutton'),
    'CHART': ('icon.wav', 'icon'),
    'DIAGRAM': ('icon.wav', 'icon'),
    'DIAL': ('slider.wav', 'slider'),
    'DROPLIST': ('combobox.wav', 'combobox'),
    'MENUBUTTON': ('menubutton.wav', 'menubutton'),
    'DROPDOWNBUTTONGRID': ('button.wav', 'button'),
    'HOTKEYFIELD': ('editabletext.wav', 'editabletext'),
    'INDICATOR': ('icon.wav', 'icon'),
    'SPINBUTTON': ('slider.wav', 'slider'),
    'TREEVIEWBUTTON': ('button.wav', 'button'),
    'DESKTOPICON': ('icon.wav', 'icon'),
    'PASSWORDEDIT': ('passwordedit.wav', 'passwordedit'),
    'CHECKMENUITEM': ('checkbox.wav', 'checkbox'),
    'SPLITBUTTON': ('splitbutton.wav', 'splitbutton'),
    'TOOLBAR': ('toolbar.wav', 'toolbar'),
    'HEADING': ('heading.wav', 'heading'),
    'HEADING1': ('h1.wav', 'heading1'),
    'HEADING2': ('h2.wav', 'heading2'),
    'HEADING3': ('h3.wav', 'heading3'),
    'HEADING4': ('h4.wav', 'heading4'),
    'HEADING5': ('h5.wav', 'heading5'),
    'HEADING6': ('h6.wav', 'heading6'),
    'DOCUMENT': ('document.wav', 'document'),
    'APPLICATION': ('application.wav', 'application'),
    'LANDMARK': ('landmark.wav', 'landmark'),
    'ARTICLE': ('article.wav', 'article'),
    'REGION': ('region.wav', 'region'),
    'SWITCH': ('switch.wav', 'switch'),
    'TABLE': ('snd2.wav', 'table'),
    'TABLEROW': ('snd11.wav', 'tablerow'),
    'TABLECELL': ('snd12.wav', 'tablecell'),
    'TABLECOLUMNHEADER': ('snd13.wav', 'tableheader'),
    'TABLEROWHEADER': ('snd13.wav', 'tableheader'),
}

# Unified state definitions: state_name -> (sound_file, control_key)
_STATE_DEFINITIONS = {
    'CHECKED': ('checked.wav', 'checked'),
    'EXPANDED': ('expanded.wav', 'expanded'),
    'COLLAPSED': ('collapsed.wav', 'collapsed'),
    'VISITED': ('visited.wav', 'visited'),
    'PRESSED': ('pressed.wav', 'pressed'),
    'SELECTED': ('selected.wav', 'selected'),
    'BUSY': ('busy.wav', 'busy'),
    'CLICKABLE': ('clickable.wav', 'clickable'),
    'HASLONGDESC': ('haslongdesc.wav', 'haslongdesc'),
}

# Generate role mappings from unified definitions.
# Uses try/except per entry to skip roles that don't exist in this NVDA version,
# preventing a fatal import crash on older or newer NVDA builds.
ROLE_SOUND_MAP = {}
ROLE_TO_CONTROL_KEY = {}
for _role_name, _role_data in _ROLE_DEFINITIONS.items():
    try:
        _const = get_role_constant(_role_name)
        ROLE_SOUND_MAP[_const] = _role_data[0]
        ROLE_TO_CONTROL_KEY[_const] = _role_data[1]
    except AttributeError:
        pass

# Generic HEADING role constant (modern NVDA uses this + a separate level attribute)
_HEADING_ROLE_CONSTANT = get_role_constant('HEADING')

# Sound files indexed by heading level (1–6) for modern NVDA
_HEADING_LEVEL_SOUNDS = {
    1: 'h1.wav',
    2: 'h2.wav',
    3: 'h3.wav',
    4: 'h4.wav',
    5: 'h5.wav',
    6: 'h6.wav',
}

# Generate state mappings from unified definitions
STATE_SOUND_MAP = {get_state_constant(k): v[0] for k, v in _STATE_DEFINITIONS.items()}
STATE_TO_CONTROL_KEY = {get_state_constant(k): v[1] for k, v in _STATE_DEFINITIONS.items()}


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
        control_key = ROLE_TO_CONTROL_KEY.get(obj.role)
        sound_file = ROLE_SOUND_MAP[obj.role]

        # For the generic HEADING role (modern NVDA), resolve the level-specific
        # control key and sound. The level can be an int (focus mode) or a string
        # (browse mode virtual buffer attrs), so we always convert via int().
        if obj.role == _HEADING_ROLE_CONSTANT:
            try:
                level = int(getattr(obj, 'level', None))
                if level in _HEADING_LEVEL_SOUNDS:
                    control_key = 'heading{}'.format(level)
                    sound_file = _HEADING_LEVEL_SOUNDS[level]
            except (TypeError, ValueError):
                pass

        if control_key and control_key in custom_sounds:
            sounds.append(custom_sounds[control_key])
        else:
            sounds.append(sound_file)

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

