#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk, gobject, cairo
from math import pi, sqrt

from Controller import *
from Model import *

def distance(x1, y1, x2, y2):
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return sqrt(dx*dx + dy*dy)

class GraphArea(gtk.DrawingArea):
    __gsignals__ = { "expose-event": "override" }

    def __init__(self, controller):
        gtk.DrawingArea.__init__(self)
        self.controller = controller
        # Settings
        self.radius = 10
        # Information for dragging nodes
        self.stateSelected = None
        self.dragStart = None
        # Setup clicking on the graph
        self.add_events(gtk.gdk.BUTTON_PRESS_MASK | \
                        gtk.gdk.BUTTON_RELEASE_MASK | \
                        gtk.gdk.POINTER_MOTION_MASK)
        self.connect('button-press-event', self.cb_button_press)
        self.connect('button-release-event', self.cb_button_release)
        # Set this to be re-rendered upon a state update
        controller.registerListener(self.queue_draw)

    def cb_button_press(self, event, data):
        ''' Handle a mouse button press on the graph area '''
        if data.button == 1:
            self.stateSelected = self.selectNode(data.x, data.y)
            self.dragStart = (data.x, data.y)
        else:
            self.stateSelected = None

    def cb_button_release(self, event, data):
        ''' Handle the end of a mouse button press on the 
        graph area '''
        if self.stateSelected is not None:
            print "end of drag of state", self.stateSelected

    def selectNode(self, x, y):
        ''' Selects the node (if any) under 
        the mouse click '''
        graph = self.controller.graph
        for stateNo in xrange(graph.numStates()):
             sx, sy = self.controller.getPosition(stateNo)
             if distance(x, y, sx, sy) <= self.radius:
                 self.controller.selectState(stateNo)
                 return stateNo
        return None
             
    # Handle the expose-event by drawing
    def do_expose_event(self, event):
        # Create the cairo context
        cr = self.window.cairo_create()

        # Restrict Cairo to the exposed area; avoid extra work
        cr.rectangle(event.area.x, event.area.y,
                event.area.width, event.area.height)
        cr.clip()

        self.draw(cr, *self.window.get_size())

    def draw(self, cr, width, height):
        # Fill the background with white
        cr.set_source_rgb(1, 1, 1)
        cr.rectangle(0, 0, width, height)
        cr.fill()
        self.draw_graph(cr)

    def draw_graph(self, cr):
        controller = self.controller
        graph = controller.graph
        npoints = graph.numStates()

        green = (0, 0.8, 0)
        red   = (1, 0, 0)
        black = (0, 0, 0)

        # Draw transitions
        for i in xrange(npoints):
            fromState = graph.getState(i)
            fromXY = controller.getPosition(i)
            for (_, toState) in fromState.listTransitions():
                j = graph.getIndex(toState)
                if i == j:
                    self.draw_loop(cr, fromXY)
                else:
                    toXY = controller.getPosition(j)
                    self.draw_transition(cr, fromXY, toXY)

        # Draw vertices
        for i in xrange(npoints):
            xy = controller.getPosition(i)
            if i == 0: 
                color = green
            elif graph.getState(i).getAttribute('end'):
                color = red
            else:
                color = black
            self.draw_node(cr, xy, color)


    def draw_node(self, cr, (x, y), color):
        cr.save()
        cr.set_source_rgb(*color)
        cr.arc(x, y, 5, 0, 2 * pi)
        cr.fill()
        cr.restore()

    def draw_transition(self, cr, fromXY, toXY):
        cr.save()
        cr.set_source_rgb(0, 0, 0)
        cr.move_to(*fromXY)
        cr.line_to(*toXY)
        cr.stroke()
        cr.restore()

    def draw_loop(self, cr, fromXY, scale=5):
        cr.save()
        cr.move_to(*fromXY)
        cr.set_source_rgb(0, 0, 1)
        cr.rel_curve_to(scale, -2*scale, scale, -3*scale, 0, -3*scale)
        cr.rel_curve_to(-scale, 0, -scale, scale, 0, 3*scale)
        cr.stroke()
        cr.restore()

    def getPosition(self, i):
        return 20 + 20*(i%10), 20 + 20*(i/10)
