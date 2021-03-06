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
import Wintergatan.Physics.MarblePhysics_OOP

# customise path
#sys.path.append('C:/Users/marga/Wintergatan_git/simulation_team_physics_simulation/Source/Physics')
# customise path
#sys.path.append('C:/Users/marga/Wintergatan_git/simulation_team_physics_simulation/Source/Test/HelloWorldAddon')
#sys.path.append('C:/vsatish/MMX/Blender/Project/GitHub/simulation_team_physics_simulation/Source/Test/HelloWorldAddon')

import Wintergatan.Test.HelloWorldAddon.helloworld as hw

print(os.path.realpath(__file__))
path = os.getcwd()
print(path)

class ObjectMoveXY(bpy.types.Operator):
    """My Object Moving Script"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.move_x"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Move X by One Y by Two"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):        # execute() is called when running the operator.
        
        # Deselcting all objects
        bpy.ops.object.select_all(action='DESELECT')

        existing_object_coordinates = []
        
        scene = context.scene
        objs = scene.objects
        for obj in objs:
            
            obj_x = obj.location.x -1.0
            obj_y = obj.location.y -2.0
            obj_z = obj.location.z + 0.5
            
            if obj.name[:10] == 'SurfSphere':
            
                existing_object_coordinates.append([obj_x, obj_y, obj_z])
        
        new_sphere_coordinates = []
        new_cube_coordinates = []
        
        # The original script
        scene = context.scene
        objs = scene.objects
        for obj in objs:
            obj.location.x += -1.0
            obj_x = obj
            obj.location.y += -2.0
            obj.location.z += 0.5

            print(obj.location)
            
            print(obj.name)
            #print(obj.type)
            print(os.path.realpath(__file__)) # this shows that the file *seems* to be saved at another location, that's why the relative paths didn't work 
            hw.print_hello_world() # this shows whether the import of a simple file works
            

            if obj.name[:4] == 'Cube':
                
                marble_x = obj.location.x
                marble_y = obj.location.y
                marble_z = obj.location.z                
                new_marble_coord = [marble_x, marble_y, marble_z]
                
                if new_marble_coord not in new_sphere_coordinates:
                
                    new_sphere_coordinates.append([marble_x, marble_y, marble_z])
                
                new_cube_1_x = marble_x + 2.0
                new_cube_1_y = marble_y + 2.0
                new_cube_1_z = marble_z + 2.0                
                new_cube_1_coord = [new_cube_1_x, new_cube_1_y, new_cube_1_z]
                
                if new_cube_1_coord not in new_cube_coordinates:
                
                    new_cube_coordinates.append(new_cube_1_coord)
                
                new_cube_2_x = marble_x - 2.0
                new_cube_2_y = marble_y - 2.0
                new_cube_2_z = marble_z - 2.0
                new_cube_2_coord = [new_cube_2_x, new_cube_2_y, new_cube_2_z]
                
                if new_cube_2_coord not in new_cube_coordinates:
                    
                    new_cube_coordinates.append(new_cube_2_coord)
                
                new_cube_3_x = marble_x + 2.0
                new_cube_3_y = marble_y - 2.0
                new_cube_3_z = marble_z - 2.0
                new_cube_3_coord = [new_cube_3_x, new_cube_3_y, new_cube_3_z]             
                
                if new_cube_3_coord not in new_cube_coordinates:
                    
                    new_cube_coordinates.append(new_cube_3_coord)
                
                new_cube_4_x = marble_x - 2.0
                new_cube_4_y = marble_y + 2.0
                new_cube_4_z = marble_z - 2.0
                new_cube_4_coord = [new_cube_4_x, new_cube_4_y, new_cube_4_z]             
                
                if new_cube_4_coord not in new_cube_coordinates:
                    
                    new_cube_coordinates.append(new_cube_4_coord)
                
                new_cube_5_x = marble_x + 2.0
                new_cube_5_y = marble_y + 2.0
                new_cube_5_z = marble_z - 2.0
                new_cube_5_coord = [new_cube_5_x, new_cube_5_y, new_cube_5_z]             
                
                if new_cube_5_coord not in new_cube_coordinates:
                    
                    new_cube_coordinates.append(new_cube_5_coord)
                
                new_cube_6_x = marble_x - 2.0
                new_cube_6_y = marble_y + 2.0
                new_cube_6_z = marble_z + 2.0
                new_cube_6_coord = [new_cube_6_x, new_cube_6_y, new_cube_6_z]             
                
                if new_cube_6_coord not in new_cube_coordinates:
                    
                    new_cube_coordinates.append(new_cube_6_coord)
                
                new_cube_7_x = marble_x - 2.0
                new_cube_7_y = marble_y - 2.0
                new_cube_7_z = marble_z + 2.0
                new_cube_7_coord = [new_cube_7_x, new_cube_7_y, new_cube_7_z]             
                
                if new_cube_7_coord not in new_cube_coordinates:
                    
                    new_cube_coordinates.append(new_cube_7_coord)
                
                new_cube_8_x = marble_x + 2.0
                new_cube_8_y = marble_y - 2.0
                new_cube_8_z = marble_z + 2.0
                new_cube_8_coord = [new_cube_8_x, new_cube_8_y, new_cube_8_z]             
                
                if new_cube_8_coord not in new_cube_coordinates:
                    
                    new_cube_coordinates.append(new_cube_8_coord)
                                
                #bpy.data.objects.remove(obj)
                bpy.data.objects
                bpy.data.objects[obj.name].select_set(True)
                bpy.ops.object.delete()
                
        for coord_entry in new_cube_coordinates:
            
            print('Try to create cube')
            print(coord_entry)
            
            if coord_entry not in existing_object_coordinates:
                
                try:
                    bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(coord_entry[0], coord_entry[1], coord_entry[2]), scale=(1, 1, 1))
                except:
                    print('cube could not be created')
                    
            else:
                print('failed to create cube as space already occupied')
                
        for coord_entry in new_sphere_coordinates:
            
            print('Try to create sphere')
            print(coord_entry)
            
            if coord_entry not in existing_object_coordinates:
            
                try:
                    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1.0, calc_uvs=True, enter_editmode=False, align='WORLD', location=(coord_entry[0], coord_entry[1], coord_entry[2]), rotation=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0))
                    #alternate ways to create sphere
                    #bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1.0, calc_uvs=True, enter_editmode=False, align='WORLD', location=(coord_entry[0], coord_entry[1], coord_entry[2]), rotation=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0))
                    #bpy.ops.surface.primitive_nurbs_surface_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(coord_entry[0], coord_entry[1], coord_entry[2]), scale=(1.0, 1.0, 1.0))
                except:
                    print('sphere could not be created')
                    
            else:
                print('failed to create sphere as space already occupied')

        return {'FINISHED'}            # Lets Blender know the operator finished successfully.

def init_setup():
    # initial settings for operation
    # Create a particle system for all the objects to be added on to for reference
    #The process for working with standard particles is:
    #Create the mesh which will emit the particles.
    #Create one or more Particle Systems to emit from the mesh. Many times, multiple particle systems interact or merge with each other to achieve the overall desired effect.
    #Tailor each Particle System???s settings to achieve the desired effect.
    #Animate the base mesh and other particle meshes involved in the scene.
    #Define and shape the path and flow of the particles.
    #For Hair particle systems: Sculpt the emitter???s flow (cut the hair to length and comb it for example).
    #Make final render and do physics simulation(s), and tweak as needed.
    #bpy.context.space_data.context = 'PARTICLES'
    #bpy.ops.object.particle_system_add()
    #bpy.data.particles["ParticleSettings"].emit_from = 'VOLUME'
    return

def menu_func(self, context):
    self.layout.operator(ObjectMoveXY.bl_idname)

def register():
    init_setup()
    bpy.utils.register_class(ObjectMoveXY)
    bpy.types.VIEW3D_MT_object.append(menu_func)  # Adds the new operator to an existing menu.

def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    bpy.utils.unregister_class(ObjectMoveXY)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
	