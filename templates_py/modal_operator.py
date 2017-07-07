import bpy

class OPS_modal_operator(bpy.types.Operator):
    bl_idname = "fd_assembly.modal_operator"
    bl_label = "Modal Operator"
    bl_options = {'UNDO'}
    
    #READONLY
    _draw_handle = None
    mouse_x = 0
    mouse_y = 0
    
    def cancel_drop(self,context,event):
        pass
        #Clean Up Scene
        
    def finish(self,context):
        context.space_data.draw_handler_remove(self._draw_handle, 'WINDOW')
        context.window.cursor_set('DEFAULT')
        
        #FINSH COMMAND
        
        context.area.tag_redraw()
        return {'FINISHED'}

    @staticmethod
    def _window_region(context):
        window_regions = [region
                          for region in context.area.regions
                          if region.type == 'WINDOW']
        return window_regions[0]

    def draw_opengl(self,context):     
        region = self._window_region(context)
        
        # DRAW OPENGL ELEMENTS

    def modal(self, context, event):
        context.area.tag_redraw()
        
        self.mouse_x = event.mouse_x
        self.mouse_y = event.mouse_y

        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.finish(context)
            return {'CANCELLED'}
        
        if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
            return {'PASS_THROUGH'}        
        
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.mouse_x = event.mouse_x
        self.mouse_y = event.mouse_y
        
        self._draw_handle = context.space_data.draw_handler_add(
            self.draw_opengl, (context,), 'WINDOW', 'POST_PIXEL')
        
        context.window_manager.modal_handler_add(self)
        context.area.tag_redraw()
        return {'RUNNING_MODAL'}