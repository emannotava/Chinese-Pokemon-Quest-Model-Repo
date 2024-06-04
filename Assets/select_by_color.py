import bpy
from mathutils import Color

bl_info = {
    'name': 'Select By Color',
    'author': 'Tamas Kemenczy, updated for 2.8 by Piotr Zgodziński, updated for 3.6.1 by ChatGPT',
    'version': (0, 3),
    'blender': (3, 6, 1),
    'location': 'View3D > Select > Select By Color',
    'description': 'Select all faces with the same vertex color of the selected face',
    'category': 'Mesh'
}

def select_by_color(obj, threshold=0.01):
    # ensure we are in edit mode
    if bpy.context.mode != 'EDIT_MESH':
        bpy.ops.object.mode_set(mode='EDIT')

    bpy.ops.object.mode_set(mode='OBJECT')

    if not obj.data.vertex_colors.active:
        return

    colors = obj.data.vertex_colors.active.data

    selected_polygons = [p for p in obj.data.polygons if p.select]

    if selected_polygons:
        p = selected_polygons[0]
        r = g = b = 0
        for i in p.loop_indices:
            r1, g1, b1, a1 = colors[i].color
            r += r1
            g += g1
            b += b1
        r /= p.loop_total
        g /= p.loop_total
        b /= p.loop_total
        target = Color((r, g, b))

        for p in obj.data.polygons:
            r = g = b = 0
            for i in p.loop_indices:
                r1, g1, b1, a1 = colors[i].color
                r += r1
                g += g1
                b += b1
            r /= p.loop_total
            g /= p.loop_total
            b /= p.loop_total
            source = Color((r, g, b))

            if (abs(source.r - target.r) < threshold and
                abs(source.g - target.g) < threshold and
                abs(source.b - target.b) < threshold):

                p.select = True

    bpy.ops.object.mode_set(mode='EDIT')

class SelectByColor(bpy.types.Operator):
    bl_label = 'Select By Color'
    bl_idname = 'mesh.select_by_color'
    bl_options = {'REGISTER', 'UNDO'}
    threshold: bpy.props.FloatProperty(name='Threshold', default=0.01, min=0.001, max=1.0, step=1)

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and obj.type == 'MESH')

    def execute(self, context):
        select_by_color(context.active_object, self.threshold)
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator_context = "INVOKE_DEFAULT"
    self.layout.operator(SelectByColor.bl_idname, text='Select By Color')

def register():
    bpy.utils.register_class(SelectByColor)
    bpy.types.VIEW3D_MT_select_edit_mesh.append(menu_func)

def unregister():
    bpy.utils.unregister_class(SelectByColor)
    bpy.types.VIEW3D_MT_select_edit_mesh.remove(menu_func)

if __name__ == "__main__":
    register()
