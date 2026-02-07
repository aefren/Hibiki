# -*- coding: utf-8 -*-
# soundPlayer.py - 3D audio playback system
# Part of SoundNav add-on for NVDA

import os
import api
from .camlorn_audio import init_camlorn_audio, Sound3D

# Audio positioning constants
AUDIO_WIDTH = 25.0  # Width of the audio space
AUDIO_DEPTH = 5.0   # Depth (z-axis) for all sounds

class SoundPlayer:
    """
    Manages loading and playing 3D positional sounds.

    Sounds are positioned in 3D space based on the on-screen location
    of NVDA objects, providing spatial audio feedback.
    """

    def __init__(self, sounds_directory):
        """
        Initialize the sound player and preload all sounds.

        Args:
            sounds_directory: Path to directory containing WAV sound files
        """
        # Initialize the 3D audio engine
        init_camlorn_audio()

        # Dictionary to store loaded sounds
        self.sounds = {}

        # Import role and state mappings
        from .roleMapper import ROLE_SOUND_MAP, STATE_SOUND_MAP

        # Preload all role sounds
        for role, filename in ROLE_SOUND_MAP.items():
            sound_path = os.path.join(sounds_directory, filename)
            if os.path.exists(sound_path):
                try:
                    sound = Sound3D(sound_path)
                    # Set rolloff_factor to 0 to disable volume falloff with distance
                    # This ensures consistent volume regardless of position
                    sound.set_rolloff_factor(0)
                    self.sounds[filename] = sound
                except Exception as e:
                    # Silently skip sounds that fail to load
                    pass

        # Preload all state sounds (avoiding duplicates)
        for state, filename in STATE_SOUND_MAP.items():
            sound_path = os.path.join(sounds_directory, filename)
            if os.path.exists(sound_path) and filename not in self.sounds:
                try:
                    sound = Sound3D(sound_path)
                    sound.set_rolloff_factor(0)
                    self.sounds[filename] = sound
                except Exception as e:
                    # Silently skip sounds that fail to load
                    pass

    def play_for_object(self, obj, sound_filenames):
        """
        Play sounds with 3D positioning based on object's screen location.

        The object's screen coordinates are mapped to a 3D audio space:
        - X axis: left (-AUDIO_WIDTH) to right (+AUDIO_WIDTH)
        - Y axis: top to bottom (inverted, accounting for aspect ratio)
        - Z axis: constant depth (AUDIO_DEPTH)

        Args:
            obj: NVDA object to play sounds for
            sound_filenames: List of sound filenames to play
        """
        # Get desktop dimensions for normalization
        desktop = api.getDesktopObject()
        desktop_max_x = desktop.location[2]  # Width
        desktop_max_y = desktop.location[3]  # Height
        desktop_aspect = float(desktop_max_y) / float(desktop_max_x)

        # Calculate center position of object
        if obj.location is not None:
            # Object has a location, use its center point
            obj_x = obj.location[0] + (obj.location[2] / 2.0)
            obj_y = obj.location[1] + (obj.location[3] / 2.0)
        else:
            # No location available, default to center of screen
            obj_x = desktop_max_x / 2.0
            obj_y = desktop_max_y / 2.0

        # Convert screen coordinates to 3D audio space
        # X: normalize to 0-1, scale to -AUDIO_WIDTH to +AUDIO_WIDTH
        position_x = (obj_x / desktop_max_x) * (AUDIO_WIDTH * 2) - AUDIO_WIDTH

        # Y: normalize to 0-1, scale by aspect ratio, adjust for top-down coordinate system
        position_y = (obj_y / desktop_max_y) * (desktop_aspect * AUDIO_WIDTH * 2) - (desktop_aspect * AUDIO_WIDTH)
        position_y *= -1  # Invert Y axis (screen coords are top-down, audio is bottom-up)

        # Z: constant depth for all sounds
        position_z = AUDIO_DEPTH * -1

        # Play each sound with the calculated position
        for filename in sound_filenames:
            if filename in self.sounds:
                try:
                    self.sounds[filename].set_position(position_x, position_y, position_z)
                    self.sounds[filename].play()
                except Exception as e:
                    # Silently skip sounds that fail to play
                    pass
