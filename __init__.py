#!BPY

bl_info = {
    "name": "Ogre Tools",
    "author": "HadesD",
    "blender": (2, 80, 0),
    "version": (0, 9, 2),
    "location": "File > Import-Export",
    "description": ("Import-Export Ogre Model files, and export Ogre collision files."),
    "warning": "",
    "wiki_url": "",
    "tracker_url": "https://github.com/HadesD/io_mesh_ogre",
    "support": 'OFFICIAL',
    "category": "Import-Export"
}

if "bpy" in locals():
    import imp
    if "OgreImport" in locals():
        imp.reload(OgreImport)
    if "OgreExport" in locals():
        imp.reload(OgreExport)
    if "PhysExport" in locals():
        imp.reload(PhysExport)

import bpy
from bpy.props import (BoolProperty,
                       FloatProperty,
                       StringProperty,
                       EnumProperty,
                       )
from bpy_extras.io_utils import (ExportHelper,
                                 ImportHelper,
                                 path_reference_mode,
                                 axis_conversion,
                                 )


# Path for your OgreXmlConverter
OGRE_XML_CONVERTER = "OgreXMLConverter.exe"

def findConverter(p):
    import os

    # Full path exists
    if os.path.isfile(p): return p

    # Look in script directory
    scriptPath = os.path.dirname( os.path.realpath( __file__ ) )
    sp = os.path.join(scriptPath, p)
    if os.path.isfile(sp): return sp

    # Fail
    print('Could not find xml converter', p)
    return None



class ImportOgre(bpy.types.Operator, ImportHelper):
    '''Load an Ogre MESH File'''
    bl_idname = "import_scene.mesh"
    bl_label = "Import MESH"
    bl_options = {'PRESET'}

    filename_ext = ".mesh"


    keep_xml: BoolProperty(
            name="Keep XML",
            description="Keeps the XML file when converting from .MESH",
            default=False,
            )
    
    import_normals: BoolProperty(
            name="Import Normals",
            description="Import custom mesh normals",
            default=True,
            )

    import_animations: BoolProperty(
            name="Import animation",
            description="Import animations as actions",
            default=True,
            )

    round_frames: BoolProperty(
            name="Adjust frame rate",
            description="Adjust scene frame rate to match imported animation",
            default=True,
            )
            
    import_shapekeys: BoolProperty(
            name="Import shape keys",
            description="Import shape keys (morphs)",
            default=True,
            )
    
    use_selected_skeleton: BoolProperty(
            name='Use selected skeleton',
            description='Link with selected armature object rather than importing a skeleton.\nUse this for importing skinned meshes that don\'t have their own skeleton.\nMake sure you have the correct skeleton selected or the weight maps may get mixed up.',
            default=False,
            )

    filter_glob: StringProperty(
            default="*.mesh;*.MESH;.xml;.XML",
            options={'HIDDEN'},
            )

    xml_converter: StringProperty(
            name="XML Converter",
            description="Ogre XML Converter program for converting between .MESH files and .XML files",
            default=OGRE_XML_CONVERTER
            )


    def execute(self, context):
        # print("Selected: " + context.active_object.name)
        from . import OgreImport

        keywords = self.as_keywords(ignore=("filter_glob",))
        keywords['xml_converter'] = findConverter( keywords['xml_converter'] )

        print( 'converter', keywords['xml_converter'])

        bpy.context.window.cursor_set("WAIT")
        result = OgreImport.load(self, context, **keywords)
        bpy.context.window.cursor_set("DEFAULT")
        return result

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "xml_converter")
        layout.prop(self, "keep_xml")
        layout.prop(self, "import_normals")
        layout.prop(self, "import_shapekeys")
        
        link = layout.column()
        link.enabled = True if context.active_object and context.active_object.type == 'ARMATURE' else False
        link.prop(self, "use_selected_skeleton")

        layout.prop(self, "import_animations")

        rate = layout.column()
        rate.enabled = self.import_animations
        rate.prop(self, "round_frames")

##############################################################################################################################

