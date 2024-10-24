bl_info = {
    "name": "Cubical Bounds",
    "blender": (3, 6, 1),
    "category": "Object",
}

import bpy
from mathutils import Vector

class OBJECT_OT_place_cubical_bounds(bpy.types.Operator):
    """Place Cubes with the same dimensions and center as selected objects"""
    bl_idname = "object.place_cubical_bounds"
    bl_label = "Place Cubical Bounds"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_objects = context.selected_objects  # Get selected objects

        for obj in selected_objects:
            # Ensure we're only working on visible mesh objects
            if obj.type == 'MESH' and obj.visible_get():
                # Get the object's world transformation matrix
                matrix_world = obj.matrix_world
                
                # Get the object's dimensions directly
                dimensions = obj.dimensions
                
                # Get the object's world position (location)
                location = obj.location
                
                # Add a cube
                bpy.ops.mesh.primitive_cube_add(size=1, align='WORLD')
                cube = context.active_object
                
                # Set the cube's dimensions to match the object's dimensions
                cube.dimensions = dimensions
                
                # Get the bounding box of the object in local space and apply the world transformation
                bbox_corners = [matrix_world @ Vector(corner) for corner in obj.bound_box]

                # Calculate the center of the bounding box in world space
                bbox_center = sum(bbox_corners, Vector()) / 8
                #bpy.context.object.location[0] = 0.3
                # Move the cube to the object's location
                #cube.matrix_world.translation = bbox_center
                #cube.matrix_world = matrix_world.copy()
                #cube.matrix_world.translation = bbox_center  # Ensure it is at the physical center
                cube.location[0] = location[0]

                # Apply the scale of the cube
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        return {'FINISHED'}


def draw_item(self, context):
    layout = self.layout
    layout.operator("object.place_cubical_bounds", text="Cubical Bounds")


def register():
    bpy.utils.register_class(OBJECT_OT_place_cubical_bounds)
    
    # Add the operator to the "Add" menu in Object Mode
    bpy.types.VIEW3D_MT_add.append(draw_item)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_place_cubical_bounds)
    
    # Remove the operator from the "Add" menu
    bpy.types.VIEW3D_MT_add.remove(draw_item)


if __name__ == "__main__":
    register()
