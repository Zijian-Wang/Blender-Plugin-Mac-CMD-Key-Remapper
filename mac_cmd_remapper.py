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

# def backup_keymap():
#     bpy.ops.wm.save_userpref()
#     bpy.ops.preferences.keyconfig_export(filepath=BACKUP_PATH)
#     print(f"Keymap backed up to: {BACKUP_PATH}")


# def restore_keymap():
#     if not os.path.exists(BACKUP_PATH):
#         print("Backup not found:", BACKUP_PATH)
#         return

#     bpy.ops.preferences.keyconfig_import(filepath=BACKUP_PATH)
#     bpy.ops.wm.save_userpref()
#     print(f"Keymap restored from: {BACKUP_PATH}")

class KEYMAP_OT_remap_ctrl_to_cmd(bpy.types.Operator):
    bl_idname = "wm.remap_ctrl_to_cmd"
    bl_label = "Convert Ctrl to Cmd"

    def execute(self, context):
        remap_ctrl_to_cmd()
        self.report({'INFO'}, "Converted Ctrl to Cmd.")
        return {'FINISHED'}

# class KEYMAP_OT_backup_keymap(bpy.types.Operator):
#     bl_idname = "wm.backup_keymap"
#     bl_label = "Backup Keymap"

#     def execute(self, context):
#         backup_keymap()
#         self.report({'INFO'}, "Keymap backed up.")
#         return {'FINISHED'}

# class KEYMAP_OT_restore_keymap(bpy.types.Operator):
#     bl_idname = "wm.restore_keymap"
#     bl_label = "Restore Original Keymap"

#     def execute(self, context):
#         restore_keymap()
#         self.report({'INFO'}, "Restored original keymap.")
#         return {'FINISHED'}

class KEYMAP_PT_ctrl2cmd_panel(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.label(text="Keymap Remap (macOS)")
        # col.operator("wm.backup_keymap", icon='FILE_BACKUP')
        col.operator("wm.remap_ctrl_to_cmd", icon='TOOL_SETTINGS')
        # col.operator("wm.restore_keymap", icon='FILE_REFRESH')
        col.label(text=f"Backup path: {BACKUP_PATH}", icon='INFO')

classes = (
    KEYMAP_OT_remap_ctrl_to_cmd,
    # KEYMAP_OT_backup_keymap,
    # KEYMAP_OT_restore_keymap,
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
