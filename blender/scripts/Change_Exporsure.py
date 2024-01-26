import bpy

step = 0.02

def increase_exposure():
    scene = bpy.context.scene
    if hasattr(scene.view_settings, "exposure"):
        scene.view_settings.exposure += step
    else:
        scene.view_settings.use_exposure = True
        scene.view_settings.exposure = step
def decrease_exposure():
    scene = bpy.context.scene
    if hasattr(scene.view_settings, "exposure"):
        scene.view_settings.exposure -= step
    else:
        scene.view_settings.use_exposure = True
        scene.view_settings.exposure = -step

class IncreaseExposureOperator(bpy.types.Operator):
    bl_idname = "scene.increase_exposure"
    bl_label = "Increase Exposure"
    
    def execute(self, context):
        increase_exposure()
        return {'FINISHED'}

class DecreaseExposureOperator(bpy.types.Operator):
    bl_idname = "scene.decrease_exposure"
    bl_label = "Decrease Exposure"
    
    def execute(self, context):
        decrease_exposure()
        return {'FINISHED'}

def register():
    bpy.utils.register_class(IncreaseExposureOperator)
    bpy.utils.register_class(DecreaseExposureOperator)
    
    # Add keybindings for "X" and "Y" keys in the Image Editor
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name="Image", space_type='IMAGE_EDITOR')
    
    kmi = km.keymap_items.new("scene.increase_exposure", 'X', 'PRESS')
    kmi.active = True

    
    kmi = km.keymap_items.new("scene.decrease_exposure", 'Y', 'PRESS')
    kmi.active = True


def unregister():
    pass

if __name__ == "__main__":
    register()
