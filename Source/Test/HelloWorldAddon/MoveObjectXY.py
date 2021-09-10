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
            existing_object_coordinates.append([obj.location.x, obj.location.y, obj.location.z])
            
            print(obj.name)
            #print(obj.type)
            print(os.path.realpath(__file__)) # this shows that the file *seems* to be saved at another location, that's why the relative paths didn't work 
            hw.print_hello_world() # this shows whether the import of a simple file works
            

            if obj.name[:4] == 'Cube':
                
                marble_x = obj.location.x
                marble_y = obj.location.y
                marble_z = obj.location.z
                
                new_sphere_coordinates.append([marble_x, marble_y, marble_z])
                
                #bpy.data.objects.remove(obj)
                bpy.data.objects[obj.name].select_set(True)
                bpy.ops.object.delete()
                
                new_cube_1_x = marble_x + 2.0
                new_cube_1_y = marble_y + 2.0
                new_cube_1_z = marble_z + 2.0
                
                new_cube_coordinates.append([new_cube_1_x, new_cube_1_y, new_cube_1_z])
                
                new_cube_2_x = marble_x - 2.0
                new_cube_2_y = marble_y - 2.0
                new_cube_2_z = marble_z - 2.0
                new_cube_coordinates.append([new_cube_2_x, new_cube_2_y, new_cube_2_z])
                
        for coord_entry in new_sphere_coordinates:
            
            print('Try to create sphere')
            print(coord_entry)
            
            if coord_entry  in existing_object_coordinates:
            
                try:
                    bpy.ops.surface.primitive_nurbs_surface_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(coord_entry[0], coord_entry[1], coord_entry[2]), scale=(1, 1, 1))
                    #alternate ways to create sphere
                    #bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=1.0, calc_uvs=True, enter_editmode=False, align='WORLD', location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), scale=(0.0, 0.0, 0.0))
                    #bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1.0, calc_uvs=True, enter_editmode=False, align='WORLD', location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), scale=(0.0, 0.0, 0.0))
                except:
                    print('sphere could not be created')
                
        for coord_entry in new_cube_coordinates:
            
            print('Try to create cube')
            print(coord_entry)
            
            if coord_entry not in existing_object_coordinates:
                
                try:
                    bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(coord_entry[0], coord_entry[1], coord_entry[2]), scale=(1, 1, 1))
                except:
                    print('cube could not be created')

        return {'FINISHED'}            # Lets Blender know the operator finished successfully.

def menu_func(self, context):
    self.layout.operator(ObjectMoveXY.bl_idname)

def register():
    bpy.utils.register_class(ObjectMoveXY)
    bpy.types.VIEW3D_MT_object.append(menu_func)  # Adds the new operator to an existing menu.

def unregister():
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    bpy.utils.unregister_class(ObjectMoveXY)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
