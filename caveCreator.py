import bmesh
import bpy
bl_info = {
    "name": "Cave Creator",
    "author": "Mahdi Gholami",
    "version": (1, 0, 0),
    "blender": (2, 90, 0),
    "location": "View3D > Toolshelf > Cave Creator",
    "description": "Creating Cave Spline",
    "category": "Mesh",
}


class CC_OT_cave(bpy.types.Operator):
    bl_idname = "mesh.cave_creator"
    bl_label = "Cave Creator"
    bl_options = {'REGISTER', 'UNDO'}

    road_percent: bpy.props.IntProperty(
        name="Road Percent",
        description="Percent of the road from hole cave",
        default=30,
        min=0,
        max=50,
    )

    roof_subdiv: bpy.props.IntProperty(
        name="Roof Subdivide",
        description="Number of cut you want for your cave's roof",
        default=4,
        min=0,
    )

    roof_noise: bpy.props.FloatProperty(
        name="Roof Noise Power",
        description="Power of your cave's noise",
        default=1.100,
        min=0.000,
    )

    roof_smoothness: bpy.props.FloatProperty(
        name="Roof Noise Smoothness",
        description="Smoothness of your cave's noise",
        default=0.000,
        min=0.000,
        max=1.000,
    )

    roof_along_normal: bpy.props.FloatProperty(
        name="Roof Along Normal",
        description="Set how much you want noise, effect in direction of vertext's normal",
        default=1.000,
        min=0.000,
        max=1.000,
    )

    roof_noise_seed: bpy.props.IntProperty(
        name="Roof Noise Seed",
        description="Seed of random noise for your cave's roof",
        default=0,
        min=0,
    )

    shade_smooth: bpy.props.BoolProperty(
        name="Shade Smooth",
        description="Check for smooth shade and uncheck for flat shade",
        default=1,
    )

    def execute(self, context):
        bpy.ops.mesh.primitive_cylinder_add(
            location=(0, 0, 0), rotation=(1.5708, 0, 0))
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_mode(type='FACE')
        bpy.ops.mesh.select_face_by_sides(number=4, type='NOTEQUAL')
        bpy.ops.mesh.delete(type='FACE')
        bpy.ops.mesh.select_mode(type='VERT')

        obj = bpy.context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        bm.faces.active = None
        range = 2
        road_y = (self.road_percent * range) / 100 - 1
        for v in bm.verts:
            if v.co.y <= road_y:
                v.co.y = road_y
        bmesh.update_edit_mesh(me, True)

        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        obj.data.vertices[0].select = True
        bpy.ops.object.mode_set(mode='EDIT')
        th = (100 - self.road_percent)/100
        bpy.ops.mesh.select_similar(threshold=th)
        bpy.ops.mesh.subdivide(
            number_cuts=self.roof_subdiv,
            smoothness=self.roof_smoothness,
            ngon=False,
            quadcorner='STRAIGHT_CUT',
            fractal=self.roof_noise,
            fractal_along_normal=self.roof_along_normal,
            seed=self.roof_noise_seed
        )
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        if self.shade_smooth:
            bpy.ops.object.shade_smooth()
        else:
            bpy.ops.object.shade_flat()
        return {'FINISHED'}


class CC_PT_cave_creator(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Cave Creator"
    bl_label = "Information"

    def draw(self, context):
        layout = self.layout
        layout.operator('mesh.cave_creator',
                        text='create cave', icon='RNDCURVE')


def register():
    bpy.utils.register_class(CC_OT_cave)
    bpy.utils.register_class(CC_PT_cave_creator)


def unregister():
    bpy.utils.unregister_class(CC_OT_cave)
    bpy.utils.unregister_class(CC_PT_cave_creator)


if __name__ == '__main__':
    register()
