# -*- coding: utf-8 -*-
# __init__.py - Main global plugin for SoundNav
# Part of SoundNav add-on for NVDA

import os
import globalPluginHandler
import addonHandler
import speech
import ui
import api
import textInfos
from scriptHandler import script

from .soundPlayer import SoundPlayer
from .roleMapper import get_sounds_for_object
from .settingsPanel import init_configuration, get_config, set_config, SoundNavSettingsPanel

addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    """
    Main global plugin for SoundNav add-on.

    Provides spatial 3D audio feedback for different control types,
    optionally suppressing spoken role labels to reduce redundancy.
    """

    # Translators: Script category for Sound Navigation commands
    scriptCategory = _("Sound Navigation")

    def __init__(self, *args, **kwargs):
        """Initialize the SoundNav add-on."""
        super().__init__(*args, **kwargs)

        # Initialize configuration
        init_configuration()

        # Initialize sound player with sounds directory
        sounds_dir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "sounds"
        )
        self.sound_player = SoundPlayer(sounds_dir)

        # Hook into speech system to suppress role labels
        # IMPORTANT: Must hook speech.speech.getPropertiesSpeech (the actual function NVDA uses internally)
        # Hooking only speech.getPropertiesSpeech (the re-export) doesn't intercept actual speech generation
        self._original_getSpeechTextForProperties = speech.speech.getPropertiesSpeech
        speech.speech.getPropertiesSpeech = self._hook_getSpeechTextForProperties
        # Also update the re-export at speech module level for compatibility
        speech.getPropertiesSpeech = speech.speech.getPropertiesSpeech

        # Hook into speech.speech.speak for browse mode sound support
        self._last_browse_element = None
        self._original_speech_speak = speech.speech.speak
        speech.speech.speak = self._hook_speech_speak
        speech.speak = speech.speech.speak

        # Register settings panel
        self.createMenu()

    def createMenu(self):
        """Register the settings panel in NVDA's settings dialog."""
        from gui.settingsDialogs import NVDASettingsDialog
        NVDASettingsDialog.categoryClasses.append(SoundNavSettingsPanel)

    def terminate(self):
        """Clean up when add-on is disabled."""
        # Restore original speech functions
        speech.speech.speak = self._original_speech_speak
        speech.speak = speech.speech.speak
        # Restore the original getPropertiesSpeech function
        speech.speech.getPropertiesSpeech = self._original_getSpeechTextForProperties
        speech.getPropertiesSpeech = speech.speech.getPropertiesSpeech

        # Remove settings panel
        from gui.settingsDialogs import NVDASettingsDialog
        try:
            NVDASettingsDialog.categoryClasses.remove(SoundNavSettingsPanel)
        except ValueError:
            # Already removed or not present
            pass

    def is_enabled(self):
        """
        Check if the add-on is currently enabled.

        Returns:
            True if enabled, False otherwise
        """
        return get_config("enabled")

    def _hook_getSpeechTextForProperties(self, reason, *args, **kwargs):
        """
        Hook function to intercept speech generation.

        Removes role labels from speech output when suppressRoleLabels is enabled.
        This prevents NVDA from saying "button", "link", etc. when sounds are played.

        Args:
            reason: The reason for speech output
            *args: Positional arguments passed to original function
            **kwargs: Keyword arguments, may contain 'role'

        Returns:
            Result from original speech function
        """
        # Only suppress if add-on is enabled and suppressRoleLabels is on
        if self.is_enabled() and get_config("suppressRoleLabels"):
            # Check if role is present in kwargs
            if 'role' in kwargs:
                # Remove the role to prevent it from being spoken
                del kwargs['role']

        # Call the original function with potentially modified arguments
        return self._original_getSpeechTextForProperties(reason, *args, **kwargs)

    def _hook_speech_speak(self, speechSequence, *args, **kwargs):
        """
        Hook for speech.speech.speak() to trigger browse mode sounds.

        Always calls the original speak function. Browse mode sound processing
        is wrapped in try/except to never break NVDA speech.
        """
        try:
            self._process_browse_mode_sound()
        except Exception:
            pass
        self._original_speech_speak(speechSequence, *args, **kwargs)

    def _process_browse_mode_sound(self):
        """
        Process browse mode navigation and play 3D positional sounds.

        Checks if we are in browse mode, gets the object at the caret position,
        and plays the appropriate sound if the element has changed.
        """
        if not self.is_enabled():
            return
        if not get_config("browseModeSound"):
            return

        focus = api.getFocusObject()
        ti = getattr(focus, 'treeInterceptor', None)
        if ti is None:
            return
        if getattr(ti, 'passThrough', False):
            return

        info = ti.makeTextInfo(textInfos.POSITION_CARET)
        obj = info.NVDAObjectAtStart
        if obj is None:
            return

        sound_filenames = get_sounds_for_object(obj)
        if not sound_filenames:
            self._last_browse_element = None
            return

        location = getattr(obj, 'location', None)
        location_tuple = tuple(location) if location is not None else ()
        element_key = (obj.role, location_tuple)

        if element_key == self._last_browse_element:
            return

        self._last_browse_element = element_key
        self.sound_player.play_for_object(obj, sound_filenames)

    def play_for_object(self, obj):
        """
        Play appropriate sounds for an NVDA object.

        Args:
            obj: NVDA object to play sounds for
        """
        if not self.is_enabled():
            return

        # Get list of sound filenames for this object
        sound_filenames = get_sounds_for_object(obj)

        # Play the sounds with 3D positioning
        if sound_filenames:
            self.sound_player.play_for_object(obj, sound_filenames)

    # ===== Event Handlers =====

    def event_gainFocus(self, obj, nextHandler):
        """
        Handle focus changes (keyboard navigation with Tab, arrows, etc.).

        Args:
            obj: The object that gained focus
            nextHandler: Function to call to propagate the event
        """
        # Reset browse mode deduplication when focus changes (e.g., Tab key)
        self._last_browse_element = None

        if self.is_enabled():
            try:
                self.play_for_object(obj)
            except Exception:
                # Silently ignore errors to prevent breaking NVDA
                pass

        # CRITICAL: Always call nextHandler to propagate the event
        nextHandler()

    def event_becomeNavigatorObject(self, obj, nextHandler, isFocus=False):
        """
        Handle NVDA object navigation (NVDA+numpad arrows).

        Args:
            obj: The object that became the navigator object
            nextHandler: Function to call to propagate the event
            isFocus: True if this object also has focus
        """
        # Only play sound if enabled and this is not also the focused object
        # (to avoid playing sound twice for the same object)
        if self.is_enabled() and not isFocus:
            try:
                self.play_for_object(obj)
            except Exception:
                # Silently ignore errors to prevent breaking NVDA
                pass

        # CRITICAL: Always call nextHandler to propagate the event
        nextHandler()

    # ===== Scripts (Keyboard Commands) =====

    @script(
        # Translators: Description for toggle Sound Navigation script
        description=_("Toggle Sound Navigation on/off"),
        gesture="kb:NVDA+shift+s"
    )
    def script_toggleSoundNav(self, gesture):
        """
        Toggle the add-on on/off.

        Keyboard shortcut: NVDA+Shift+S
        """
        enabled = get_config("enabled")
        set_config("enabled", not enabled)

        if not enabled:
            # Was disabled, now enabled
            # Translators: Message when Sound Navigation is enabled
            ui.message(_("Sound Navigation enabled"))
        else:
            # Was enabled, now disabled
            # Translators: Message when Sound Navigation is disabled
            ui.message(_("Sound Navigation disabled"))
