bl_info = {
    "name": "Mac Cmd Key Remapper with Backup",
    "blender": (2, 80, 0),
    "category": "Interface",
    "author": "Your Name",
    "version": (1, 1),
    "description": "Replace Ctrl with Cmd in keymaps on macOS, with backup and revert support"
}

import bpy
import platform
import os
import json

BACKUP_PATH = os.path.join(bpy.utils.user_resource('CONFIG'), "keymap_backup.json")

def backup_keymap():
    kc = bpy.context.window_manager.keyconfigs.user
    keymap_data = []

    for keymap in kc.keymaps:
        for item in keymap.keymap_items:
            keymap_data.append({
                'idname': item.idname,
                'type': item.type,
                'value': item.value,
                'ctrl': item.ctrl,
                'alt': item.alt,
                'shift': item.shift,
                'oskey': item.oskey,
                'keymap_name': keymap.name,
                'keymap_space_type': keymap.space_type,
                'keymap_region_type': keymap.region_type,
            })

    with open(BACKUP_PATH, 'w') as f:
        json.dump(keymap_data, f, indent=2)

def remap_ctrl_to_cmd():
    kc = bpy.context.window_manager.keyconfigs.user

    for keymap in kc.keymaps:
        for item in keymap.keymap_items:
            if item.ctrl and not item.oskey:
                item.ctrl = False
                item.oskey = True

def restore_keymap():
    if not os.path.exists(BACKUP_PATH):
        return False

    with open(BACKUP_PATH, 'r') as f:
        keymap_data = json.load(f)

    kc = bpy.context.window_manager.keyconfigs.user

    for keymap in kc.keymaps:
        for item in list(keymap.keymap_items):
            keymap.keymap_items.remove(item)

    for entry in keymap_data:
        km = kc.keymaps.get(entry['keymap_name'])
        if not km:
            continue
        try:
            kmi = km.keymap_items.new(
                idname=entry['idname'],
                type=entry['type'],
                value=entry['value']
            )
            kmi.ctrl = entry['ctrl']
            kmi.alt = entry['alt']
            kmi.shift = entry['shift']
            kmi.oskey = entry['oskey']
        except:
            pass  # Ignore if fails to restore a specific keymap item

    return True

class RemapCtrlToCmdOperator(bpy.types.Operator):
    bl_idname = "wm.remap_ctrl_to_cmd"
    bl_label = "Remap Ctrl to Cmd"
    bl_description = "Replace all Ctrl shortcuts with Cmd (macOS only)"

    def execute(self, context):
        if platform.system() != 'Darwin':
            self.report({'WARNING'}, "This only works on macOS")
            return {'CANCELLED'}

        backup_keymap()
        remap_ctrl_to_cmd()
        self.report({'INFO'}, "Remapped Ctrl to Cmd and backup saved")
        return {'FINISHED'}

class RestoreOriginalKeymapOperator(bpy.types.Operator):
    bl_idname = "wm.restore_keymap_backup"
    bl_label = "Revert to Original Keymap"
    bl_description = "Restore keymap from backup"

    def execute(self, context):
        if restore_keymap():
            self.report({'INFO'}, "Original keymap restored")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "No backup found")
            return {'CANCELLED'}

# class CmdKeyRemapPanel(bpy.types.Panel):
#     bl_label = "Mac Cmd Key Remapper"
#     bl_idname = "VIEW3D_PT_cmd_key_remapper"
#     bl_space_type = 'PREFERENCES'
#     bl_region_type = 'WINDOW'
#     bl_context = "keymap"

#     def draw(self, context):
#         layout = self.layout
#         layout.operator("wm.remap_ctrl_to_cmd", icon='KEYINGSET')
#         layout.operator("wm.restore_keymap_backup", icon='FILE_REFRESH')

class CmdKeyRemapPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        layout.label(text="Remap and Restore Keymap")
        layout.operator("wm.remap_ctrl_to_cmd", icon='KEYINGSET')
        layout.operator("wm.restore_keymap_backup", icon='FILE_REFRESH')

def register():
    bpy.utils.register_class(CmdKeyRemapPreferences)
    bpy.utils.register_class(RemapCtrlToCmdOperator)
    bpy.utils.register_class(RestoreOriginalKeymapOperator)
    # （你原来的面板 VIEW3D_PT_cmd_key_remapper 可删或保留）

def unregister():
    bpy.utils.unregister_class(CmdKeyRemapPreferences)
    bpy.utils.unregister_class(RemapCtrlToCmdOperator)
    bpy.utils.unregister_class(RestoreOriginalKeymapOperator)

# def unregister():
#     bpy.utils.unregister_class(RemapCtrlToCmdOperator)
#     bpy.utils.unregister_class(RestoreOriginalKeymapOperator)
#     bpy.utils.unregister_class(CmdKeyRemapPanel)

if __name__ == "__main__":
    register()
