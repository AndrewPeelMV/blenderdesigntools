"""
This script contains common opengl functions and classes

"""

import bpy, blf, bgl

def get_dpi():
    system_preferences = bpy.context.user_preferences.system
    factor = getattr(system_preferences, "pixel_size", 1)
    return int(system_preferences.dpi * factor)

def get_dpi_factor():
    return get_dpi() / 72

def round_box(minx, miny, maxx, maxy, rad, corners = [True, True, True, True]):
    '''
    TODO, make smarter indexing decisions so only some corners have
    to be rounded
    '''
   
    vec0 = [[0.195, 0.02],
           [0.383, 0.067],
           [0.55, 0.169],
           [0.707, 0.293],
           [0.831, 0.45],
           [0.924, 0.617],
           [0.98, 0.805]]
    
    #cache so we only scale the corners once
    vec = [[0,0]]*len(vec0)
    for i in range(0,len(vec0)):
        vec[i] = [vec0[i][0]*rad, vec0[i][1]*rad]
        
    verts = [[0,0]]*(9*4)
    
    # start with corner right-bottom
    verts[0] = [maxx-rad,miny]
    for i in range(1,8):
        verts[i]= [maxx - rad + vec[i-1][0], miny + vec[i-1][1]] #done
    verts[8] = [maxx, miny + rad]   #done
           
    #corner right-top    
    verts[9] = [maxx, maxy - rad]
    for i in range(10,17):
        verts[i]= [maxx - vec[i-10][1], maxy - rad + vec[i-10][0]]
    verts[17] = [maxx-rad, maxy]
    
    #corver left top
    verts[18] = [minx + rad, maxy]
    for i in range(19,26):
        verts[i]= [minx + rad - vec[i-19][0], maxy - vec[i-19][1]] #done
    verts[26] = [minx, maxy - rad]
    
    #corner left bottom    
    verts[27] = [minx, miny+rad]
    for i in range(28,35):
        verts[i]= [minx + vec[i-28][1], miny + rad - vec[i-28][0]]    #done
    verts[35]=[minx + rad, miny]
    
    
    return verts

def draw_outline_or_region(mode, points, color):
    '''  
    arg: 
    mode - either bgl.GL_POLYGON or bgl.GL_LINE_LOOP
    color - will need to be set beforehand using theme colors. eg
    bgl.glColor4f(self.ri, self.gi, self.bi, self.ai)
    '''
    
    bgl.glColor4f(color[0],color[1],color[2],color[3])
    if mode == 'GL_LINE_LOOP':
        bgl.glBegin(bgl.GL_LINE_LOOP)
    else:
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glBegin(bgl.GL_POLYGON)
    
    # start with corner right-bottom
    for i in range(0,len(points)):
        bgl.glVertex2f(points[i][0],points[i][1])
    
    bgl.glEnd()

