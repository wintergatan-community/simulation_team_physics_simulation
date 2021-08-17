# -*- coding: utf-8 -*-
"""
Main class for MMX Marbles Simulation.

@author: Vsk
Created: August 17 2021

"""
bl_info = {
    "name": "Marbles Simulator",
    "blender": (2, 80, 0),
    "category": "Object",
}

try:
    import os
    import bpy
    import numpy as np
    import Physics.MarblePhysics_OOP
except ModuleNotFoundError:
    print("ERROR: Module not found. Please install the numpy package before running.")
#    raise SystemExit

#   Add to path as needed.

#   need to check where to put the simuation and type
class MMXSimulate(bpy.types.Operator):
    """MMX Marbles Simulation Script"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.mmx_simulate"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Simulate Marbles"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):        # execute() is called when running the operator.

        # The original script
        scene = context.scene

        # Trigger MMX Simulation here

        print(os.path.realpath(__file__)) # this shows that the file *seems* to be saved at another location, that's why the relative paths didn't work 
        
        return {'FINISHED'}            # Lets Blender know the operator finished successfully.

def menu_func(self, context):
    self.layout.operator(MMXSimulate.bl_idname)

def register():
    bpy.utils.register_class(MMXSimulate)
    #bpy.types.VIEW3D_MT_mesh_add()  # Adds the new operator to an existing menu.
    bpy.types.VIEW3D_MT_object.append(menu_func)  #temporarily added

def unregister():
    bpy.utils.unregister_class(MMXSimulate)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
