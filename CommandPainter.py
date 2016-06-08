import bpy
import threading
import subprocess
import os

from SubstanceBridge.settings import SubstanceSettings

# ------------------------------------------------------------------------
# Create a class for a generic thread, else blender are block.
# ------------------------------------------------------------------------
class PainterThread(threading.Thread):
    def __init__(self):
        self.stdout = None
        self.stderr = None
        threading.Thread.__init__(self)

    def run(self):
        user_preferences = bpy.context.user_preferences
        addon_prefs = user_preferences.addons["SubstanceBridge"].preferences
        painter = str(addon_prefs.painterpath) # Set path for instant meshes
        
        mesh = 'E:\\Temp\\Blender\\zob.obj'
        project = 'E:\\Documents\\Substance Painter\\samples\\Hans.spp'
        
        popen = subprocess.call([painter, '--mesh', mesh])

# ------------------------------------------------------------------------
# Function to create an Obj, and export to painter
# ------------------------------------------------------------------------
class NewPainterProject(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.painter_export"
    bl_label = "Send mesh to painter export"
    
    def execute(self, context):
        # All variable for the script
        obj = bpy.context.active_object
        mesh = 'E:\\Temp\\Blender\\zob.obj'
        path = 'D:\\Games\\SteamLibrary\\steamapps\\common\\Substance Painter\\Substance Painter.exe'
        # path = 'D:\\Graflog\\Allegorithmic\\Substance Painter 2\\Substance Painter 2.exe'
        command = "zob"
        
        if obj.type == 'MESH':
            if bpy.data.meshes[obj.name].uv_textures:
                # Export du mesh selectionne
                bpy.ops.export_scene.obj(filepath=mesh, use_selection=True, path_mode='AUTO')

                # def launch_painter(self):
                """Launch substance painter program."""
                myclass = PainterThread()
                myclass.start()
                # print(painterpath)

            else:
                self.report({'WARNING'}, "This object don't containt a UV layers.")
                return {'CANCELLED'}

        else:
            self.report({'WARNING'}, "This object is not a mesh.")
            return {'CANCELLED'}

        return {'FINISHED'}