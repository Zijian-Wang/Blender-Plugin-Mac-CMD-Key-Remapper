# Mac Cmd Key Remapper for Blender

A Blender add-on for macOS that automatically replaces all `Ctrl` shortcuts with the `Cmd` (Command) key.

## Features

- Replace all `Ctrl` modifiers with `Cmd` (macOS only)
- Automatically backs up current keymap before modifying
- One-click restore to original keymap

## Installation

1. Download the repository as ZIP or clone it:
   git clone https://github.com/zijian-wang/blender-mac-cmd-remapper.git
2. In Blender, go to **Preferences → Add-ons → Install**
3. Select `mac_cmd_remapper.py`
4. Enable the add-on

## Usage

In **Preferences → Keymap** tab:

- Click **Remap Ctrl to Cmd** to apply changes
- Click **Revert to Original Keymap** to restore previous state

## Notes

- Backup is saved to:
  ~/Library/Application Support/Blender/{version}/config/keymap_backup.json

## License

MIT