class TextBox(object):
    
    def __init__(self,x,y,width,height,border, margin, message):
        context = bpy.context
        
        self.x = x #middle of text box
        self.y = y #top of text box
        self.def_width = width
        self.def_height = height
        self.hang_indent = '-'
        
        self.width = width * get_dpi_factor()
        self.height = height * get_dpi_factor()
        self.border = border * get_dpi_factor()
        self.margin = margin * get_dpi_factor()
        self.spacer = 15 * get_dpi_factor()  # pixels between text lines
        self.is_collapsed = False
        self.is_hovered = False
        self.collapsed_msg = "Click for Help"

        self.text_size = 12
        self.text_dpi = get_dpi()
        blf.size(0, self.text_size, self.text_dpi)
        
        self.line_height = self.txt_height('A')
        self.raw_text = message
        self.text_lines = []
        self.format_and_wrap_text()

        self.window_dims = (context.window.width, context.window.height)

    def txt_height(self, text):
        return blf.dimensions(0,text)[1]
    
    def txt_width(self, text):
        return blf.dimensions(0,text)[0]
    
    def fit_box_width_to_text_lines(self):
        '''
        shrink width of box to fit width of text
        '''
        blf.size(0, self.text_size, self.text_dpi)
        max_width = max(self.txt_width(line) for line in self.text_lines)
        self.width = min(max_width + 2*self.border, self.def_width)
        
    def fit_box_height_to_text_lines(self):
        '''
        fit height of box to match text
        '''
        blf.size(0, self.text_size, self.text_dpi)
        line_height = self.txt_height('A')
        line_count  = len(self.text_lines)
        self.height = line_count*(line_height + self.spacer) + 2*self.border
        
    def format_and_wrap_text(self):
        '''
        '''
        blf.size(0, self.text_size, self.text_dpi)
        
        # remove \r characters (silly windows machines!)
        self.raw_text = self.raw_text.replace('\r','')
        
        #TODO text size settings?
        useful_width = self.width - 2 * self.border
        #print('>>> useful width = % 8.1f' % useful_width)
        
        # special case: no newlines and we fit already!
        if '\n' not in self.raw_text and self.txt_width(self.raw_text) < useful_width:
            self.text_lines = [self.raw_text]
            return
        
        def split_word(line):
            '''
            splits off first word, including any leading spaces
            '''
            if not line: return (None,None)
            sp = (line[0] == ' ')
            for i,c in enumerate(line):
                if c == ' ':
                    if not sp: return (line[:i], line[i:])
                    continue
                sp = False
            return (line,'')
        
        def wrap_line(line):
            '''
            takes a string, returns a list of strings, corresponding to wrapped
            text of the specified pixel width, given current BLF settings
            '''
            
            line = line.rstrip() # ignore right whitespace
            
            if self.txt_width(line) < useful_width:
                # no need to wrap!
                lines = [line]
                #for line in lines:
                #    print('>>> line width = % 8.1f: %s' % (self.txt_width(line), line))
                return lines
            
            lines = []
            working = ""
            while line:
                word,line = split_word(line)
                if self.txt_width(working + word) < useful_width:
                    working += word
                else:
                    # adding word is too wide!
                    # start new row
                    lines += [working]
                    working = '  ' + word.strip() # lead with exactly two spaces
            lines += [working]
            
            #for line in lines:
            #    print('>>> line width = % 8.1f: %s' % (self.txt_width(line), line))
            
            return lines
        
        self.text_lines = []
        for line in self.raw_text.split('\n'):
            self.text_lines += wrap_line(line)
        
        self.fit_box_height_to_text_lines()
        self.fit_box_width_to_text_lines()
    
    def draw(self):
        blf.size(0, self.text_size, self.text_dpi)
        
        self.fit_box_width_to_text_lines()
        self.fit_box_height_to_text_lines()
        
        if (bpy.context.window.width, bpy.context.window.height) != self.window_dims:
            self.snap_to_corner(bpy.context, corner = [1,1])
            self.window_dims = (bpy.context.window.width, bpy.context.window.height)
        bgcol = bpy.context.user_preferences.themes[0].user_interface.wcol_menu_item.inner
        bgR = bgcol[0]
        bgG = bgcol[1]
        bgB = bgcol[2]
        bgA = .5
        bg_color = (bgR, bgG, bgB, bgA)
        
        txtcol = bpy.context.user_preferences.themes[0].user_interface.wcol_menu_item.text
        txt_color = (txtcol[0], txtcol[1], txtcol[2], .9) #RGBA
        
        bordcol = bpy.context.user_preferences.themes[0].user_interface.wcol_menu_item.outline
        border_color = (.8, .8, .8, .8) #RGBA
#         border_color = (bordcol[0], bordcol[1], bordcol[2], .8) #RGBA
        
        left = self.x - self.width/2
        bottom = self.y - self.height
        top = self.y
        
        #draw the whole menu background
        line_height = self.txt_height('A')
        outline = round_box(left, bottom, left +self.width, bottom + self.height, (line_height + 2 * self.spacer)/6)
        draw_outline_or_region('GL_POLYGON', outline, bg_color)
        draw_outline_or_region('GL_LINE_LOOP', outline, border_color)
        
#         if self.is_collapsed:
#             txt_x = left + self.border
#             txt_y = top - self.border - line_height
#             blf.position(0,txt_x, txt_y, 0)
#             bgl.glColor4f(*txt_color)
#             blf.draw(0, self.collapsed_msg)
#             return
        
        for i, line in enumerate(self.text_lines):
            
            txt_x = left + self.border
#             txt_y = top - self.border - (i+1) * (line_height + self.spacer)
            txt_y = top - (i+1) * (line_height + self.spacer)
            
            blf.position(0,txt_x, txt_y, 0)
            bgl.glColor4f(*txt_color)
            blf.draw(0, line)
            