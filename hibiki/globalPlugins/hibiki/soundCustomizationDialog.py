# soundCustomizationDialog.py - Dialog for customizing control sounds
# Part of Hibiki add-on for NVDA

import os
import json
import wave
import wx
import ui
import addonHandler
from .settingsPanel import get_config, set_config

addonHandler.initTranslation()

# Human-readable names for control types
CONTROL_DISPLAY_NAMES = {
    'checkbox': _("Checkbox"),
    'radiobutton': _("Radio Button"),
    'editabletext': _("Text Field"),
    'button': _("Button"),
    'menuitem': _("Menu Item"),
    'combobox': _("Combo Box"),
    'listitem': _("List Item"),
    'graphic': _("Graphic"),
    'link': _("Link"),
    'treeviewitem': _("Tree View Item"),
    'tab': _("Tab"),
    'slider': _("Slider"),
    'clock': _("Clock"),
    'icon': _("Icon"),
    'togglebutton': _("Toggle Button"),
    'menubutton': _("Menu Button"),
    'passwordedit': _("Password Field"),
    'splitbutton': _("Split Button"),
    'heading': _("Heading"),
    'document': _("Document"),
    'application': _("Application"),
    'landmark': _("Landmark"),
    'article': _("Article"),
    'region': _("Region"),
    'switch': _("Switch"),
    'list': _("List"),
    'progressbar': _("Progress Bar"),
    'toolbar': _("Toolbar"),
    'popupmenu': _("Popup Menu"),
    'propertypage': _("Property Page"),
    'checked': _("Checked State"),
    'expanded': _("Expanded State"),
    'collapsed': _("Collapsed State"),
    'visited': _("Visited State"),
    'pressed': _("Pressed State"),
    'selected': _("Selected State"),
    'busy': _("Busy State"),
    'clickable': _("Clickable State"),
    'haslongdesc': _("Has Long Description"),
}

# Default sound files for each control type
DEFAULT_SOUNDS = {
    'checkbox': 'checkbox.wav',
    'radiobutton': 'radiobutton.wav',
    'editabletext': 'editabletext.wav',
    'button': 'button.wav',
    'menuitem': 'menuitem.wav',
    'combobox': 'combobox.wav',
    'listitem': 'listitem.wav',
    'graphic': 'graphic.wav',
    'link': 'link.wav',
    'treeviewitem': 'treeviewitem.wav',
    'tab': 'tab.wav',
    'slider': 'slider.wav',
    'clock': 'clock.wav',
    'icon': 'icon.wav',
    'togglebutton': 'togglebutton.wav',
    'menubutton': 'menubutton.wav',
    'passwordedit': 'passwordedit.wav',
    'splitbutton': 'splitbutton.wav',
    'heading': 'heading.wav',
    'document': 'document.wav',
    'application': 'application.wav',
    'landmark': 'landmark.wav',
    'article': 'article.wav',
    'region': 'region.wav',
    'switch': 'switch.wav',
    'list': 'list.wav',
    'progressbar': 'progressbar.wav',
    'toolbar': 'toolbar.wav',
    'popupmenu': 'popupmenu.wav',
    'propertypage': 'propertypage.wav',
    'checked': 'checked.wav',
    'expanded': 'expanded.wav',
    'collapsed': 'collapsed.wav',
    'visited': 'visited.wav',
    'pressed': 'pressed.wav',
    'selected': 'selected.wav',
    'busy': 'busy.wav',
    'clickable': 'clickable.wav',
    'haslongdesc': 'haslongdesc.wav',
}

# Cached custom sounds to avoid repeated JSON parsing on hot paths
_custom_sounds_cache = {}
_custom_sounds_cache_raw = None


def get_custom_sounds():
    """
    Get the dictionary of custom sounds from config.
    
    Returns:
        dict: Mapping of control type to custom sound path
    """
    global _custom_sounds_cache, _custom_sounds_cache_raw
    try:
        custom_json = get_config("customSounds")
    except Exception:
        return {}

    # Fast path: return cached dict if config string unchanged
    if custom_json == _custom_sounds_cache_raw:
        return _custom_sounds_cache

    if not custom_json:
        _custom_sounds_cache = {}
        _custom_sounds_cache_raw = custom_json
        return _custom_sounds_cache

    try:
        _custom_sounds_cache = json.loads(custom_json)
        _custom_sounds_cache_raw = custom_json
        return _custom_sounds_cache
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        _custom_sounds_cache = {}
        _custom_sounds_cache_raw = custom_json
        return _custom_sounds_cache


