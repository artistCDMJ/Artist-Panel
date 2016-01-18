# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Artist Panel",
    "author": "CDMJ",
    "version": (1, 0, 3),
    "blender": (2, 76, 0),
    "location": "Toolbar > Misc Tab > Artist Panel",
    "description": "Art Macros.",
    "warning": "",    
    "category": "Paint",
}






import bpy
  

class MirrorCanvas(bpy.types.Operator):
    """Mirror Canvas from Image as Plane Setup Macro"""
    bl_idname = "image.mirror_canvas" # must match a operator context, like
                                     # view3d, object or image and cannot have
                                     # more then one '.', if you need something
                                     # that is global use wm.create_brush
                                     # and uncomment from line 24-29
    bl_label = "Setup Mirror Canvas"
    bl_options = { 'REGISTER', 'UNDO' }
    
    
    
    def execute(self, context):
        
        scene = context.scene
        
        #get current context
        #bpy.context.active_object
        
        #make textured viewport
        bpy.context.space_data.viewport_shade = 'TEXTURED'

        
        #make shadeless for avoiding highlights and shadows while painting
        bpy.context.object.active_material.use_shadeless = True

        #set variable as current X dimension of image plane
        MoveX = bpy.context.object.dimensions.x
        
        #switch to top view
        bpy.ops.view3d.viewnumpad(type='TOP')

        #enter edit mode to move the mesh
        bpy.ops.object.editmode_toggle()
        
        #add mirror modifier
        bpy.ops.object.modifier_add(type='MIRROR')  


        #move the mesh constrained to X at half of the mesh dimension in X
        bpy.ops.transform.translate(value=(MoveX/2, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, release_confirm=True)
         
        #exit edit mode
        bpy.ops.object.editmode_toggle()





        #apply the mirror modifier to paint on both sides
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Mirror")
        
        #texture paint
        bpy.ops.paint.texture_paint_toggle()
        
        #toggle the tool bar
        #bpy.ops.view3d.toolshelf()
        
        #center to selected in view
        bpy.ops.view3d.view_selected()

        
        #change to camera view

        #commented out-  not needed for this script-cdmj
        #for area in bpy.context.screen.areas:
            #if area.type == 'VIEW_3D':
                #override = bpy.context.copy()
                #override['area'] = area
                #bpy.ops.view3d.viewnumpad(override, type = 'CAMERA')
                #break # this will break the loop after it is first ran
                
        return {'FINISHED'} # this is importent, as it tells blender that the
                            # operator is finished.
                            
class MacroCreateBrush(bpy.types.Operator):
    """Image Brush Scene Setup Macro"""
    bl_idname = "image.create_brush" # must match a operator context, like
                                     # view3d, object or image and cannot have
                                     # more then one '.', if you need something
                                     # that is global use wm.create_brush
                                     # and uncomment from line 24-29
    bl_label = "Setup Scene for Image Brush Maker"
    bl_options = { 'REGISTER', 'UNDO' }
    
    # @classmethod
    # def poll(self, cls):
    #   '''
    #     A function that controls wether the operator can be accessed
    #   '''
    #   return context.area.type in {'VIEW3D'. 'IMAGE'}
    
    def execute(self, context):
        
        scene = context.scene


        #add new scene and name it 'Brush'

        bpy.ops.scene.new(type='NEW')
        bpy.context.scene.name = "Brush"


        #add lamp and move up 4 units in z
        bpy.ops.object.lamp_add( # you can sort elements like this if the code
                                 # is gettings long
          type = 'POINT',
          radius = 1,
          view_align = False,
          location = (0, 0, 4)
        )


        #add camera to center and move up 4 units in Z
        #rename selected camera

        bpy.ops.object.camera_add(
          view_align=False,
          enter_editmode=False,
          location=(0, 0, 4),
          rotation=(0, 0, 0)
        )

        bpy.context.object.name="Tex Camera"





        #change scene size to 1K

        bpy.context.scene.render.resolution_x=1024
        bpy.context.scene.render.resolution_y=1024
        bpy.context.scene.render.resolution_percentage = 100



        #save scene size as preset

        bpy.ops.render.preset_add(name = "1K Texture")

        #change to camera view


        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                override = bpy.context.copy()
                override['area'] = area
                bpy.ops.view3d.viewnumpad(override, type = 'CAMERA')
                break # this will break the loop after it is first ran
                
        return {'FINISHED'} # this is importent, as it tells blender that the
                            # operator is finished.


class CanvasShadeless(bpy.types.Operator):
    """Canvas made shadeless Macro"""
    bl_idname = "image.canvas_shadeless" # must match a operator context, like
                                     # view3d, object or image and cannot have
                                     # more then one '.', if you need something
                                     # that is global use wm.create_brush
                                     # and uncomment from line 24-29
    bl_label = "Canvas Shadeless"
    bl_options = { 'REGISTER', 'UNDO' }
    
    
    def execute(self, context):
        
        scene = context.scene

        #texture draw mode
        bpy.context.space_data.viewport_shade = 'TEXTURED'
        
        #shadeless material
        bpy.context.object.active_material.use_shadeless = True

        #change to local view and centerview
        bpy.ops.view3d.localview()
        
        #change to Texture Paint
        bpy.ops.paint.texture_paint_toggle()

        
        return {'FINISHED'} # this is importent, as it tells blender that the
                            # operator is finished.
                            
                            
                            
#flip horizontal macro
class CanvasHoriz(bpy.types.Operator):
    """Canvas Flip Horizontal Macro"""
    bl_idname = "image.canvas_horizontal" # must match a operator context, like
                                     # view3d, object or image and cannot have
                                     # more then one '.', if you need something
                                     # that is global use wm.create_brush
                                     # and uncomment from line 24-29
    bl_label = "Canvas Horizontal"
    bl_options = { 'REGISTER', 'UNDO' }
    
    
    def execute(self, context):
        
        scene = context.scene
        
        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()


        #flip canvas horizontal
        bpy.ops.transform.resize(value=(-1, 1, 1), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        
        #toggle object to texture
        bpy.ops.paint.texture_paint_toggle()


        

        
        return {'FINISHED'} # this is importent, as it tells blender that the
                            # operator is finished.
                            
                            
#--------------------------------flip vertical macro

class CanvasVertical(bpy.types.Operator):
    """Canvas Flip Vertical Macro"""
    bl_idname = "image.canvas_vertical" # must match a operator context, like
                                     # view3d, object or image and cannot have
                                     # more then one '.', if you need something
                                     # that is global use wm.create_brush
                                     # and uncomment from line 24-29
    bl_label = "Canvas Vertical"
    bl_options = { 'REGISTER', 'UNDO' }
    
    
    def execute(self, context):
        
        scene = context.scene
        
        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()

        #flip canvas horizontal
        bpy.ops.transform.resize(value=(1, -1, 1), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        
        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()

        

        
        return {'FINISHED'} # this is importent, as it tells blender that the
                            # operator is finished.



#--------------------------ccw15

class RotateCanvasCCW15(bpy.types.Operator):
    """Image Rotate CounterClockwise 15 Macro"""
    bl_idname = "image.rotate_ccw_15" # must match a operator context, like
                                     # view3d, object or image and cannot have
                                     # more then one '.', if you need something
                                     # that is global use wm.create_brush
                                     # and uncomment from line 24-29
    bl_label = "Canvas Rotate CounterClockwise 15"
    bl_options = { 'REGISTER', 'UNDO' }
    
    
    def execute(self, context):
        
        scene = context.scene
        
        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()

        #rotate canvas 15 degrees left
        bpy.ops.transform.rotate(value=0.261799, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        
        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()



        
        return {'FINISHED'} # this is important, as it tells blender that the
                            # operator is finished.
    
#--------------------------cw15

class RotateCanvasCW15(bpy.types.Operator):
    """Image Rotate Clockwise 15 Macro"""
    bl_idname = "image.rotate_cw_15" # must match a operator context, like
                                     # view3d, object or image and cannot have
                                     # more then one '.', if you need something
                                     # that is global use wm.create_brush
                                     # and uncomment from line 24-29
    bl_label = "Canvas Rotate Clockwise 15"
    bl_options = { 'REGISTER', 'UNDO' }
    
    
    def execute(self, context):
        
        scene = context.scene
        
        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()

        #rotate canvas 15 degrees left
        bpy.ops.transform.rotate(value=-0.261799, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        
        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()



        
        return {'FINISHED'} # this is important, as it tells blender that the
                            # operator is finished.
                            
#---------------------------ccw 90


class RotateCanvasCCW(bpy.types.Operator):
    """Image Rotate CounterClockwise 90 Macro"""
    bl_idname = "image.rotate_ccw_90" # must match a operator context, like
                                     # view3d, object or image and cannot have
                                     # more then one '.', if you need something
                                     # that is global use wm.create_brush
                                     # and uncomment from line 24-29
    bl_label = "Canvas Rotate CounterClockwise 90"
    bl_options = { 'REGISTER', 'UNDO' }
    
    
    def execute(self, context):
        
        scene = context.scene
        
        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()

        #rotate canvas 90 degrees left
        bpy.ops.transform.rotate(value=1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        
        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()



        
        return {'FINISHED'} # this is important, as it tells blender that the
                            # operator is finished.
    


#-----------------------------------cw 90

class RotateCanvasCW(bpy.types.Operator):
    """Image Rotate Clockwise 90 Macro"""
    bl_idname = "image.rotate_cw_90" # must match a operator context, like
                                     # view3d, object or image and cannot have
                                     # more then one '.', if you need something
                                     # that is global use wm.create_brush
                                     # and uncomment from line 24-29
    bl_label = "Canvas Rotate Clockwise 90"
    bl_options = { 'REGISTER', 'UNDO' }
    
    
    def execute(self, context):
        
        scene = context.scene
        
        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()

        #rotate canvas 90 degrees left
        bpy.ops.transform.rotate(value=-1.5708, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        
        #toggle texture mode / object mode
        bpy.ops.paint.texture_paint_toggle()



        
        return {'FINISHED'} # this is important, as it tells blender that the
                            # operator is finished.
                            
                            
                            
                            
                            
#-----------------------------------reload image


class ImageReload(bpy.types.Operator):
    """Reload Image Last Saved State"""
    bl_idname = "image.reload_saved_state"
    bl_label = "Reload Image Save Point"
    bl_options = { 'REGISTER', 'UNDO' }
    
    
    def execute(self, context):
        
        scene = context.scene
        original_type = bpy.context.area.type
        bpy.context.area.type = 'IMAGE_EDITOR'
        
        #return image to last saved state
        bpy.ops.image.reload()
        
        bpy.context.area.type = original_type
   
        
        


        
        
        return {'FINISHED'}  #operator finished
    
    
    
#--------------------------------image rotation reset

class CanvasResetrot(bpy.types.Operator):
    """Canvas Rotation Reset Macro"""
    bl_idname = "image.canvas_resetrot" # must match a operator context, like
                                     # view3d, object or image and cannot have
                                     # more then one '.', if you need something
                                     # that is global use wm.create_brush
                                     # and uncomment from line 24-29
    bl_label = "Canvas Reset Rotation"
    bl_options = { 'REGISTER', 'UNDO' }
    
    
    def execute(self, context):
        
        scene = context.scene

        #reset canvas rotation
        bpy.ops.object.rotation_clear()

        

        
        return {'FINISHED'} # this is importent, as it tells blender that the
                            # operator is finished.
    

                         
                            
                            
                            
########################################
## panel


class ArtistPanel(bpy.types.Panel):
    """A custom panel in the viewport toolbar"""
    bl_label = "Artist Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Artist Macros"
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        
        row.label(text="Artist Macros")
        
        row = layout.row()
        row.operator("image.reload_saved_state", text = "Reload Image", icon = 'LOAD_FACTORY')
        
        row = layout.row()
        row.operator("image.canvas_horizontal", text = "Canvas Flip Horizontal", icon = 'ARROW_LEFTRIGHT') 
        
        row = layout.row()
        row.operator("image.canvas_vertical", text = "Canvas Flip Vertical", icon = 'FILE_PARENT')
        
        
        row = layout.row()
        row.operator("image.canvas_shadeless", text = "Shadeless Canvas", icon = 'FORCE_TEXTURE')
        
        row = layout.row()
        row.operator("image.create_brush", text = "Brush Maker Scene", icon = 'OUTLINER_OB_CAMERA')
        
        row = layout.row()
        row.operator("image.mirror_canvas", text = "Mirror Canvas Paint", icon = 'MOD_WIREFRAME')
        
        row = layout.row()
        row.operator("image.rotate_ccw_15", text = "Rotate 15 CCW", icon = 'MAN_ROT')
        
        row = layout.row()
        row.operator("image.rotate_cw_15", text = "Rotate 15 CW", icon = 'MAN_ROT')
        
        row = layout.row()
        row.operator("image.rotate_ccw_90", text = "Rotate 90 CCW", icon = 'MAN_ROT')
        
        row = layout.row()
        row.operator("image.rotate_cw_90", text = "Rotate 90 CW", icon = 'MAN_ROT')
        
        row = layout.row()
        row.operator("image.canvas_resetrot", text = "Reset Rotation", icon = 'CANCEL')
        
        
        
              
        
        
        
    
    


def register():
    bpy.utils.register_class(MirrorCanvas)
    bpy.utils.register_class(ArtistPanel)
    bpy.utils.register_class(MacroCreateBrush)
    bpy.utils.register_class(CanvasShadeless)
    bpy.utils.register_class(CanvasHoriz)
    bpy.utils.register_class(CanvasVertical)
    bpy.utils.register_class(RotateCanvasCCW15)
    bpy.utils.register_class(RotateCanvasCW15)
    bpy.utils.register_class(RotateCanvasCCW)
    bpy.utils.register_class(RotateCanvasCW)
    bpy.utils.register_class(ImageReload)
    bpy.utils.register_class(CanvasResetrot)
    
def unregister():
    bpy.utils.unregister_class(MirrorCanvas)
    bpy.utils.unregister_class(ArtistPanel)
    bpy.utils.unregister_class(MacroCreateBrush)
    bpy.utils.unregister_class(CanvasShadeless)
    bpy.utils.unregister_class(CanvasHoriz)
    bpy.utils.unregister_class(CanvasVertical)
    bpy.utils.unregister_class(RotateCanvasCCW15)
    bpy.utils.unregister_class(RotateCanvasCW15)
    bpy.utils.unregister_class(RotateCanvasCCW)
    bpy.utils.unregister_class(RotateCanvasCW)
    bpy.utils.unregister_class(ImageReload)
    bpy.utils.unregister_class(CanvasResetrot)
    
if __name__ == "__main__":
    register()
    





   