class ExportOgre(bpy.types.Operator, ExportHelper):
    '''Export a Kenshi MESH File'''

    bl_idname = "export_scene.mesh"
    bl_label = 'Export MESH'
    bl_options = {'PRESET'}

    filename_ext = ".mesh"

    xml_converter: StringProperty(
            name="XML Converter",
            description="Ogre XML Converter program for converting between .MESH files and .XML files",
            default=OGRE_XML_CONVERTER,
            )

    export_tangents: BoolProperty(
            name="Export tangents",
            description="Export tangent data for the mesh",
            default=True,
            )
    tangent_parity: BoolProperty(
            name="   Parity in W",
            description="Tangents have parity stored in the W component",
            default=False,
            )

    export_binormals: BoolProperty(
            name="Export Binormals",
            description="Generate binormals for the mesh",
            default=False,
            )

    export_colour: BoolProperty(
            name="Export colour",
            description="Export vertex colour data. Name a colour layer 'Alpha' to use as the alpha component",
            default=False,
            )

    keep_xml: BoolProperty(
            name="Keep XML",
            description="Keeps the XML file when converting to .MESH",
            default=False,
            )

    apply_transform: BoolProperty(
            name="Apply Transform",
            description="Applies object's transformation to its data",
            default=False,
            )

    apply_modifiers: BoolProperty(
            name="Apply Modifiers",
            description="Applies modifiers to the mesh",
            default=False,
            )

    export_poses: BoolProperty(
            name="Export shape keys",
            description="Export shape keys as poses",
            default=False,
            )

    export_materials: BoolProperty(
            name="Export materials",
            description="Export material files. Kenshi does not use these",
            default=False,
            )

    overwrite_material: BoolProperty(
            name="Overwrite material",
            description="Overwrites existing .material file, if present.",
            default=False,
            )

    copy_textures: BoolProperty(
            name="Copy textures",
            description="Copies material source textures to material file location",
            default=False,
            )

    export_skeleton: BoolProperty(
            name="Export skeleton",
            description="Exports new skeleton and links the mesh to this new skeleton.\nLeave off to link with existing skeleton if applicable.",
            default=False,
            )

    export_animation: BoolProperty(
            name="Export Animation",
            description="Export all actions attached to the selected skeleton as animations",
            default=False,
            )

    filter_glob: StringProperty(
            default="*.mesh;*.MESH;.xml;.XML",
            options={'HIDDEN'},
            )

    def invoke(self, context, event):
        #if not self.filepath:
        #    self.filepath = bpy.path.ensure_ext(bpy.data.filepath, ".bm")
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        from . import OgreExport
        from mathutils import Matrix

        keywords = self.as_keywords(ignore=("check_existing", "filter_glob"))
        keywords['xml_converter'] = findConverter( keywords['xml_converter'] )
        
        bpy.context.window.cursor_set("WAIT")
        result = OgreExport.save(self, context, **keywords)
        bpy.context.window.cursor_set("DEFAULT")
        return result


    def draw(self, context):
        layout = self.layout

        xml = layout.box()
        xml.prop(self, "xml_converter")
        xml.prop(self, "keep_xml")
        
        mesh = layout.box()
        mesh.prop(self, "export_tangents")
        mesh.prop(self, "export_binormals")
        mesh.prop(self, "export_colour")
        mesh.prop(self, "export_poses")
        mesh.prop(self, "apply_transform")
        mesh.prop(self, "apply_modifiers")

        material = layout.box()
        material.prop(self, "export_materials")
        materialOps = material.column()
        materialOps.prop(self, "overwrite_material")
        materialOps.prop(self, "copy_textures")
        materialOps.enabled = False

        skeleton = layout.box()
        skeleton.prop(self, "export_skeleton")
        skeleton.prop(self, "export_animation")

##############################################################################################################################

class ExportKenshiCollision(bpy.types.Operator, ExportHelper):
    '''Export a Kenshi MESH File'''

    bl_idname = "export_scene_collision.xml"
    bl_label = 'Export Collision'
    bl_options = {'PRESET'}
    filename_ext = ".xml"

    objects: EnumProperty(
            name="Objects",
            description="Which objects to export",
            items=[('ALL', 'All Objects', 'Export all collision objects in the scene'),
                    ('SELECTED', 'Selection', 'Export only selected objects'),
                    ('CHILDREN', 'Selected Children', 'Export selected objects and all their child objects')],
            default='CHILDREN',
            )
    transform: EnumProperty(
            name="Transform",
            description="Root transformation",
            items=[('SCENE', 'Scene', 'Export objects relative to scene origin'),
                    ('PARENT', 'Parent', 'Export objects relative to common parent'),
                    ('ACTIVE', 'Active', 'Export objects relative to the active object')],
            default='PARENT',
            )

    filter_glob: StringProperty(
            default="*.xml;*.XML",
            options={'HIDDEN'},
            )

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        from . import PhysExport
        keywords = self.as_keywords(ignore=("check_existing", "filter_glob"))
        bpy.context.window.cursor_set("WAIT")
        result = PhysExport.save(self, context, **keywords)
        bpy.context.window.cursor_set("DEFAULT")
        return result


    def draw(self, context):
        layout = self.layout
        layout.prop(self, "objects")
        layout.prop(self, "transform")

##############################################################################################################################

def menu_func_import(self, context):
    self.layout.operator(ImportOgre.bl_idname, text="Kenshi OGRE (.mesh)")


def menu_func_export(self, context):
    self.layout.operator(ExportOgre.bl_idname, text="Kenshi OGRE (.mesh)")

def menu_func_export_collision(self, context):
    self.layout.operator(ExportKenshiCollision.bl_idname, text="Kenshi Collision (.xml)")


classes = ( ImportOgre, ExportOgre, ExportKenshiCollision )

def register():
    from bpy.utils import register_class
    for cls in classes: register_class(cls)

    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export_collision)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes): unregister_class(cls)

    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export_collision)

if __name__ == "__main__":
    register()
