# -*- coding: utf-8 -*-

# following this tutorial: https://docs.blender.org/manual/en/latest/advanced/scripting/addon_tutorial.html

bl_info = {
    "name": "Move X and Y Axis",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
import sys
import os

# With link of source folder to Blender Addon=>Wintergatan, no need for customising path
# customise path
#sys.path.append('C:/Users/marga/Wintergatan_git/simulation_team_physics_simulation/Source/Physics')
# customise path
#sys.path.append('C:/Users/marga/Wintergatan_git/simulation_team_physics_simulation/Source/Test/HelloWorldAddon')

# uncommenting and importing Physics crashes my blender
import Wintergatan.Physics.MarblePhysics_OOP as MarblePhysics_OOP
# this import works
import helloworld as hw

class ObjectMoveXY(bpy.types.Operator):
    """My Object Moving Script"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.move_x"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Move X by One Y by Two"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):        # execute() is called when running the operator.

        # The original script
        scene = context.scene
        for obj in scene.objects:
            obj.location.x += -1.0
            obj.location.y += -2.0
            obj.location.z += 0.5
            #print(os.path.realpath(__file__)) # this shows that the file *seems* to be saved at another location, that's why the relative paths didn't work 
            print(obj.name)
            hw.print_hello_world() # this shows whether the import of a simple file works
        
        

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
