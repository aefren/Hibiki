#!/usr/bin/env python
"""Build script for Hibiki NVDA add-on"""

import os
import zipfile
import configparser
import subprocess
import glob

def get_version_from_manifest(manifest_path):
    """
    Read version from manifest.ini file.

    Args:
        manifest_path: Path to manifest.ini file

    Returns:
        Version string (e.g., "1.3.4")
    """
    config = configparser.ConfigParser()
    # NVDA manifest.ini files don't have section headers, so add a dummy one
    with open(manifest_path, 'r', encoding='utf-8') as f:
        config.read_string('[DEFAULT]\n' + f.read())
    return config.get('DEFAULT', 'version', fallback='unknown')

def compile_translations():
    """
    Compile all .po files to .mo files for the add-on.
    Uses pybabel (Babel) to compile translation catalogs.
    """
    print("Compiling translations...")
    po_files = glob.glob("hibiki/locale/*/LC_MESSAGES/*.po")

    if not po_files:
        print("No .po files found to compile.")
        return

    for po_file in po_files:
        mo_file = po_file.replace('.po', '.mo')
        print(f"  {po_file} -> {mo_file}")

        try:
            result = subprocess.run([
                'pybabel', 'compile',
                '--input-file', po_file,
                '--output-file', mo_file,
                '--use-fuzzy'
            ], check=True, capture_output=True, text=True)

            # Show statistics if available
            if result.stderr:
                print(f"    {result.stderr.strip()}")

        except FileNotFoundError:
            print("  Warning: pybabel not found. Install Babel: pip install Babel")
            print("  Skipping translation compilation.")
            break
        except subprocess.CalledProcessError as e:
            print(f"  Error compiling {po_file}: {e}")
            if e.stderr:
                print(f"  {e.stderr}")

    print()

def build_addon():
    """Build the .nvda-addon file (which is a ZIP archive)"""
    # Compile translations first
    compile_translations()

    source_dir = "hibiki"
    manifest_path = os.path.join(source_dir, "manifest.ini")

    # Read version from manifest.ini
    version = get_version_from_manifest(manifest_path)
    addon_name = f"Hibiki-{version}.nvda-addon"

    print(f"Building {addon_name}...")

    with zipfile.ZipFile(addon_name, 'w', zipfile.ZIP_DEFLATED) as addon_zip:
        # Walk through the hibiki directory
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # Calculate the archive name (relative to hibiki dir)
                arcname = os.path.relpath(file_path, source_dir)
                print(f"Adding: {arcname}")
                addon_zip.write(file_path, arcname)

    print(f"\nSuccessfully built {addon_name}")
    print(f"Size: {os.path.getsize(addon_name) / 1024:.1f} KB")

if __name__ == "__main__":
    build_addon()
