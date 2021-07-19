# -*- coding: utf-8 -*-

# following this tutorial: https://docs.blender.org/manual/en/latest/advanced/scripting/addon_tutorial.html

bl_info = {
    "name": "Move X and Y Axis",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy


class ObjectMoveXY(bpy.types.Operator):
    """My Object Moving Script"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.move_x"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Move X by One Y by Two"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):        # execute() is called when running the operator.

        # The original script
        scene = context.scene
        for obj in scene.objects:
            obj.location.x += 1.0
            obj.location.y += 2.0

        return {'FINISHED'}            # Lets Blender know the operator finished successfully.

def menu_func(self, context):
    self.layout.operator(ObjectMoveXY.bl_idname)

def register():
    bpy.utils.register_class(ObjectMoveXY)
    bpy.types.VIEW3D_MT_object.append(menu_func)  # Adds the new operator to an existing menu.

def unregister():
    bpy.utils.unregister_class(ObjectMoveXY)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
