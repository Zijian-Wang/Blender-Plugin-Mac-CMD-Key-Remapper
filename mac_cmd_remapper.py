bl_info = {
    "name": "Ctrl to Cmd Keymap Converter (macOS)",
    "author": "ZJ Design Lab",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "location": "Preferences > Add-ons",
    "description": "Convert all Ctrl shortcuts to Cmd (oskey) on macOS.",
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

class KEYMAP_OT_remap_ctrl_to_cmd(bpy.types.Operator):
    bl_idname = "wm.remap_ctrl_to_cmd"
    bl_label = "Convert Ctrl to Cmd"

    def execute(self, context):
        remap_ctrl_to_cmd()
        self.report({'INFO'}, "Converted Ctrl to Cmd.")
        return {'FINISHED'}

class KEYMAP_PT_ctrl2cmd_panel(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.label(text="Keymap Remap (macOS)")
        col.operator("wm.remap_ctrl_to_cmd", icon='TOOL_SETTINGS')
        col.label(text=f"Backup path: {BACKUP_PATH}", icon='INFO')

classes = (
    KEYMAP_OT_remap_ctrl_to_cmd,
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