def set_custom_sounds(custom_sounds):
    """
    Save the dictionary of custom sounds to config.
    
    Args:
        custom_sounds: dict mapping control type to sound path
    """
    global _custom_sounds_cache, _custom_sounds_cache_raw
    custom_json = json.dumps(custom_sounds)
    set_config("customSounds", custom_json)
    _custom_sounds_cache = dict(custom_sounds)
    _custom_sounds_cache_raw = custom_json


def validate_wav_file(filepath):
    """
    Validate that a WAV file is compatible with camlorn_audio (mono, 44100Hz).
    
    Args:
        filepath: Path to the WAV file
        
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        with wave.open(filepath, 'rb') as wav:
            channels = wav.getnchannels()
            framerate = wav.getframerate()
            
            if channels != 1:
                return False, _("The file must be mono (1 channel). This file has {} channels.").format(channels)
            
            if framerate != 44100:
                # Warning but still allow
                return True, _("Warning: Recommended sample rate is 44100 Hz. This file has {} Hz.").format(framerate)
            
            return True, None
    except wave.Error as e:
        return False, _("Invalid WAV file: {}").format(str(e))
    except Exception as e:
        return False, _("Error reading file: {}").format(str(e))


class SoundCustomizationDialog(wx.Dialog):
    """
    Dialog for customizing sounds for each control type.
    """
    
    def __init__(self, parent, sounds_directory):
        """
        Initialize the sound customization dialog.
        
        Args:
            parent: Parent window
            sounds_directory: Path to the default sounds directory
        """
        # Translators: Title of the sound customization dialog
        super().__init__(parent, title=_("Customize Control Sounds"), size=(500, 400))
        
        self.sounds_directory = sounds_directory
        self.custom_sounds = dict(get_custom_sounds())
        
        self._create_ui()
        self._populate_list()
        self.Centre()
    
    def _create_ui(self):
        """Create the dialog UI elements."""
        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Instructions
        # Translators: Instructions shown at top of sound customization dialog
        instructions = wx.StaticText(panel, label=_(
            "Select a control type and click 'Change Sound' to assign a custom WAV file.\n"
            "Sound files must be mono (1 channel) and preferably 44100 Hz."
        ))
        main_sizer.Add(instructions, 0, wx.ALL | wx.EXPAND, 10)
        
        # List control
        self.list_ctrl = wx.ListCtrl(
            panel,
            style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.BORDER_SUNKEN
        )
        # Translators: Column header for control type
        self.list_ctrl.InsertColumn(0, _("Control Type"), width=200)
        # Translators: Column header for current sound
        self.list_ctrl.InsertColumn(1, _("Current Sound"), width=250)
        
        main_sizer.Add(self.list_ctrl, 1, wx.ALL | wx.EXPAND, 10)
        
        # Buttons
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Translators: Button to change the sound for selected control
        self.change_btn = wx.Button(panel, label=_("&Change Sound..."))
        self.change_btn.Bind(wx.EVT_BUTTON, self._on_change_sound)
        button_sizer.Add(self.change_btn, 0, wx.RIGHT, 5)
        
        # Translators: Button to preview the sound for selected control
        self.preview_btn = wx.Button(panel, label=_("&Preview"))
        self.preview_btn.Bind(wx.EVT_BUTTON, self._on_preview)
        button_sizer.Add(self.preview_btn, 0, wx.RIGHT, 5)
        
        # Translators: Button to restore default sound for selected control
        self.restore_btn = wx.Button(panel, label=_("&Restore Default"))
        self.restore_btn.Bind(wx.EVT_BUTTON, self._on_restore_default)
        button_sizer.Add(self.restore_btn, 0, wx.RIGHT, 5)
        
        # Translators: Button to restore all sounds to defaults
        self.restore_all_btn = wx.Button(panel, label=_("Restore &All Defaults"))
        self.restore_all_btn.Bind(wx.EVT_BUTTON, self._on_restore_all)
        button_sizer.Add(self.restore_all_btn, 0)
        
        main_sizer.Add(button_sizer, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        
        # OK/Cancel buttons
        ok_cancel_sizer = wx.StdDialogButtonSizer()
        ok_btn = wx.Button(panel, wx.ID_OK)
        ok_btn.Bind(wx.EVT_BUTTON, self._on_ok)
        cancel_btn = wx.Button(panel, wx.ID_CANCEL)
        ok_cancel_sizer.AddButton(ok_btn)
        ok_cancel_sizer.AddButton(cancel_btn)
        ok_cancel_sizer.Realize()
        
        main_sizer.Add(ok_cancel_sizer, 0, wx.ALL | wx.ALIGN_RIGHT, 10)
        
        panel.SetSizer(main_sizer)
    
    def _populate_list(self):
        """Populate the list with control types and their sounds."""
        self.list_ctrl.DeleteAllItems()
        
        for control_key, display_name in CONTROL_DISPLAY_NAMES.items():
            index = self.list_ctrl.InsertItem(self.list_ctrl.GetItemCount(), display_name)
            self.list_ctrl.SetItemData(index, hash(control_key) & 0xFFFFFFFF)
            
            # Get current sound (custom or default)
            if control_key in self.custom_sounds:
                sound_path = self.custom_sounds[control_key]
                sound_name = os.path.basename(sound_path) + _(" (custom)")
            else:
                sound_name = DEFAULT_SOUNDS.get(control_key, _("None"))
            
            self.list_ctrl.SetItem(index, 1, sound_name)
        
        # Store mapping for later lookup
        self._control_keys = list(CONTROL_DISPLAY_NAMES.keys())
    
    def _get_selected_control_key(self):
        """Get the control key for the selected item."""
        selection = self.list_ctrl.GetFirstSelected()
        if selection == -1:
            return None
        return self._control_keys[selection]
    
    def _on_change_sound(self, event):
        """Handle Change Sound button click."""
        control_key = self._get_selected_control_key()
        if not control_key:
            # Translators: Message when no control is selected
            ui.message(_("Please select a control type first."))
            return
        
        # Translators: Title of file picker dialog
        with wx.FileDialog(
            self,
            _("Select Sound File"),
            wildcard=_("WAV files (*.wav)|*.wav"),
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        ) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return
            
            filepath = file_dialog.GetPath()
            
            # Validate the file
            is_valid, message = validate_wav_file(filepath)
            
            if not is_valid:
                wx.MessageBox(
                    message,
                    _("Invalid Sound File"),
                    wx.OK | wx.ICON_ERROR
                )
                return
            
            # Show warning if any
            if message:
                wx.MessageBox(
                    message,
                    _("Warning"),
                    wx.OK | wx.ICON_WARNING
                )
            
            # Save the custom sound
            self.custom_sounds[control_key] = filepath
            self._populate_list()
            
            # Translators: Confirmation message after changing sound
            ui.message(_("Sound changed successfully."))
    
    def _on_preview(self, event):
        """Handle Preview button click."""
        control_key = self._get_selected_control_key()
        if not control_key:
            ui.message(_("Please select a control type first."))
            return
        
        # Get the sound path
        if control_key in self.custom_sounds:
            sound_path = self.custom_sounds[control_key]
        else:
            default_sound = DEFAULT_SOUNDS.get(control_key)
            if default_sound:
                sound_path = os.path.join(self.sounds_directory, default_sound)
            else:
                ui.message(_("No sound assigned."))
                return
        
        if not os.path.exists(sound_path):
            ui.message(_("Sound file not found."))
            return
        
        # Play the sound using nvwave for preview (simpler than camlorn for preview)
        try:
            import nvwave
            nvwave.playWaveFile(sound_path)
        except Exception as e:
            ui.message(_("Error playing sound: {}").format(str(e)))
    
    def _on_restore_default(self, event):
        """Handle Restore Default button click."""
        control_key = self._get_selected_control_key()
        if not control_key:
            ui.message(_("Please select a control type first."))
            return
        
        if control_key in self.custom_sounds:
            del self.custom_sounds[control_key]
            self._populate_list()
            # Translators: Confirmation after restoring default sound
            ui.message(_("Default sound restored."))
        else:
            ui.message(_("Already using default sound."))
    
    def _on_restore_all(self, event):
        """Handle Restore All Defaults button click."""
        if not self.custom_sounds:
            ui.message(_("All sounds are already set to defaults."))
            return
        
        # Translators: Confirmation dialog for restoring all defaults
        result = wx.MessageBox(
            _("Are you sure you want to restore all sounds to their defaults?"),
            _("Confirm Restore All"),
            wx.YES_NO | wx.ICON_QUESTION
        )
        
        if result == wx.YES:
            self.custom_sounds.clear()
            self._populate_list()
            ui.message(_("All default sounds restored."))
    
    def _on_ok(self, event):
        """Handle OK button - save changes."""
        set_custom_sounds(self.custom_sounds)
        self.EndModal(wx.ID_OK)
