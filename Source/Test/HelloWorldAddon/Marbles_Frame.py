# -*- coding: utf-8 -*-

# following this tutorial: https://docs.blender.org/manual/en/latest/advanced/scripting/addon_tutorial.html

bl_info = {
    "name": "Display Frame",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
import sys
import os
import numpy as np
import Wintergatan.Physics.MarblePhysics_OOP as MPOOP

# customise path
#sys.path.append('C:/Users/marga/Wintergatan_git/simulation_team_physics_simulation/Source/Physics')
# customise path
#sys.path.append('C:/Users/marga/Wintergatan_git/simulation_team_physics_simulation/Source/Test/HelloWorldAddon')
#sys.path.append('C:/vsatish/MMX/Blender/Project/GitHub/simulation_team_physics_simulation/Source/Test/HelloWorldAddon')

import Wintergatan.Test.HelloWorldAddon.helloworld as hw

print(os.path.realpath(__file__))
path = os.getcwd()
print(path)

class DisplayFrame(bpy.types.Operator):
    """My Frame Displaying Script"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.display_frame"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Display Frame"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):        # execute() is called when running the operator.
        
        # Deselcting all objects
        bpy.ops.object.select_all(action='DESELECT')
        
        selected_frame = 20
        x_marbles = 4
        y_marbles = 4
        marble_depth = 1
        n_mables = x_marbles*y_marbles*marble_depth
        
        physics_output = MPOOP.run_test_problem(0.4, [x_marbles, y_marbles, marble_depth])
        x_coordinates, y_coordinates, z_coordinates, marble_radius, nsteps = physics_output
        

        
        scene = context.scene
        objs = scene.objects
        for obj in objs:

            bpy.data.objects
            bpy.data.objects[obj.name].select_set(True)
            bpy.ops.object.delete()
                        
        for i in range(n_mables):
            print('n = ' + str(i))
            print('x = ' + str(x_coordinates[i][selected_frame]))
            print('y = ' + str(y_coordinates[i][selected_frame]))
            print('z = ' + str(z_coordinates[i][selected_frame]))
            
            try:
                bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=marble_radius, calc_uvs=True, enter_editmode=False, align='WORLD', location=(x_coordinates[i][selected_frame], y_coordinates[i][selected_frame], z_coordinates[i][selected_frame]), rotation=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0))
                #bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(x_coordinates[i][selected_fame], y_coordinates[i][selected_fame], z_coordinates[i][selected_fame]), scale=(1, 1, 1))
            except:
                print('marble could not be created')

        return {'FINISHED'}            # Lets Blender know the operator finished successfully.

def init_setup():
    # initial settings for operation
    # Create a particle system for all the objects to be added on to for reference
    #The process for working with standard particles is:
    #Create the mesh which will emit the particles.
    #Create one or more Particle Systems to emit from the mesh. Many times, multiple particle systems interact or merge with each other to achieve the overall desired effect.
    #Tailor each Particle System’s settings to achieve the desired effect.
    #Animate the base mesh and other particle meshes involved in the scene.
    #Define and shape the path and flow of the particles.
    #For Hair particle systems: Sculpt the emitter’s flow (cut the hair to length and comb it for example).
    #Make final render and do physics simulation(s), and tweak as needed.
    #bpy.context.space_data.context = 'PARTICLES'
    #bpy.ops.object.particle_system_add()
    #bpy.data.particles["ParticleSettings"].emit_from = 'VOLUME'
    return

def menu_func(self, context):
    self.layout.operator(DisplayFrame.bl_idname)

def register():
    init_setup()
    bpy.utils.register_class(DisplayFrame)
    bpy.types.VIEW3D_MT_object.append(menu_func)  # Adds the new operator to an existing menu.

def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    bpy.utils.unregister_class(DisplayFrame)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
	