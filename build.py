#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import gobject

from states import *
        

class BuilderWindow:
    def __init__(self):
        ''' Set up the window '''
        window = self._makeWindow()
        window.show_all()

    def _makeWindow(self):
        ''' Creates the window object '''
        # Create window
        w = gtk.Window(gtk.WINDOW_TOPLEVEL)
        w.connect('delete_event', self.delete_event)
        w.connect('destroy', self.destroy)
        w.set_default_size(800,600)
        # Set content
        vb = gtk.VBox(False, 0)
        vb.pack_start(self._makeMenuBar(), False, False)
        vb.pack_start(self._makeLayout(), False, False)
        w.add(vb)
        # Return the window
        self.window = w
        self.setTitle()
        return w

    def _makeMenuBar(self):
        ''' Create the menu bar '''
        menu = gtk.MenuBar()
        mFile = gtk.MenuItem('File')
        muFile = gtk.Menu()
        mFile.set_submenu(muFile)
        mFileQuit = gtk.MenuItem('Quit')
        muFile.add(mFileQuit)
        menu.add(mFile)
        mEdit = gtk.MenuItem('Edit')
        menu.add(mEdit)
        mPlay = gtk.MenuItem('Play')
        menu.add(mPlay)
        self.menuBar = menu
        return menu

    def _makeLayout(self):
        ''' Creates the HBox within the window '''
        hb = gtk.HBox(False, 0)
        hb.pack_start(self._makeLeftPane())
        hb.pack_start(self._makeRightPane(), False)
        self.hb = hb
        return hb

    def _makeLeftPane(self):
        ''' Creates the VBox holding the left pane '''
        drawing = gtk.DrawingArea()
        drawing.set_size_request(400, 400)
        drawing.connect('expose-event', self.draw_graph)
        self.graphPane = drawing
        return drawing

    def _makeRightPane(self):
        ''' Creates the VBox holding the right pane '''
        # Setup
        vb = gtk.VBox(False, 5)
        vb.set_border_width(5)
        vb.set_size_request(300, -1)
        # Content - State selection
        vb.pack_start(self._makeStateSelection(), False, False)
        vb.pack_start(gtk.HSeparator())
        # Content - State text
        vb.pack_start(leftLabel('State text:'))
        vb.pack_start(self._makeStateText(), False, False)
        vb.pack_start(gtk.HSeparator())
        # Content - Transitions
        vb.pack_start(leftLabel('Transitions:'))
        vb.pack_start(self._makeAddTransition(), False, False)
        vb.pack_start(self._makeTransitionList(), False, False)
        # Store
        self.rightPane = vb
        return vb

    def _makeStateSelection(self):
        ''' Creates selection box for states '''
        hb = gtk.HBox(False, 0)
        stateLabel = leftLabel('State: ')
        hb.pack_start(stateLabel)
        stateCombo = gtk.ComboBox()
        hb.pack_start(stateCombo)
        self.stateCombo = stateCombo
        return hb

    def _makeStateText(self):
        ''' Creates box for entering a state's text '''
        # Text box
        text = gtk.TextView()
        text.set_cursor_visible(True)
        text.set_wrap_mode(gtk.WRAP_CHAR)
        text.set_size_request(0, 100)
        # Scrolled window
        scroll = gtk.ScrolledWindow()
        scroll.add(text)
        scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_ALWAYS)
        scroll.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        # Store
        self.stateTextBuffer = text.get_buffer()
        self.stateText = text
        return scroll

    def _makeAddTransition(self):
        ''' Creates the inputs to add a transition '''
        vb = gtk.VBox(False, 0)
        entry = gtk.Entry(max = 100)
        vb.pack_start(entry)
        hb = gtk.HBox(False, 0)
        hb.pack_start(leftLabel('to'), False, False, 5)
        combo = gtk.ComboBox()
        hb.pack_start(combo, False, False, 5)
        btn = gtk.Button('add')
        hb.pack_start(btn, False, False, 5)
        vb.pack_start(hb)
        self.trEntry = entry
        self.trCombo = combo
        self.trAdd = btn
        return vb

    def _makeTransitionList(self):
        ''' Creates a scroll pane containing the list of 
        transitions '''
        # Scrolled Window
        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scroll.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        #scroll.set_size_request(0, 100)
        # List of transitions
        vb = gtk.VBox(False, 0)
        scroll.add_with_viewport(vb)
        self.trList = vb
        return scroll

    def setTransitionItems(self, items):
        ''' Creates an element in the list of 
        transitions '''
        self.trList.clear()
        for (n, s) in items:
            row = (n, s, gtk.Button('-'))
            self.trList.append(row)

    def setTitle(self, fileName=None):
        ''' Sets the title of the window '''
        title = 'DFA editor'
        if fileName:
            title = fileName + ' - ' + title
        self.window.set_title(title)

    def draw_graph(self, area, event):
        style = self.graphPane.get_style()
        gc = style.fg_gc[gtk.STATE_NORMAL]
        self.graphPane.window.draw_rectangle(gc, True, 100, 100, 200, 200)
        return True

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()


def leftLabel(text):
    label = gtk.Label(text)
    label.set_alignment(0, 0.5)
    return label

def main():
    builder = BuilderWindow()
    gtk.main()

if __name__ == '__main__':
    main()