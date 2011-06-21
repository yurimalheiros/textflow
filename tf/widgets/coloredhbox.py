# -*- coding: utf-8 -*-

#######################################################################
# Copyright © 2009 TextFlow Team
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# the Free Software Foundation; version 2 only.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#######################################################################

import gtk
import cairo

class ColoredHBox(gtk.HBox):
    """
    A HBox container with round borders and gradient color background.
    """
    
    def __init__(self, color_stroke, color_begin, color_end, gradient_pos, curve):
        """.
        Constructor
        
        @param color_stroke: a tuple (R, G, B) to determine the color of stroke.
                             0 is the mininum and 1 the maximum value.
        @type color_stroke: a Tuple.
        
        @param color_begin: a tuple (R, G, B) to determine the first color of gradient.
                            0 is the mininum and 1 the maximum value.
        @type color_begin: a Tuple.
        
        @param color_end: a tuple (R, G, B) to determine the last color of gradient.
                          0 is the mininum and 1 the maximum value.
        @type color_end: a Tuple.
        
        @param gradient_pos: the position where gradient stops.
        @type gradient_pos: a Float.
        
        @param curve: the size of round borders.
        @param curve: a Int.
        """
        super(ColoredHBox, self).__init__()
        
        self.color_stroke = color_stroke
        self.color_begin = color_begin
        self.color_end = color_end
        self.gradient_pos = gradient_pos
        self.__curve = curve * 2
        
        self.connect("expose_event", self.expose)
        self.connect("size-allocate", self.size_allocate)


    #################### Properties ####################

    @property
    def curve(self):
        return self.__curve / 2
    
    @curve.setter
    def curve(self, value):
        self.__curve = value * 2


    #################### Callbacks ####################
    
    def size_allocate(self, widget, allocation):
        self.queue_draw()
        
        return False

    
    def expose(self, widget, event):
        context = self.window.cairo_create()
        
        alloc = self.get_allocation()
        context.rectangle(alloc.x, alloc.y, alloc.width, alloc.height)
        context.clip()
        
        pat = cairo.LinearGradient(0.0, alloc.y, 0.0, alloc.y + self.gradient_pos)
        pat.add_color_stop_rgba(0, self.color_begin[0], self.color_begin[1],
                                self.color_begin[2], 1)
                                
        pat.add_color_stop_rgba(1, self.color_end[0], self.color_end[1],
                                self.color_end[2], 1)

        
        ld = self.__curve
        cd = ld / 2.0
        
        self.roundedrec(context, alloc.x, alloc.y, alloc.width, alloc.height, self.__curve)
        
        context.set_source(pat)
        context.fill_preserve()
        context.set_source_rgb(self.color_stroke[0], self.color_stroke[1],
                               self.color_stroke[2])
        context.set_line_width(1)
        context.stroke()
        
        return False


    def roundedrec(self,context,x,y,w,h,r = 10):
        "Draw a rounded rectangle"
        #   A****BQ
        #  H      C
        #  *      *
        #  G      D
        #   F****E

        context.move_to(x+r,y)                      # Move to A
        context.line_to(x+w-r,y)                    # Straight line to B
        context.curve_to(x+w,y,x+w,y,x+w,y+r)       # Curve to C, Control points are both at Q
        context.line_to(x+w,y+h-r)                  # Move to D
        context.curve_to(x+w,y+h,x+w,y+h,x+w-r,y+h) # Curve to E
        context.line_to(x+r,y+h)                    # Line to F
        context.curve_to(x,y+h,x,y+h,x,y+h-r)       # Curve to G
        context.line_to(x,y+r)                      # Line to H
        context.curve_to(x,y,x,y,x+r,y)             # Curve to A
        return


    def roundedrecA(self,cr,x,y,width,height,radius=5):
        #/* a custom shape, that could be wrapped in a function */
        #radius = 5  #/*< and an approximate curvature radius */        
        x0       = x+radius/2.0   #/*< parameters like cairo_rectangle */
        y0       = y+radius/2.0
        rect_width  = width - radius
        rect_height = height - radius

        cr.save()
        #cr.set_line_width (0.04)
        #self.snippet_normalize (cr, width, height)

        x1=x0+rect_width
        y1=y0+rect_height
        #if (!rect_width || !rect_height)
        #    return
        if rect_width/2<radius:
            if rect_height/2<radius:
                cr.move_to  (x0, (y0 + y1)/2)
                cr.curve_to (x0 ,y0, x0, y0, (x0 + x1)/2, y0)
                cr.curve_to (x1, y0, x1, y0, x1, (y0 + y1)/2)
                cr.curve_to (x1, y1, x1, y1, (x1 + x0)/2, y1)
                cr.curve_to (x0, y1, x0, y1, x0, (y0 + y1)/2)
            else:
                cr.move_to  (x0, y0 + radius)
                cr.curve_to (x0 ,y0, x0, y0, (x0 + x1)/2, y0)
                cr.curve_to (x1, y0, x1, y0, x1, y0 + radius)
                cr.line_to (x1 , y1 - radius)
                cr.curve_to (x1, y1, x1, y1, (x1 + x0)/2, y1)
                cr.curve_to (x0, y1, x0, y1, x0, y1- radius)

        else:
            if rect_height/2<radius:
                cr.move_to  (x0, (y0 + y1)/2)
                cr.curve_to (x0 , y0, x0 , y0, x0 + radius, y0)
                cr.line_to (x1 - radius, y0)
                cr.curve_to (x1, y0, x1, y0, x1, (y0 + y1)/2)
                cr.curve_to (x1, y1, x1, y1, x1 - radius, y1)
                cr.line_to (x0 + radius, y1)
                cr.curve_to (x0, y1, x0, y1, x0, (y0 + y1)/2)
            else:
                cr.move_to  (x0, y0 + radius)
                cr.curve_to (x0 , y0, x0 , y0, x0 + radius, y0)
                cr.line_to (x1 - radius, y0)
                cr.curve_to (x1, y0, x1, y0, x1, y0 + radius)
                cr.line_to (x1 , y1 - radius)
                cr.curve_to (x1, y1, x1, y1, x1 - radius, y1)
                cr.line_to (x0 + radius, y1)
                cr.curve_to (x0, y1, x0, y1, x0, y1- radius)

        cr.close_path ()

        cr.restore()

