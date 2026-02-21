# __init__.py - Main global plugin for Hibiki
# Part of Hibikiadd-on for NVDA

import os
import types
import globalPluginHandler
import addonHandler
import speech
import controlTypes
import ui
import api
import textInfos
from scriptHandler import script

from .soundPlayer import SoundPlayer
from .roleMapper import get_sounds_for_object, ROLE_SOUND_MAP
from .settingsPanel import init_configuration, get_config, set_config, HibikiSettingsPanel

addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    """
    Main global plugin for Hibikiadd-on.

    Provides spatial 3D audio feedback for different control types,
    optionally suppressing spoken role labels to reduce redundancy.

    Sound triggering hooks into NVDA's speech generation pipeline
    (getObjectPropertiesSpeech and getControlFieldSpeech) rather than
    the speech output (speak), ensuring sounds are synchronized with
    announcements and preventing phantom sounds from unrelated speech events.
    """

    # Translators: Script category for Hibiki commands
    scriptCategory = _("Hibiki")

    def __init__(self, *args, **kwargs):
        """Initialize the Hibikiadd-on."""
        super().__init__(*args, **kwargs)

        # Initialize configuration
        init_configuration()

        # Initialize sound player with sounds directory
        sounds_dir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "sounds"
        )
        self.sound_player = SoundPlayer(sounds_dir)

        # ── Hook 1: getPropertiesSpeech ──
        # Suppresses role/state labels from speech output when options are enabled.
        # This is the low-level function that generates text like "button", "link", etc.
        self._original_getSpeechTextForProperties = speech.speech.getPropertiesSpeech
        speech.speech.getPropertiesSpeech = self._hook_getSpeechTextForProperties
        speech.getPropertiesSpeech = speech.speech.getPropertiesSpeech

        # ── Hook 2: getObjectPropertiesSpeech ──
        # Triggers 3D sound for focus-based navigation (Tab, Shift+Tab, NVDA+numpad).
        # Called when NVDA generates speech for an object's properties.
        # Has direct access to the NVDA object → perfect for 3D positioning.
        self._original_getObjectPropertiesSpeech = speech.speech.getObjectPropertiesSpeech
        speech.speech.getObjectPropertiesSpeech = self._hook_getObjectPropertiesSpeech

        # ── Hook 3: getControlFieldSpeech ──
        # Triggers 3D sound for browse mode navigation (arrows, k, b, e, etc.).
        # Called when NVDA generates speech for control fields in virtual buffers.
        # Gets role from attrs dict; gets location from POSITION_CARET.
        self._original_getControlFieldSpeech = speech.speech.getControlFieldSpeech
        speech.speech.getControlFieldSpeech = self._hook_getControlFieldSpeech
        # Also update the re-export at speech module level for compatibility
        speech.getControlFieldSpeech = speech.speech.getControlFieldSpeech

        # Register settings panel
        self.createMenu()

    def createMenu(self):
        """Register the settings panel in NVDA's settings dialog."""
        from gui.settingsDialogs import NVDASettingsDialog
        NVDASettingsDialog.categoryClasses.append(HibikiSettingsPanel)

    def terminate(self):
        """Clean up when add-on is disabled."""
        # Restore all hooks
        speech.speech.getPropertiesSpeech = self._original_getSpeechTextForProperties
        speech.getPropertiesSpeech = speech.speech.getPropertiesSpeech

        speech.speech.getObjectPropertiesSpeech = self._original_getObjectPropertiesSpeech

        speech.speech.getControlFieldSpeech = self._original_getControlFieldSpeech
        speech.getControlFieldSpeech = speech.speech.getControlFieldSpeech

        # Remove settings panel
        from gui.settingsDialogs import NVDASettingsDialog
        try:
            NVDASettingsDialog.categoryClasses.remove(HibikiSettingsPanel)
        except ValueError:
            pass

    def is_enabled(self):
        """
        Check if the add-on is currently enabled.

        Returns:
            True if enabled, False otherwise
        """
        return get_config("enabled")

    # ===== Speech Generation Hooks =====

    def _hook_getSpeechTextForProperties(self, *args, **kwargs):
        """
        Hook for speech.speech.getPropertiesSpeech.

        Removes role and state labels from speech output when corresponding
        options are enabled. This prevents NVDA from saying "button", "link",
        "checked", "visited", etc.

        Uses *args/**kwargs to match the original function's signature exactly,
        avoiding TypeError when NVDA omits the 'reason' parameter.
        Wrapped in try/except to never break NVDA's speech pipeline.
        """
        try:
            if self.is_enabled():
                if get_config("suppressRoleLabels"):
                    if 'role' in kwargs:
                        del kwargs['role']
                if get_config("suppressStateLabels"):
                    if 'states' in kwargs:
                        del kwargs['states']
        except Exception:
            pass
        return self._original_getSpeechTextForProperties(*args, **kwargs)

    def _hook_getObjectPropertiesSpeech(self, obj, reason=controlTypes.OutputReason.QUERY, _prefixSpeechCommand=None, **allowedProperties):
        """
        Hook for speech.speech.getObjectPropertiesSpeech.

        Triggers 3D positional sound when NVDA generates speech for an object.
        This covers focus-based navigation (Tab, Shift+Tab) and object
        navigation (NVDA+numpad arrows).

        The object is available directly, so 3D positioning uses obj.location.
        Sound plays during speech generation, ensuring perfect synchronization.

        Args:
            obj: NVDA object whose properties are being spoken
            reason: Why the properties are being spoken
            _prefixSpeechCommand: Optional prefix command
            **allowedProperties: Which properties to include (role, states, etc.)
        """
        try:
            if self.is_enabled() and obj is not None:
                # Only play sound if NVDA is going to announce the role
                if allowedProperties.get('role', False):
                    sound_filenames = get_sounds_for_object(obj)
                    if sound_filenames:
                        self.sound_player.play_for_object(obj, sound_filenames)
        except Exception:
            pass

        return self._original_getObjectPropertiesSpeech(
            obj, reason, _prefixSpeechCommand, **allowedProperties
        )

    def _hook_getControlFieldSpeech(self, attrs, ancestorAttrs, fieldType, formatConfig=None, extraDetail=False, reason=None):
        """
        Hook for speech.speech.getControlFieldSpeech.

        Triggers 3D positional sound when NVDA generates speech for a control
        field in browse mode. This covers arrow keys, quick navigation keys
        (k, b, e, h, etc.), and other browse mode movements.

        Only activates when entering a control (fieldType starts with "start_"),
        not when exiting ("end_"). Gets the role from attrs dict and the
        screen location from the object at the virtual caret position.

        Args:
            attrs: Dictionary of control field attributes (role, states, etc.)
            ancestorAttrs: Attributes of ancestor controls
            fieldType: Type of field event (start_*, end_*)
            formatConfig: Document formatting configuration
            extraDetail: Whether extra detail is requested
            reason: Why the speech is being generated
        """
        try:
            if (
                self.is_enabled()
                and get_config("browseModeSound")
                and isinstance(fieldType, str)
                and fieldType == "start_addedToControlFieldStack"
            ):
                role = attrs.get("role")
                if role is not None and role in ROLE_SOUND_MAP:
                    states = attrs.get("states", set()) or set()
                    level = attrs.get("level", None)
                    # Create a lightweight object for get_sounds_for_object
                    elem = types.SimpleNamespace(role=role, states=states, level=level)
                    sound_filenames = get_sounds_for_object(elem)

                    if sound_filenames:
                        # Get object at caret for 3D positioning
                        obj = self._get_browse_mode_object()
                        if obj is not None:
                            self.sound_player.play_for_object(obj, sound_filenames)
        except Exception:
            pass

        return self._original_getControlFieldSpeech(
            attrs, ancestorAttrs, fieldType, formatConfig, extraDetail, reason
        )

    def _get_browse_mode_object(self):
        """
        Get the NVDA object at the current browse mode caret position.

        Used for 3D audio positioning when navigating in browse mode.
        The caret position is already updated when getControlFieldSpeech
        is called, so this returns the correct object.

        Returns:
            NVDA object at caret, or None if unavailable
        """
        try:
            focus = api.getFocusObject()
            ti = getattr(focus, 'treeInterceptor', None)
            if ti is None:
                return None
            info = ti.makeTextInfo(textInfos.POSITION_CARET)
            return info.NVDAObjectAtStart
        except Exception:
            return None

    def play_for_object(self, obj):
        """
        Play appropriate sounds for an NVDA object.

        Args:
            obj: NVDA object to play sounds for
        """
        if not self.is_enabled():
            return
        sound_filenames = get_sounds_for_object(obj)
        if sound_filenames:
            self.sound_player.play_for_object(obj, sound_filenames)

    # ===== Event Handlers =====

    def event_gainFocus(self, obj, nextHandler):
        """
        Handle focus changes (keyboard navigation with Tab, arrows, etc.).

        Sound is NOT played here — it is triggered by the
        getObjectPropertiesSpeech hook to ensure perfect synchronization.

        Args:
            obj: The object that gained focus
            nextHandler: Function to call to propagate the event
        """
        # CRITICAL: Always call nextHandler to propagate the event.
        # The sound will be triggered by _hook_getObjectPropertiesSpeech
        # when NVDA generates speech for this object.
        nextHandler()

    def event_becomeNavigatorObject(self, obj, nextHandler, isFocus=False):
        """
        Handle NVDA object navigation (NVDA+numpad arrows).

        Sound is NOT played here — it is triggered by the
        getObjectPropertiesSpeech hook to ensure perfect synchronization.

        Args:
            obj: The object that became the navigator object
            nextHandler: Function to call to propagate the event
            isFocus: True if this object also has focus
        """
        # CRITICAL: Always call nextHandler to propagate the event.
        nextHandler()

    # ===== Scripts (Keyboard Commands) =====

    @script(
        # Translators: Description for toggle Hibiki script
        description=_("Toggle Hibiki on/off"),
        gesture="kb:NVDA+shift+s"
    )
    def script_toggleHibiki(self, gesture):
        """
        Toggle the add-on on/off.

        Keyboard shortcut: NVDA+Shift+S
        """
        enabled = get_config("enabled")
        set_config("enabled", not enabled)

        if not enabled:
            # Was disabled, now enabled
            # Translators: Message when Hibiki is enabled
            ui.message(_("Hibiki enabled"))
        else:
            # Was enabled, now disabled
            # Translators: Message when Hibiki is disabled
            ui.message(_("Hibiki disabled"))
