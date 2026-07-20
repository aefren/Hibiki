# __init__.py - Main global plugin for Hibiki
# Part of Hibiki add-on for NVDA

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
from .roleMapper import get_sounds_for_object, ROLE_SOUND_MAP, STATE_SOUND_MAP
from .settingsPanel import init_configuration, get_config, set_config, HibikiSettingsPanel

addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    """
    Main global plugin for Hibiki add-on.

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
        """Initialize the Hibiki add-on."""
        super().__init__(*args, **kwargs)

        # Initialize configuration
        init_configuration()

        # Initialize sound player with sounds directory
        sounds_dir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "sounds"
        )
        self.sound_player = SoundPlayer(sounds_dir)

        # State shared by the speech hooks below. Must exist before any hook
        # is installed, since speech can fire between installations.
        self._speaking_textinfo = None
        self._in_control_field_speech = False

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

        # ── Hook 4: speakTextInfo ──
        # Records the text range currently being announced. Browse mode uses it
        # to position sounds on the range actually being spoken, which is not
        # always where the virtual caret is (see _resolve_control_field_object).
        self._original_speakTextInfo = speech.speech.speakTextInfo
        speech.speech.speakTextInfo = self._hook_speakTextInfo
        speech.speakTextInfo = speech.speech.speakTextInfo

        # Register settings panel
        self.createMenu()

    def createMenu(self):
        """Register the settings panel in NVDA's settings dialog."""
        from gui.settingsDialogs import NVDASettingsDialog
        if HibikiSettingsPanel not in NVDASettingsDialog.categoryClasses:
            NVDASettingsDialog.categoryClasses.append(HibikiSettingsPanel)

    def terminate(self):
        """Clean up when add-on is disabled."""
        # Restore all hooks
        speech.speech.getPropertiesSpeech = self._original_getSpeechTextForProperties
        speech.getPropertiesSpeech = speech.speech.getPropertiesSpeech

        speech.speech.getObjectPropertiesSpeech = self._original_getObjectPropertiesSpeech

        speech.speech.getControlFieldSpeech = self._original_getControlFieldSpeech
        speech.getControlFieldSpeech = speech.speech.getControlFieldSpeech

        speech.speech.speakTextInfo = self._original_speakTextInfo
        speech.speakTextInfo = speech.speech.speakTextInfo

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

        Hides role and state labels from speech output when the corresponding
        options are enabled, but only where a sound actually replaces the label.
        A role or state Hibiki has no sound for stays spoken, otherwise the
        information would be lost entirely.

        Uses *args/**kwargs to match the original function's signature exactly,
        avoiding TypeError when NVDA omits the 'reason' parameter.
        Wrapped in try/except to never break NVDA's speech pipeline.
        """
        try:
            if self.is_enabled() and self._sounds_replace_labels_here():
                if get_config("suppressRoleLabels"):
                    self._suppress_role_label(kwargs)
                if get_config("suppressStateLabels"):
                    self._suppress_state_labels(kwargs)
        except Exception:
            pass
        return self._original_getSpeechTextForProperties(*args, **kwargs)

    def _sounds_replace_labels_here(self):
        """
        Whether a sound actually stands in for suppressed labels right now.

        Browse mode control field speech only gets sounds while the
        browseModeSound option is on; hiding labels there without a sound
        playing would leave controls unannounced entirely.
        """
        if self._in_control_field_speech:
            return get_config("browseModeSound")
        return True

    def _suppress_role_label(self, propertyValues):
        """
        Hide the spoken role label when Hibiki has a sound for that role.

        The role is moved to the private '_role' key rather than deleted:
        getPropertiesSpeech still needs the role to decide how to phrase the
        states and whether the value should be spoken at all, but it only
        speaks the role name when the public 'role' key is present.

        Args:
            propertyValues: The kwargs dict passed to getPropertiesSpeech (mutated in place)
        """
        role = propertyValues.get('role')
        if role is None or role not in ROLE_SOUND_MAP:
            # No sound for this role, so keep the spoken label.
            return
        propertyValues.setdefault('_role', role)
        del propertyValues['role']

    def _suppress_state_labels(self, propertyValues):
        """
        Hide the spoken state labels Hibiki has sounds for, keeping the rest.

        States without a sound (unavailable, read only, required, invalid
        entry, ...) carry information no sound conveys, so they stay spoken.

        The full state set is preserved under the private '_states' key, which
        getPropertiesSpeech uses to work out the *negative* states ("not
        checked"). Dropping it would make NVDA report negative states based on
        the filtered set and announce them incorrectly.

        Args:
            propertyValues: The kwargs dict passed to getPropertiesSpeech (mutated in place)
        """
        states = propertyValues.get('states')
        if not states:
            return
        remaining = {state for state in states if state not in STATE_SOUND_MAP}
        if len(remaining) == len(states):
            # Nothing here has a sound, so leave the speech untouched.
            return
        propertyValues.setdefault('_states', states)
        propertyValues['states'] = remaining

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
                        # Resolve the control being announced for 3D positioning
                        obj = self._resolve_control_field_object(attrs)
                        if obj is not None:
                            self.sound_player.play_for_object(obj, sound_filenames)
        except Exception:
            pass

        # Flag the context while NVDA generates the field's speech: the role
        # and state labels come from getPropertiesSpeech calls made inside the
        # original function, and the suppression hook needs to know they belong
        # to browse mode (see _sounds_replace_labels_here).
        previous = self._in_control_field_speech
        self._in_control_field_speech = True
        try:
            return self._original_getControlFieldSpeech(
                attrs, ancestorAttrs, fieldType, formatConfig, extraDetail, reason
            )
        finally:
            self._in_control_field_speech = previous

    def _hook_speakTextInfo(self, *args, **kwargs):
        """
        Hook for speech.speech.speakTextInfo.

        Remembers the text range being announced while the original function
        runs, so getControlFieldSpeech can position sounds on it. The previous
        value is restored afterwards to stay correct if calls ever nest.
        """
        previous = self._speaking_textinfo
        try:
            self._speaking_textinfo = args[0] if args else kwargs.get("info")
        except Exception:
            self._speaking_textinfo = None
        try:
            return self._original_speakTextInfo(*args, **kwargs)
        finally:
            self._speaking_textinfo = previous

    def _resolve_control_field_object(self, attrs):
        """
        Find the NVDA object a browse mode control field belongs to.

        The virtual caret cannot be trusted here: quick navigation
        (b, shift+b, h, k, ...) calls item.report() *before* item.moveTo()
        (NVDA issue #8831), so while this runs the caret still sits on the
        previously visited control. Positioning from the caret would play every
        sound one step behind the control being announced.

        Strategies, most to least precise:
          1. The control field's own identifier, which names the exact control
             even when several share one line.
          2. The start of the text range currently being spoken, which is the
             navigation target for browse modes without such identifiers.
          3. The caret, as a last resort.

        Args:
            attrs: The control field attributes dict

        Returns:
            NVDA object to position the sound at, or None if unavailable
        """
        obj = self._object_from_control_identifier(attrs)
        if obj is not None:
            return obj

        info = self._speaking_textinfo
        if info is not None:
            try:
                obj = info.NVDAObjectAtStart
                if obj is not None:
                    return obj
            except Exception:
                pass

        return self._get_browse_mode_object()

    def _object_from_control_identifier(self, attrs):
        """
        Resolve a control field to its NVDA object via its virtual buffer id.

        Virtual buffers tag every control field with the document handle and
        node id it came from, which maps straight back to the real object.
        Browse modes that are not virtual buffers do not provide these, in
        which case the caller falls back to another strategy.

        Args:
            attrs: The control field attributes dict

        Returns:
            NVDA object, or None if the identifier is unavailable or stale
        """
        try:
            doc_handle = attrs.get("controlIdentifier_docHandle")
            node_id = attrs.get("controlIdentifier_ID")
            if doc_handle is None or node_id is None:
                return None
            interceptor = self._get_tree_interceptor()
            resolve = getattr(interceptor, "getNVDAObjectFromIdentifier", None)
            if resolve is None:
                return None
            return resolve(int(doc_handle), int(node_id))
        except Exception:
            return None

    def _get_tree_interceptor(self):
        """
        Get the tree interceptor owning the document being announced.

        Prefers the one attached to the text range being spoken, since the
        focus may have moved on by the time this runs.

        Returns:
            Tree interceptor, or None if unavailable
        """
        info = self._speaking_textinfo
        interceptor = getattr(info, "obj", None) if info is not None else None
        if interceptor is not None and hasattr(interceptor, "getNVDAObjectFromIdentifier"):
            return interceptor
        try:
            focus = api.getFocusObject()
            return getattr(focus, "treeInterceptor", None)
        except Exception:
            return None

    def _get_browse_mode_object(self):
        """
        Get the NVDA object at the current browse mode caret position.

        Last-resort fallback for 3D positioning: the caret lags behind during
        quick navigation, so prefer _resolve_control_field_object.

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
