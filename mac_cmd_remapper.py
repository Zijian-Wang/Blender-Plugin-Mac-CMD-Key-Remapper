bl_info = {
    "name": "Ctrl to Cmd Keymap Converter (macOS)",
    "author": "ChatGPT & You",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Preferences > Add-ons",
    "description": "Convert all Ctrl shortcuts to Cmd (oskey) on macOS, with backup/restore.",
    "category": "Interface",
}

import bpy
import os
import platform

BACKUP_PATH = os.path.join(
    bpy.utils.user_resource('CONFIG'),
    "keyconfig_ctrl2cmd_backup.py"
)

def is_mouse_related(item):
    return item.type in {
        "LEFTMOUSE", "RIGHTMOUSE", "MIDDLEMOUSE",
        "WHEELUPMOUSE", "WHEELDOWNMOUSE", "MOUSEMOVE"
    }

def remap_ctrl_to_cmd():
    kc = bpy.context.window_manager.keyconfigs.user
    print("Starting keymap remap...")
    for keymap in kc.keymaps:
        for item in keymap.keymap_items:
            if item.ctrl and not item.oskey and not is_mouse_related(item):
                print(f"Remapping: {keymap.name} - {item.name}")
                item.ctrl = False
                item.oskey = True
    print("Remap complete.")
    bpy.ops.wm.save_userpref()

def backup_keymap():
    print("Backing up current keymap to:", BACKUP_PATH)
    bpy.ops.wm.save_userpref()
    
    kc = bpy.context.window_manager.keyconfigs.user
    with open(BACKUP_PATH, 'w', encoding='utf-8') as f:
        f.write("# Keymap backup by Ctrl-to-Cmd plugin\n")
        for km in kc.keymaps:
            for item in km.keymap_items:
                f.write(f"# {km.name}: {item.name} | type={item.type}, ctrl={item.ctrl}, oskey={item.oskey}, alt={item.alt}, shift={item.shift}\n")
    print("Backup complete.")

def restore_keymap():
    if not os.path.exists(BACKUP_PATH):
        print("Backup file not found:", BACKUP_PATH)
        return

    print("Restoring keymap from:", BACKUP_PATH)
    kc = bpy.context.window_manager.keyconfigs.user

    with open(BACKUP_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith("#") and "type=" in line:
            try:
                parts = line.strip().split("|")
                km_name = parts[0].split(":")[1].strip()
                key_type = parts[1].split(",")[0].split("=")[1].strip()

                # Parse modifier flags
                ctrl = "ctrl=True" in parts[1]
                oskey = "oskey=True" in parts[1]
                alt = "alt=True" in parts[1]
                shift = "shift=True" in parts[1]

                keymap = kc.keymaps.get(km_name)
                if not keymap:
                    continue

                for item in keymap.keymap_items:
                    if (item.type == key_type and
                        item.ctrl == False and item.oskey == True and
                        item.alt == alt and item.shift == shift):
                        item.ctrl = True
                        item.oskey = False

            except Exception as e:
                print("Error parsing line:", line)
                print("Exception:", e)

    bpy.ops.wm.save_userpref()
    print("Keymap restore complete.")

class KEYMAP_OT_remap_ctrl_to_cmd(bpy.types.Operator):
    bl_idname = "wm.remap_ctrl_to_cmd"
    bl_label = "Convert Ctrl to Cmd"

    def execute(self, context):
        remap_ctrl_to_cmd()
        self.report({'INFO'}, "Converted Ctrl to Cmd.")
        return {'FINISHED'}

class KEYMAP_OT_backup_keymap(bpy.types.Operator):
    bl_idname = "wm.backup_keymap"
    bl_label = "Backup Keymap"

    def execute(self, context):
        backup_keymap()
        self.report({'INFO'}, "Keymap backed up.")
        return {'FINISHED'}

class KEYMAP_OT_restore_keymap(bpy.types.Operator):
    bl_idname = "wm.restore_keymap"
    bl_label = "Restore Keymap"

    def execute(self, context):
        restore_keymap()
        self.report({'INFO'}, "Keymap restored.")
        return {'FINISHED'}

class KEYMAP_PT_ctrl2cmd_panel(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.label(text="Keymap Remap (macOS)")
        col.operator("wm.backup_keymap", icon='FILE_BACKUP')
        col.operator("wm.remap_ctrl_to_cmd", icon='TOOL_SETTINGS')
        col.operator("wm.restore_keymap", icon='FILE_REFRESH')
        col.label(text=f"Backup path: {BACKUP_PATH}", icon='INFO')

classes = (
    KEYMAP_OT_remap_ctrl_to_cmd,
    KEYMAP_OT_backup_keymap,
    KEYMAP_OT_restore_keymap,
    KEYMAP_PT_ctrl2cmd_panel,
)

def register():
    if platform.system() != 'Darwin':
        print("Warning: This plugin is intended for macOS only.")
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
